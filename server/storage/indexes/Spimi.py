import math
import sys

import numpy as np
import os
import pandas as pd
import pickle
from server.types.text import preprocess, preprocess_word, count_tokens
from collections import defaultdict
import shutil

from server.storage.indexes.spimi_utils.BlockSpimi import BlockSpimi, FinallyMerge, binary_search_block_index, copiar_contenido
from server.storage.indexes.spimi_utils.LinkedPostingList import LinkedPostingList
from server.storage.indexes.spimi_utils.DocTf import DocTf


# pct_block <- que tan alejado quiero que esté mi memoria disponible con respecto a la memoría mínima
# ocupada por un bloque

# pct_pg <- tam_block * pct_pg.
def inicializar_hiperparametros_spimi(doc_list, pct_pg=0.4):
    if not (0 < pct_pg <= 1):
        raise ValueError("El valor de pct_pg debe estar en el rango (0, 1]")

    token_docIDs = defaultdict(set)
    total_tokens = 0

    for doc_id, doc in enumerate(doc_list):
        tokens = preprocess(doc)
        total_tokens += len(tokens)
        for token in set(tokens):
            token_docIDs[token].add(doc_id)

    tam_block = max(15, 0.1 * (total_tokens + 1) ** 0.6)

    df_list = [len(docIDs) for docIDs in token_docIDs.values()]
    df_prom = np.mean(df_list)
    tam_posting_list = max(2.0, pct_pg * df_prom)

    return math.floor(tam_block), math.ceil(tam_posting_list)


