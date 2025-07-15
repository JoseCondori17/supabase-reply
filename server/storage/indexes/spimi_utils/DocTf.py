class DocTf:
    def __init__(self, token, docId, tf=1):
        self.token = token
        self.tf = tf
        self.docId = docId

    def AddOneTf(self):
        self.tf += 1

    def AddTf(self, tf):
        self.tf += tf

    def is_same_token(self, token):
        return self.token == token

    def is_same_docId(self, docId):
        return self.docId == docId

    def get_tf(self):
        return self.tf

    def __call__(self):
        print(f"DocId: {self.docId} con tf: {self.tf}")