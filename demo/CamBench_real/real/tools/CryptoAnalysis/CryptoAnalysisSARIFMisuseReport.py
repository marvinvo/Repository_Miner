from AbstractMisuseReport import AbstractMisuseReport
from tools.CryptoAnalysis import CryptoAnalysisAnalysis


class CryptoAnalysisSARIFMisuseReport(AbstractMisuseReport):

    __mapper_args__ = {'polymorphic_identity': 'cryptoanalysis'}
    
    def misuse_name(*args):
        return CryptoAnalysisAnalysis.TOOL_NAME

    def __init__(self, crypto_analysis_error):
        self.crypto_analysis_error = crypto_analysis_error

        self.file_path = self.crypto_analysis_error['locations'][0]['physicalLocation']['fileLocation']['uri']
        self.method_name = self.crypto_analysis_error['locations'][0]['fullyQualifiedLogicalName'].split("::")[-1]
        self.method_parameter_types = None
        self.line = int(self.crypto_analysis_error['locations'][0]['physicalLocation']['region']['startLine'])
        self.api = self.crypto_analysis_error['message']['richText'].split(' ')[-1][:-1]
        self.name = self.crypto_analysis_error['message']['richText'].split(' ')[0]
        self.description = self.crypto_analysis_error['message']['text']

        print(self.__repr__())

