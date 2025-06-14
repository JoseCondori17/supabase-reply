import math
from collections import defaultdict, Counter

from server.types.text import preprocess
from server.storage.indexes.bptree import BPlusTreeFile
from server.storage.disk.file_manager import FileManager
from server.storage.disk.path_builder import PathBuilder


class InvertedIndex:
    def __init__(self, fm: FileManager, pb: PathBuilder, db: str, schema: str, table: str, column: str):
        self.fm = fm
        self.pb = pb
        self.db = db
        self.schema = schema
        self.table = table
        self.column = column

        index_path = self.pb.table_index(db, schema, table, column)
        self.index = BPlusTreeFile(str(index_path), str, key_len=256)
        self.doc_norms = {}

    def build(self, documents: dict[int, str]):
        """
        Construye el índice invertido con TF-IDF y guarda las normas para similitud coseno.
        """
        N = len(documents)
        term_doc_freq = defaultdict(list)
        tf_per_doc = {}

        # Paso 1: tokenizar y contar TF por doc
        for doc_id, text in documents.items():
            tokens = preprocess(text)
            counts = Counter(tokens)
            tf_per_doc[doc_id] = counts
            for term, freq in counts.items():
                term_doc_freq[term].append((doc_id, freq))

        # Paso 2: Calcular TF-IDF y guardar en B+Tree
        for term, postings in term_doc_freq.items():
            df = len(postings)
            idf = math.log(N / df)
            posting_list = []
            for doc_id, tf in postings:
                tfidf = tf * idf
                posting_list.append((doc_id, tfidf))
            self.index.insert(term, posting_list)

        # Paso 3: Guardar norma de cada doc para coseno
        for doc_id, counts in tf_per_doc.items():
            norm = 0.0
            for term, tf in counts.items():
                idf = math.log(N / len(term_doc_freq[term]))
                norm += (tf * idf) ** 2
            self.doc_norms[doc_id] = math.sqrt(norm)

        # Guardar normas en disco
        norms_path = self.pb.table_index(self.db, self.schema, self.table, self.column).with_suffix(".norms")
        self.fm.write_data(self.doc_norms, norms_path)

    def query(self, query: str, top_k: int = 5):
        """
        Consulta una frase y devuelve top-k docs usando similitud coseno.
        """
        query_tokens = preprocess(query)
        query_tf = Counter(query_tokens)
        scores = defaultdict(float)

        # Cargar normas del disco
        norms_path = self.pb.table_index(self.db, self.schema, self.table, self.column).with_suffix(".norms")
        self.doc_norms = self.fm.read_data(norms_path)

        for term, tf in query_tf.items():
            postings = self.index.search(term)
            if postings:
                for doc_id, doc_tfidf in postings:
                    scores[doc_id] += tf * doc_tfidf

        # Normalizar
        query_norm = math.sqrt(sum(tf ** 2 for tf in query_tf.values()))
        for doc_id in scores:
            scores[doc_id] /= (query_norm * self.doc_norms[doc_id] + 1e-9)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]
