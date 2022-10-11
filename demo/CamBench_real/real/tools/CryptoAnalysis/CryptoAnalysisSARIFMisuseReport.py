from AbstractMisuseReport import AbstractMisuseReport
from tools.CryptoAnalysis import CryptoAnalysis


class CryptoAnalysisSARIFMisuseReport(AbstractMisuseReport):
    
    def misuse_name(*args):
        return CryptoAnalysis.TOOL_NAME

    def __init__(self, crypto_analysis_error):
        self.crypto_analysis_error = crypto_analysis_error

    def get_file_path(self) -> str:
        return self.crypto_analysis_error['locations']['physicalLocation']['fileLocation']['uri']

    def get_method_name(self) -> str:
        return self.crypto_analysis_error['locations']['fullyQualifiedLogicalName'].split("::")[-1]

    def get_line(self) -> int:
        return int(self.crypto_analysis_error['locations']['physicalLocation']['region']['startLine'])

    def get_api(self) -> str:
        return self.crypto_analysis_error['message']['richText'].split(' ')[-1][:-1]

    def get_name(self) -> str:
        return self.crypto_analysis_error['message']['richText'].split(' ')[0]

    def get_description(self) -> str:
        return self.crypto_analysis_error['message']['text']

    def check_if_match_label(self, label) -> bool:
        pass