class SpimiIndex:

    def __init__(self, DocList, path_save, inicializar_hp=True, tam_block=10, tam_posting_list=5):

        self.path_save = path_save
        self.path_save_temporal = self.path_save + "_temporal"

        self.DocList = DocList

        if inicializar_hp:
            self.tam_block, self.tam_posting_list = inicializar_hiperparametros_spimi(DocList)
        else:
            self.tam_block = tam_block
            self.tam_posting_list = tam_posting_list

        self.idx = 0
        self.num_blocks = 0
        self.df = {}
        self.length = {}

        if not os.path.exists(self.path_save):

            os.makedirs(self.path_save)
            os.makedirs(self.path_save_temporal)

            print("Construyendo el Spimi...")
            self.BuildSpimi()

            shutil.rmtree(self.path_save_temporal)

            with open(os.path.join(self.path_save, "df"), "wb") as f:
                pickle.dump(self.df, f)

            with open(os.path.join(self.path_save, "length"), "wb") as f:
                pickle.dump(self.length, f)

            print("Listo!")

        else:

            print("Extrayendo SpimiBlocks desde Binario...")
            self.LoadSpimiBlocks()
            self.num_blocks = len(os.listdir(self.path_save)) - 2

            # self.__call__()
            # print(self.)

            print("Listo!")

    def BuildSpimi(self):

        n = 0
        save_parse_tokens = []

        is_full_block_but_not_posting_list = False

        while n < len(self.DocList):

            Block = BlockSpimi(self.tam_block, self.tam_posting_list)

            while not Block.is_full() and n < len(self.DocList):

                if not is_full_block_but_not_posting_list:
                    token_stream = preprocess(self.DocList[n])

                    token_and_docId = [[token, docId] for token, docId in
                                       zip(token_stream, [n] * len(token_stream))]

                    _, counts = np.unique(token_stream, return_counts=True)
                    self.length[n] = np.sqrt(np.sum(np.pow(counts, 2)))

                else:
                    token_and_docId = save_parse_tokens

                self.BuildBlock(Block, token_and_docId)

                if self.idx == 0:
                    n += 1
                    is_full_block_but_not_posting_list = False

                else:

                    if not Block.is_full():
                        save_parse_tokens = token_and_docId
                        is_full_block_but_not_posting_list = True
                    else:
                        is_full_block_but_not_posting_list = False

            if not Block.is_empty():
                Block.sort_dict_tokens()

                # Escribiendo el bloque en binario.
                with open(os.path.join(self.path_save, f"Block_{self.num_blocks}"), "wb") as f:
                    pickle.dump(Block, f)

                self.num_blocks += 1

        self.MergeBlocksSpimi()

    def BuildBlock(self, Block: BlockSpimi, token_and_docId):

        while not Block.is_full() and self.idx < len(token_and_docId):

            token = token_and_docId[self.idx][0]
            docId = token_and_docId[self.idx][1]

            if not Block.in_dict(token):
                Block.add_posting_list(token)

            posting_list: LinkedPostingList = Block.get_posting_list_by_token(token)

            if posting_list.is_full():
                posting_list.add_posting_linked()

            Block.insert_docId(token, docId)

            if token not in self.df:
                self.df[token] = []

            if docId not in self.df[token]:
                self.df[token].append(docId)

            self.idx += 1

        if len(token_and_docId) == self.idx:
            self.idx = 0

    def MergeBlocks(self, G1, G2, actual_block_write):

        G1size = G1[0]
        G2size = G2[0]

        block_merge = BlockSpimi(self.tam_block, self.tam_posting_list)
        tam_block_merge = 0

        idx1 = 0
        idx2 = 0

        isG1full: bool = True
        isG2full: bool = True

        block_g1 = None
        block_g2 = None

        while G1size <= G1[1] and G2size <= G2[1]:

            if isG1full:
                with open(os.path.join(self.path_save, f"Block_{G1size}"), "rb") as f:
                    block_g1 = pickle.load(f)

            if isG2full:
                with open(os.path.join(self.path_save, f"Block_{G2size}"), "rb") as f:
                    block_g2 = pickle.load(f)

            pl_g1 = block_g1.posting_list
            pl_g2 = block_g2.posting_list

            # Ya están ordenadas, se ordenan en el mismo BuildBlock
            tokens_g1 = list(pl_g1.keys())
            tokens_g2 = list(pl_g2.keys())

            while idx1 < len(tokens_g1) and idx2 < len(tokens_g2):

                if tokens_g1[idx1] > tokens_g2[idx2]:

                    token = tokens_g2[idx2]
                    linked = pl_g2[token]

                    actually_extract = linked.num_extract_actually()
                    size = linked.get_all_size()
                    espacio = self.tam_block - tam_block_merge
                    num_extract = min(size - actually_extract, espacio)

                    if num_extract != 0:
                        docs = linked.Extract_Posting_List_By_Index(num_extract)

                        tam_block_merge += num_extract

                        new_linked = LinkedPostingList(token, self.tam_posting_list, ListPointListInit=docs)
                        block_merge.ConcatenatePostingList(token, new_linked)

                    if not linked.CanExtract():
                        idx2 += 1
                elif tokens_g1[idx1] < tokens_g2[idx2]:

                    token = tokens_g1[idx1]
                    linked = pl_g1[token]

                    actually_extract = linked.num_extract_actually()
                    size = linked.get_all_size()
                    espacio = self.tam_block - tam_block_merge

                    num_extract = min(size - actually_extract, espacio)

                    if num_extract != 0:
                        docs = linked.Extract_Posting_List_By_Index(num_extract)
                        tam_block_merge += num_extract

                        new_linked = LinkedPostingList(token, self.tam_posting_list, ListPointListInit=docs)
                        block_merge.ConcatenatePostingList(token, new_linked)

                    if not linked.CanExtract():
                        idx1 += 1
                else:
                    # Caso esquina, si son iguales pues evitamos que se sobre escriba la solución anterior.

                    # Token compartido en ambos
                    token = tokens_g1[idx1]
                    linked1 = pl_g1[token]
                    linked2 = pl_g2[token]

                    actually_extract_1 = linked1.num_extract_actually()
                    actually_extract_2 = linked2.num_extract_actually()

                    espacio = self.tam_block - tam_block_merge
                    min_extract = min(actually_extract_1, actually_extract_2)

                    if min_extract == actually_extract_1:

                        num_extract = min(linked1.get_all_size() - min_extract, espacio)

                        if num_extract != 0:
                            docs1 = linked1.Extract_Posting_List_By_Index(num_extract)
                            tam_block_merge += num_extract

                            new_linked = LinkedPostingList(token, self.tam_posting_list, ListPointListInit=docs1)
                            block_merge.ConcatenatePostingList(token, new_linked)

                    else:

                        num_extract = min(linked2.get_all_size() - min_extract, espacio)

                        if num_extract != 0:
                            docs2 = linked2.Extract_Posting_List_By_Index(num_extract)
                            tam_block_merge += num_extract

                            new_linked = LinkedPostingList(token, self.tam_posting_list, ListPointListInit=docs2)
                            block_merge.ConcatenatePostingList(token, new_linked)

                    if min_extract == actually_extract_1 and not linked1.CanExtract():
                        idx1 += 1

                    if min_extract == actually_extract_2 and not linked2.CanExtract():
                        idx2 += 1

                if tam_block_merge == self.tam_block:
                    tam_block_merge = 0

                    with open(os.path.join(self.path_save_temporal, f"Block_{actual_block_write}"), "wb") as f:
                        pickle.dump(block_merge, f)

                    block_merge.clear()
                    actual_block_write += 1

            if idx1 == len(tokens_g1):
                idx1 = 0
                G1size += 1
                isG1full = True
                isG2full = False
            else:
                idx2 = 0
                G2size += 1
                isG1full = False
                isG2full = True

        actual_block_write = FinallyMerge(self, G1size, G1, block_g1, idx1, actual_block_write,
                                          block_merge, tam_block_merge)
        actual_block_write = FinallyMerge(self, G2size, G2, block_g2, idx2, actual_block_write,
                                          block_merge, tam_block_merge)

        if not block_merge.is_empty():
            with open(os.path.join(self.path_save_temporal, f"Block_{actual_block_write}"), "wb") as f:
                pickle.dump(block_merge, f)
            actual_block_write += 1

        return actual_block_write

    def MergeBlocksSpimi(self, nivel=1):

        groups = pow(2, nivel)
        n = self.num_blocks
        mid = groups // 2
        actual_block_write = 0

        count_before_merge = self.spimi_size()

        for i in range(0, n, groups):
            start1 = i
            end1 = min(i + mid - 1, n - 1)
            start2 = i + mid
            end2 = min(i + groups - 1, n - 1)

            G1 = (start1, end1)
            G2 = (start2, end2)
            actual_block_write = self.MergeBlocks(G1, G2, actual_block_write)

        if actual_block_write != n:
            raise ValueError("[ERROR] Cantidad erronea de bloques escritos!")

        copiar_contenido(self.path_save_temporal, self.path_save)

        count_after_merge = self.spimi_size()
        if count_before_merge != count_after_merge:
            raise ValueError("[ERROR] Cantidad erronea de elementos after merge!")

        print("q fue")
        if groups < n:
            self.MergeBlocksSpimi(nivel + 1)

    def LoadSpimiBlocks(self):
        write_df = self.path_save + "/df"

        with open(write_df, "rb") as f:
            load_df = pickle.load(f)
            self.df = load_df

        write_length = self.path_save + "/length"
        with open(write_length, "rb") as f:
            load_length = pickle.load(f)
            self.length = load_length

    def test(self):

        for i in range(self.num_blocks):
            path = os.path.join(self.path_save, f"Block_{i}")
            with open(path, "rb") as f:
                block: BlockSpimi = pickle.load(f)

            print(f"\n=== Bloque {i} ===")
            for tk, p_l in block.posting_list.items():
                print(f"Token: {tk}")
                print(f"Posting Linked List:")
                p_l()
                print("\n")

    def spimi_size(self):

        count = 0

        for i in range(self.num_blocks):
            path = os.path.join(self.path_save, f"Block_{i}")
            with open(path, "rb") as f:
                block: BlockSpimi = pickle.load(f)

            count += block.CountSizeBlock()

        return count

    def docListByWord(self, word, getdocsid=True):

        word = preprocess_word(word)

        min_pos = binary_search_block_index(self, word, find_left=True)
        max_pos = binary_search_block_index(self, word, find_left=False)
        result = []
        for pos_block in range(min_pos, max_pos + 1):
            with open(os.path.join(self.path_save, f"Block_{pos_block}"), "rb") as f:
                block: BlockSpimi = pickle.load(f)

            min_token = block.get_first_token()
            max_token = block.get_last_token()

            if min_token <= word <= max_token:
                if block.in_dict(word):
                    pl = block.get_posting_list_by_token(word)
                    pl_flatten = pl.flattenDocID() if getdocsid else pl.flattenDocTF()
                    result.extend(pl_flatten)

        return sorted(set(result)) if getdocsid else result

    def AND(self, query1: str, query2: str):
        tokens1 = preprocess(query1)
        tokens2 = preprocess(query2)

        docs1 = set()
        for token in tokens1:
            docs1.update(self.docListByWord(token))

        docs2 = set()
        for token in tokens2:
            docs2.update(self.docListByWord(token))

        return sorted(docs1 & docs2)

    def OR(self, query1: str, query2: str):
        tokens1 = preprocess(query1)
        tokens2 = preprocess(query2)

        docs = set()
        for token in tokens1 + tokens2:
            docs.update(self.docListByWord(token))

        return sorted(docs)

    def AND_NOT(self, query1: str, query2: str):
        tokens1 = preprocess(query1)
        tokens2 = preprocess(query2)

        docs1 = set()
        for token in tokens1:
            docs1.update(self.docListByWord(token))

        docs2 = set()
        for token in tokens2:
            docs2.update(self.docListByWord(token))

        return sorted(docs1 - docs2)

    def query_knn(self, query, k=5):

        Querytf = count_tokens(preprocess(query))
        Scores = defaultdict(float)
        total_docs = len(self.length)

        print(Querytf)
        for idx, (wordQ, tf) in enumerate(Querytf):
            tfQ = 1 + np.log10(tf)
            DocTFDict = self.docListByWord(wordQ, getdocsid=False)
            if DocTFDict:
                df = len(self.df[wordQ])
                idf = np.log10(total_docs / df)

                for DocTF in DocTFDict:
                    DocId = DocTF.docId
                    tfD = DocTF.tf
                    tfidf_product = (idf ** 2) * tfQ * tfD
                    Scores[DocId] += tfidf_product
        for DocId in Scores.keys():
            Scores[DocId] /= self.length[DocId]

        result = sorted(Scores.items(), key=lambda tup: tup[1], reverse=True)
        result = [(r_tuple[0] + 1, r_tuple[1]) for r_tuple in result[:k]]
        return result[:k]


if __name__ == "__main__":
    csv = pd.read_csv("C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/dataset/spotify_songs_10.csv")

    lyrics2 = list(csv["lyrics"])


    lyrics = [
        "love me love you love again",
        "baby baby I love you baby",
        "yeah yeah yeah love yeah yeah",
        "no no no love no no no",
        "fire fire burning baby love",
        "cry baby cry no one knows",
        "run baby run fast love run",
        "love yeah dance yeah love yeah",
        "baby fire dance fire fire baby",
        "cry cry love cry yeah love",
        "dance baby love dance all night",
        "fire yeah run fire no run",
        "yeah baby yeah yeah yeah love",
        "run love run baby run again",
        "no more love no more pain",
        "cry out loud cry cry baby",
        "fire in love fire in heart",
        "love baby cry baby love fire",
        "yeah dance baby yeah dance yeah",
        "no love no fire no cry"
    ]


    print("Construccion SPIMI:")
    # Crear el índice

    path_save = "./SpimiBlocks2"
    spimi = SpimiIndex(lyrics2, path_save, inicializar_hp=True)
    print("Construido...")
    knn = spimi.query_knn('dance baby love dance all night', 10)
    print(knn)

