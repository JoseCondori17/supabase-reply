import itertools
from .DocTf import DocTf


class LinkedPostingList:

    def __init__(self, name_token, tam_posting_list=5, ListPointListInit=None):
        self.tam_posting_list = tam_posting_list
        self.ListPostingList = [[]] if ListPointListInit is None else ListPointListInit
        self.actual_pos_extract = 0
        self.name_token = name_token

        # Para mantener la posición
        self.dict = {}

    def in_postinglist_and_push(self, DocId):

        if DocId in self.dict:
            idx_pl, idx_block = self.dict[DocId]
            DocSave = self.ListPostingList[idx_pl][idx_block]
            DocSave.AddOneTf()
            return True

        return False

    def flattenDocID(self):
        flatten = list(itertools.chain.from_iterable(self.ListPostingList))
        listDocId = [doctf.docId for doctf in flatten]
        return listDocId

    def flattenDocTF(self):
        return list(itertools.chain.from_iterable(self.ListPostingList))

    def in_postinglist_and_Addtf(self, DocId, tf):

        if DocId in self.dict:
            idx_pl, idx_block = self.dict[DocId]
            DocSave = self.ListPostingList[idx_pl][idx_block]
            DocSave.AddTf(tf)

            return True

        return False

    def insert_docId(self, DocId):

        if not self.in_postinglist_and_push(DocId):
            DocSave = DocTf(self.name_token, DocId, tf=1)
            self.ListPostingList[-1].append(DocSave)
            self.dict[DocId] = [len(self.ListPostingList) - 1, len(self.ListPostingList[-1]) - 1]

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

        canti = 0
        for p_l in self.ListPostingList:
            for DocSave in p_l:
                canti += DocSave.get_tf()

        return canti

    def push_doctf(self, doctf: DocTf):
        self.ListPostingList.append(doctf)

    def Extract_Posting_List_By_Index(self, num_extract):

        idx_pl = 0
        actual_posi = 0
        copy_ap = self.actual_pos_extract

        for idx, p_l in enumerate(self.ListPostingList):
            salir = False

            for doc_idx, DocSave in enumerate(p_l):
                if copy_ap - DocSave.get_tf() > 0:
                    copy_ap -= DocSave.get_tf()
                else:
                    idx_pl = idx
                    actual_posi = doc_idx
                    salir = True
                    break

            if salir:
                break

        LinkedListIdDocs = []
        ListIdDocs = []

        DocSave = self.ListPostingList[idx_pl][actual_posi]
        if DocSave.get_tf() - copy_ap == 0:
            actual_posi += 1
            copy_ap = 0
            if actual_posi == self.tam_posting_list:
                actual_posi = 0
                idx_pl += 1

        while num_extract != 0:

            if idx_pl >= len(self.ListPostingList) and actual_posi >= self.tam_posting_list:
                raise ValueError("No debería entrar acá.")

            DocSave: DocTf = self.ListPostingList[idx_pl][actual_posi]
            copy_extract = num_extract
            ExtractDoc = DocSave.get_tf() - copy_ap

            if len(ListIdDocs) == self.tam_posting_list:
                LinkedListIdDocs.append(ListIdDocs)
                ListIdDocs = []

            if ExtractDoc >= copy_extract:
                PushDoc = DocTf(DocSave.token, DocSave.docId, copy_extract)
                self.actual_pos_extract += copy_extract
                num_extract = 0
            else:
                PushDoc = DocTf(DocSave.token, DocSave.docId, ExtractDoc)
                self.actual_pos_extract += ExtractDoc
                num_extract -= ExtractDoc

            ListIdDocs.append(PushDoc)
            actual_posi += 1

            if actual_posi == self.tam_posting_list:
                actual_posi = 0
                idx_pl += 1

            copy_ap = 0

        if ListIdDocs:
            LinkedListIdDocs.append(ListIdDocs)

        return LinkedListIdDocs

    def num_extract_actually(self):
        return self.actual_pos_extract

    def CanExtract(self):
        return self.actual_pos_extract < self.get_all_size()

    def ConcatenateLinkedList(self, LinkedList):

        if not self.ListPostingList:
            self.ListPostingList = LinkedList.ListPostingList
            self.dict = {}
            for i, p_l in enumerate(self.ListPostingList):
                for j, DocSave in enumerate(p_l):
                    self.dict[DocSave.docId] = [i, j]
            return

        for block in LinkedList.ListPostingList:
            for DocSave in block:

                if self.is_full():
                    self.ListPostingList.append([])

                if not self.in_postinglist_and_Addtf(DocSave.docId, DocSave.get_tf()):
                    self.ListPostingList[-1].append(DocSave)
                    self.dict[DocSave.docId] = [len(self.ListPostingList) - 1,
                                                len(self.ListPostingList[-1]) - 1]

    def __call__(self):
        for pl in self.ListPostingList:
            for doc in pl:
                doc()
