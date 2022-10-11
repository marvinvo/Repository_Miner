from matcher import AbstractMatcher

class ApiMatcher(AbstractMatcher.AbstractMatcher):

    def matcher_name(*args):
        return "Api"

    def matches(self):
        if not self.label.get_api() or not self.misuse.get_api():
            return AbstractMatcher.NOT_FOUND

        if self.label.get_api() == self.misuse.get_api():
            return AbstractMatcher.MATCHES

        return AbstractMatcher.NOT_MATCHES