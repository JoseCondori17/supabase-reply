from .LinkedPostingList import LinkedPostingList
import os
import pickle
import shutil


class BlockSpimi:

    # tam_block: # de docId's en total que tiene cada bloque.
    # tam_posting_list: # de docId's anclados a un posting list de un token.

    def __init__(self, tam_block=10, tam_posting_list=5):
        self.tam_block = tam_block
        self.tam_posting_list = tam_posting_list
        self.actual_size_block = 0
        self.posting_list = {}

    def CountSizeBlock(self):
        canti = 0

        for token in self.posting_list.keys():
            canti += self.posting_list[token].get_all_size()

        return canti

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

    def get_first_token(self):
        return next(iter(self.posting_list))

    def get_last_token(self):
        return next(reversed(self.posting_list))

    def is_empty(self):
        return len(self.posting_list) == 0

    def ConcatenatePostingList(self, token, posting_list):

        if not self.in_dict(token):
            self.posting_list[token] = LinkedPostingList(token, tam_posting_list=self.tam_posting_list)

        self.posting_list[token].ConcatenateLinkedList(posting_list)

    def __call__(self):
        for token_key in self.posting_list.keys():
            print("Token:")
            self.posting_list[token_key]()

    def clear(self):
        self.posting_list.clear()
        self.actual_size_block = 0


def FinallyMerge(self, Gsize, G, block_g, idx, actual_block_write, block_merge, tam_block_merge):
    is_first_loop: bool = True
    while Gsize <= G[1]:

        if block_g is None or not is_first_loop:
            with open(os.path.join(self.path_save, f"Block_{Gsize}"), "rb") as f:
                block_g = pickle.load(f)

        p1_g = block_g.posting_list

        tokens_g = list(p1_g.keys())[idx:]

        for token in tokens_g:
            linked = p1_g[token]

            while linked.CanExtract():
                espacio = self.tam_block - tam_block_merge
                num_extract = min(linked.get_all_size() - linked.num_extract_actually(), espacio)

                if num_extract == 0:
                    tam_block_merge = 0

                    with open(os.path.join(self.path_save_temporal, f"Block_{actual_block_write}"), "wb") as f:
                        pickle.dump(block_merge, f)

                    block_merge.clear()
                    actual_block_write += 1
                    continue

                docs = linked.Extract_Posting_List_By_Index(num_extract)
                new_linked = LinkedPostingList(token, self.tam_posting_list, ListPointListInit=docs)
                block_merge.ConcatenatePostingList(token, new_linked)
                tam_block_merge += num_extract

        idx = 0
        Gsize += 1
        is_first_loop = False

    return actual_block_write


def binary_search_block_index(self, query, find_left=True):
    left = 0
    right = self.num_blocks - 1

    while left <= right:

        mid = (left + right) // 2

        with open(os.path.join(self.path_save, f"Block_{mid}"), "rb") as f:
            block: BlockSpimi = pickle.load(f)

        token = block.get_last_token() if find_left else block.get_first_token()

        if (find_left and query > token) or (not find_left and query < token):
            if find_left:
                left = mid + 1
            else:
                right = mid - 1
        else:
            if find_left:
                right = mid - 1
            else:
                left = mid + 1

    return left


def copiar_contenido(origen, destino):

    for item in os.listdir(origen):
        ruta_origen = os.path.join(origen, item)
        ruta_destino = os.path.join(destino, item)

        if os.path.isdir(ruta_origen):
            shutil.copytree(ruta_origen, ruta_destino, dirs_exist_ok=True)
        else:
            shutil.copy2(ruta_origen, ruta_destino)
