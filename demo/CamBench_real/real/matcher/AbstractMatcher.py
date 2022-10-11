MATCHES=1
NOT_FOUND=0
NOT_MATCHES=-1

class AbstractMatcher():

    def matcher_name(*args) -> str:
        pass

    def __init__(self, label, misuse):
        self.label = label
        self.misuse = misuse


    def matches(self) -> int:
        pass
