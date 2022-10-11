from AbstractMisuseReport import AbstractMisuseReport
from tools.CryptoGuard import CryptoGuard


class CryptoGuardXMLMisuseReport(AbstractMisuseReport):
    
    def misuse_name(*args):
        return CryptoGuard.TOOL_NAME

    def __init__(self, cryptoguard_error):
        self.cryptoguard_error = cryptoguard_error

    def get_file_path(self) -> str:
        return "/".join(self.cryptoguard_error.find('BugLocations').find('Location').find('SourceFile').text.split('/')[1:])
        #return self.crypto_analysis_error['locations']['physicalLocation']['fileLocation']['uri']

    def get_method(self) -> str:
        pass 

    def get_method_name(self) -> str:
        return self.cryptoguard_error.find('Methods').find('Method').text

    def get_line(self) -> int:
        start_line = self.cryptoguard_error.find('BugLocations').find('Location').find('StartLine')
        if start_line == None:
            return None
        return int(start_line.text)

    def get_api(self) -> str:
        pass

    def get_name(self) -> str:
        return self.cryptoguard_error.find("BugCode").text

    def get_description(self) -> str:
        return self.cryptoguard_error.find("BugMessage")

    def check_if_match_label(self, label) -> bool:
        pass
