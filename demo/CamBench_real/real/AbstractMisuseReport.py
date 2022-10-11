from matcher.PathMatcher import PathMatcher
from matcher.ApiMatcher import ApiMatcher
from matcher.LineMatcher import LineMatcher
from matcher import AbstractMatcher


class AbstractMisuseReport():

    def misuse_name(*args) -> str:
        pass

    def get_file_path(self) -> str:
        pass

    def get_method(self) -> str:
        pass

    def get_method_name(self) -> str:
        pass

    def get_method_parameter_types(self) -> list:
        pass

    def get_method_return_type(self) -> str:
        pass

    def get_line(self) -> int:
        pass

    def get_api(self) -> str:
        pass

    def get_name(self) -> str:
        pass

    def get_description(self) -> str:
        pass

    def check_if_matches_label(self, label) -> bool:
        matcher = [
            PathMatcher(label, self),
            ApiMatcher(label, self), 
            LineMatcher(label, self)]
        
        matches = list()
        not_matches = list()
        for m in matcher:
            result = m.matches()
            if result == AbstractMatcher.NOT_FOUND:
                continue
            if result == AbstractMatcher.NOT_MATCHES:
                not_matches.append(m.matcher_name())
            else:
                matches.append(m.matcher_name())

        label.add_matching_error(self.misuse_name(), self, matches)
        return True

    def __str__(self) -> str:
        return f"FilePath: {self.get_file_path()}\nMethod: {self.get_method_name()}\nLine: {self.get_line()}"

    def __repr__(self) -> str:
        return self.__str__()