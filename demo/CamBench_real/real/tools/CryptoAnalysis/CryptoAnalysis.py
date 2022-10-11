import json
import os
import subprocess
from AbstractAnalysis import AbstractAnalysis
from tools.CryptoAnalysis.CryptoAnalysisSARIFMisuseReport import CryptoAnalysisSARIFMisuseReport

TOOL_NAME="CryptoAnalysis"

class CryptoAnalysis(AbstractAnalysis):
    
    def tool_name(*args):
        return TOOL_NAME

    def __init__(self, project):
        self.project = project
        self.reported_misuses = None
        self.init_SARIF()


    def parse_SARIF(self):
        with open(self.report_file_path, "r") as report_file:
            report = json.loads(report_file.read())
            if "runs" in report and "results" in report["runs"]:
                return [CryptoAnalysisSARIFMisuseReport(error) for error in report["runs"]["results"]]

    def init_SARIF(self):
        # create folder for reports
        self.report_folder_path = os.path.join(self.project.repository_path, "CryptoAnalysis")
        self.report_file_path = os.path.join(self.report_folder_path, "CryptoAnalysis-Report.json")
        if not os.path.exists(self.report_folder_path):
            os.mkdir(self.report_folder_path)

        # retrieve paths to execute the tool
        cryptoanalysis_folder = self.get_path_for_tool("CryptoAnalysis")
        print(cryptoanalysis_folder)
        self.tool = os.path.join(cryptoanalysis_folder, "CryptoAnalysisSUBS", "SUBS.jar")
        self.rules = os.path.join(cryptoanalysis_folder, "CryptoAnalysisSUBS", "JavaCryptographicArchitecture_BET")

        self.cmd = f'java -Xmx5G -Xss100M -cp "{self.tool}" crypto.HeadlessCryptoScanner --rulesDir "{self.rules}" --appPath "{self.project.project_path}" --reportPath "{self.report_folder_path}" --subsequenterrordetection --reportFormat "sarif"'
        self.parse = self.parse_SARIF


    def execute(self):
        try:
            print(self.cmd)
            subprocess.check_output(self.cmd, shell=True).decode("utf-8")
            self.reported_misuses = self.parse()
        except subprocess.CalledProcessError as cpe:
            print(cpe.stderr)
        except subprocess.TimeoutExpired:
            print("CryptoAnalysis Timeout")

    def get_reported_misuses(self):
        return self.reported_misuses

    