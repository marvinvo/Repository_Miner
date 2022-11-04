from AbstractMisuseReport import AbstractMisuseReport
from tools.CryptoGuard import CryptoGuardAnalysis


class CryptoGuardXMLMisuseReport(AbstractMisuseReport):

    __mapper_args__ = {'polymorphic_identity': 'cryptoguard'}
    
    def __init__(self, cryptoguard_error):
        self.cryptoguard_error = cryptoguard_error

        self.file_path = "/".join(self.cryptoguard_error.find('BugLocations').find('Location').find('SourceFile').text.split('/')[1:])
        self.method_name = self.cryptoguard_error.find('Methods').find('Method').text
        self.method_parameter_types = None
        _start_line = self.cryptoguard_error.find('BugLocations').find('Location').find('StartLine')
        self.line = None if _start_line==None else _start_line.text
        self.api = None
        self.name = self.cryptoguard_error.find("BugCode").text
        self.description = self.cryptoguard_error.find("BugMessage").text

        print(self.__repr__())