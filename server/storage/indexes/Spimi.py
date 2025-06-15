import numpy as np
import os
import math

from server.types.text import preprocess


class BlockSpimi:

    # tam_block: # de docId's en total que tiene cada bloque.
    # tam_posting_list: # de docId's anclados a un posting list de un token.

    def __init__(self, tam_block=10, tam_posting_list=5):
        self.tam_block = tam_block
        self.tam_posting_list = tam_posting_list
        self.actual_size_block = 0
        self.posting_list = {}

    def get_posting_list_by_token(self, token):
        return self.posting_list[token]

    def UpdateLinkedList(self, token, LinkedList):
        self.posting_list[token] = LinkedList

    def insert_docId(self, token, docId):
        self.posting_list[token].insert_docId(docId)
        self.actual_size_block += 1

    def is_full(self):
        return self.tam_block == self.actual_size_block

    def in_dict(self, key):
        return key in self.posting_list

    def add_posting_list(self, token):
        self.posting_list[token] = LinkedPostingList(token, self.tam_posting_list)

    def sort_dict_tokens(self):
        # dict.items() retorna una lista de tuplas del diccionario.
        self.posting_list = dict(sorted(self.posting_list.items()))

    def is_empty(self):
        return len(self.posting_list)

    def ConcatenatePostingList(self, token, posting_list):
        self.posting_list[token].ConcatenateLinkedList(posting_list)


class LinkedPostingList:

    def __init__(self, name_token, tam_posting_list=5, ListPointListInit=None):
        self.tam_posting_list = tam_posting_list
        self.ListPostingList = [[]] if ListPointListInit is None else ListPointListInit
        self.actual_pos_extract = 0
        self.name_token = name_token

    def insert_docId(self, DocId):
        self.ListPostingList[-1].append(DocId)

    def last_posting_list(self):
        return self.ListPostingList[-1]

    # Booleano para controlar si es que se pudo crear un bloque.
    def add_posting_linked(self):
        self.ListPostingList.append([])

    def is_full(self):
        return len(self.ListPostingList[-1]) == self.tam_posting_list

    def get_list_block(self):
        return self.ListPostingList

    def get_all_size(self):

        # más de un posting list enlazado
        if len(self.ListPostingList) >= 2:
            canti = self.tam_posting_list * (len(self.ListPostingList) - 1)
            return canti + len(self.ListPostingList[-1])

        # solo un posting list
        else:
            return len(self.ListPostingList[-1])

    # Extrae en el rango [idx, n].

    # extrae num_extract DocId's de los posting list anclados al token
    # La posición actual de la extracción se guarda en self.actual_pos_extract
    def Extract_Posting_List_By_Index(self, num_extract):

        idx_pl = self.actual_pos_extract // self.tam_posting_list
        actual_posi = self.actual_pos_extract % self.tam_posting_list

        LinkedListIdDocs = []
        ListIdDocs = []

        actual_num_extract = 0

        while actual_num_extract < num_extract:

            if idx_pl >= len(self.ListPostingList):
                raise ValueError("No debería entrar acá.")

            posting_list = self.ListPostingList[idx_pl]
            for pos_doc in range(actual_posi, len(posting_list)):

                if actual_num_extract >= num_extract:
                    break

                ListIdDocs.append(posting_list[pos_doc])

                if len(ListIdDocs) == self.tam_posting_list:
                    LinkedListIdDocs.append(ListIdDocs)
                    ListIdDocs = []

                self.actual_pos_extract += 1
                actual_num_extract += 1

            idx_pl += 1
            actual_posi = 0

        if ListIdDocs:
            LinkedListIdDocs.append(ListIdDocs)

        return LinkedListIdDocs

    def num_extract_actually(self):
        return self.actual_pos_extract + 1

    def CanExtract(self):
        return self.actual_pos_extract < self.get_all_size()

    def ConcatenateLinkedList(self, LinkedList):
        if not self.ListPostingList:
            self.ListPostingList = [block[:] for block in LinkedList]
            return

        for block in LinkedList:
            for doc_id in block:
                if self.is_full():
                    self.ListPostingList.append([])
                self.ListPostingList[-1].append(doc_id)


