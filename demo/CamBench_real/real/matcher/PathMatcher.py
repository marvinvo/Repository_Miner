from matcher import AbstractMatcher


class PathMatcher(AbstractMatcher.AbstractMatcher):

    def matcher_name(*args):
        return "Path"

    def matches(self):
        label_path = self.label.get_file_path()
        misuse_path = self.misuse.get_file_path()

        if not label_path or not misuse_path:
            return AbstractMatcher.NOT_FOUND

        misuse_path = misuse_path.replace(".java", "").replace(".class", "")
        if ".jar" in misuse_path:
            misuse_path = misuse_path.split(".jar")[-1]

        
        if misuse_path in label_path:
            return AbstractMatcher.MATCHES

        return AbstractMatcher.NOT_MATCHES