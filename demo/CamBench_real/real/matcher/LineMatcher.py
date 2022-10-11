
from matcher import AbstractMatcher


class LineMatcher(AbstractMatcher.AbstractMatcher):

    def matcher_name(*args):
        return "Line"

    def matches(self):
        if not self.label.get_line() or not self.misuse.get_line():
            return AbstractMatcher.NOT_FOUND

        
        if self.label.get_line()==self.misuse.get_line():
            return AbstractMatcher.MATCHES

        return AbstractMatcher.NOT_MATCHES