class SpimiIndex:

    def __init__(self, DocList, tam_block=10, tam_posting_list=5):

        self.DocList = DocList
        self.tam_block = tam_block
        self.tam_posting_list = tam_posting_list

        # Lista de bloques creados
        self.ListBlock = []

        # Se va a encargar de controlar la posición actual del token_stream que se quedo un Doc
        # cuando se lleno un bloque.
        self.idx = 0

        self.BuildSpimi()

    def BuildSpimi(self):

        n = 0

        # Para evitar el recálculo de los tokens cuando se llena un bloque
        save_parse_tokens = []

        # mi profe de software estaría orgulloso
        is_full_block_but_not_posting_list = False

        while n < len(self.DocList):

            Block = BlockSpimi(self.tam_block, self.tam_posting_list)

            while not Block.is_full() and n < len(self.DocList):

                if not is_full_block_but_not_posting_list:
                    token_stream = preprocess(self.DocList[n])

                    # Todos esos tokens le pertenecen al doc número n.
                    token_and_docId = [[token, docId] for token, docId in
                                       zip(token_stream, [n] * len(token_stream))]
                else:
                    token_and_docId = save_parse_tokens

                self.BuildBlock(Block, token_and_docId)

                # Significa que acabo de leer el documento actual o no tenía contenido.
                if self.idx == 0:
                    n += 1
                    is_full_block_but_not_posting_list = False

                # Esto indica que aún no se acabo de leer el documento pero se lleno el bloque.
                else:

                    # Caso esquinaaaa
                    if not Block.is_full():
                        save_parse_tokens = token_and_docId
                        is_full_block_but_not_posting_list = True
                    else:
                        is_full_block_but_not_posting_list = False

            # Posible caso esquina, entra un bloque vacio.
            if not Block.is_empty():
                self.ListBlock.append(Block)

        # Algoritmo de merge de los bloques...
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

            # posting_list.insert_docId(docId)

            # Para que se llene el size del bloque, igualmente hará las operaciones de los
            # postings del token.
            Block.insert_docId(token, docId)

            self.idx += 1

        # Posible caso esquina, si es que manejo ambos por separado.
        if len(token_and_docId) == self.idx and Block.is_full():
            self.idx = 0
            Block.sort_dict_tokens()

        # Para que avance en el siguiente registro desde esta posición.
        elif len(token_and_docId) == self.idx:
            self.idx = 0

        else:
            Block.sort_dict_tokens()

    def MergeBlocks(self, G1, G2):

        G1size = 0
        G2size = 0

        GMerge = []

        block_merge = BlockSpimi(self.tam_block, self.tam_posting_list)
        tam_block_merge = 0

        idx1 = 0
        idx2 = 0

        # Esto para controlar el orden de los bloques.
        while G1size < len(G1) and G2size < len(G2):

            block_g1: BlockSpimi = G1[G1size]
            block_g2: BlockSpimi = G2[G2size]

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

                    tam_block_merge += num_extract
                    docs = linked.Extract_Posting_List_By_Index(num_extract)
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

                    tam_block_merge += num_extract
                    docs = linked.Extract_Posting_List_By_Index(num_extract)
                    new_linked = LinkedPostingList(token, self.tam_posting_list, ListPointListInit=docs)
                    block_merge.ConcatenatePostingList(token, new_linked)

                    if not linked.CanExtract():
                        idx1 += 1

                # Caso esquina, si son iguales pues evitamos que se sobre escriba la solución anterior.
                else:

                    # Token compartido en ambos
                    token = tokens_g1[idx1]
                    linked1 = pl_g1[token]
                    linked2 = pl_g2[token]

                    actually_extract_1 = linked1.num_extract_actually()
                    actually_extract_2 = linked2.num_extract_actually()
                    size_total = linked1.get_all_size() + linked2.get_all_size()

                    espacio = self.tam_block - tam_block_merge

                    min_extract = min(actually_extract_1, actually_extract_2)
                    num_extract = min(size_total - min_extract, espacio)

                    tam_block_merge += num_extract

                    if min_extract == actually_extract_1:

                        docs1 = linked1.Extract_Posting_List_By_Index(num_extract)
                        new_linked = LinkedPostingList(token, self.tam_posting_list, ListPointListInit=docs1)
                        block_merge.ConcatenatePostingList(token, new_linked)

                    else:

                        docs2 = linked2.Extract_Posting_List_By_Index(num_extract)
                        new_linked = LinkedPostingList(token, self.tam_posting_list, ListPointListInit=docs2)
                        block_merge.ConcatenatePostingList(token, new_linked)

                    if min_extract == actually_extract_1 and not linked1.CanExtract():
                        idx1 += 1
                    if min_extract == actually_extract_2 and not linked2.CanExtract():
                        idx2 += 1

                if tam_block_merge == self.tam_block:
                    tam_block_merge = 0
                    GMerge.append(block_merge)
                    block_merge = BlockSpimi(self.tam_block, self.tam_posting_list)

            if idx1 == len(tokens_g1):
                idx1 = 0
                G1size += 1
            else:
                idx2 = 0
                G2size += 1

        if not block_merge.is_empty():
            GMerge.append(block_merge)

        for i in range(G1size, len(G1)):
            GMerge.append(G1[i])
        for i in range(G2size, len(G2)):
            GMerge.append(G2[i])

        return GMerge

    def MergeBlocksSpimi(self, nivel=1):

        groups = pow(2, nivel)
        n = len(self.ListBlock)

        for i in range(0, n, groups):
            mid = groups // 2
            G1 = self.ListBlock[i: i + mid]
            G2 = self.ListBlock[i + mid: min(i + groups, n)]

            GMerge = self.MergeBlocks(G1, G2)

            # Puede que este mal esto...
            self.ListBlock[i: i + len(G1) + len(G2)] = GMerge[:]

        if groups * 2 < n:
            self.MergeBlocksSpimi(nivel + 1)
