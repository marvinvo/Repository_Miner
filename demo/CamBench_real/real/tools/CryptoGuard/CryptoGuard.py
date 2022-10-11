import json
import os
import pathlib
import subprocess
from AbstractAnalysis import AbstractAnalysis
import xml.etree.ElementTree as ET

from tools.CryptoGuard.CryptoGuardXMLMisuseReport import CryptoGuardXMLMisuseReport

TOOL_NAME="CryptoGuard"

class CryptoGuard(AbstractAnalysis):

    def tool_name(*args):
        return TOOL_NAME
    
    def __init__(self, project):
        self.project = project
        self.reported_misuses = None
        self.init_XML()

    def move_result_to_result_folder(self):
        for root, dirs, files in os.walk(pathlib.Path().resolve()):
            for file in files:
                if "cryptoguard" in file.lower() and ".xml" in file.lower():
                    origin = os.path.join(pathlib.Path().resolve(), file)
                    self.report_file_path = os.path.join(self.report_folder_path, file)
                    os.rename(origin, self.report_file_path)
                    

    def parse_XML(self):
        root = ET.parse(self.report_file_path).getroot()
        return [CryptoGuardXMLMisuseReport(error) for error in root.iter('BugInstance')]

    def init_XML(self):
        # create folder for reports
        self.report_folder_path = os.path.join(self.project.repository_path, "CryptoGuard")
        #self.report_file_path = os.path.join(self.report_folder_path, "CryptoAnalysis-Report.json")
        if not os.path.exists(self.report_folder_path):
            os.mkdir(self.report_folder_path)

        # retrieve paths to execute the tool
        self.cryptoguard_folder = self.get_path_for_tool("CryptoGuard")
        self.tool = os.path.join(self.cryptoguard_folder, "cryptoguard.jar")
        print(self.tool)

        self.cmd = f'java -jar {self.tool} -in jar -s "{self.project.project_path}" -m SX'

        self.parse = self.parse_XML


    def execute(self):
        try:
            subprocess.check_output(self.cmd, shell=True).decode("utf-8")
            self.move_result_to_result_folder()
            self.reported_misuses = self.parse()
        except subprocess.CalledProcessError as cpe:
            print(cpe.stderr)
        except subprocess.TimeoutExpired:
            print("CryptoAnalysis Timeout")

    def get_reported_misuses(self):
        return self.reported_misuses

    