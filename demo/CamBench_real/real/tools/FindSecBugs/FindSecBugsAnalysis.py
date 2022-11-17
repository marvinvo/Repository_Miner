import json
import os
import pathlib
import subprocess
import xml.etree.ElementTree as ET
from AbstractAnalysis import AbstractAnalysis
from tools.FindSecBugs.FindSecBugsXMLMisuseReport import FindSecBugsXMLMisuseReport

TOOL_NAME="SpotBugs"

class FindSecBugs(AbstractAnalysis):

    __mapper_args__ = {'polymorphic_identity': 'spotbugs'}
    
    def __init__(self, project):
        self.tool_name = "SpotBugs"
        self.project = project
        self.reported_misuses = None
        self.init_XML()

    def move_result_to_result_folder(self):
        for root, dirs, files in os.walk(pathlib.Path().resolve()):
            for file in files:
                if "spotbugs" in file.lower() and ".xml" in file.lower():
                    origin = os.path.join(pathlib.Path().resolve(), file)
                    self.report_file_path = os.path.join(self.report_folder_path, file)
                    os.rename(origin, self.report_file_path)
                    

    def parse_XML(self):
        root = ET.parse(self.report_file_path).getroot()
        return [FindSecBugsXMLMisuseReport(error) for error in root.iter('BugInstance')]

    def init_XML(self):
        # create folder for reports
        self.report_folder_path = os.path.join(self.project.repository_path, self.tool_name)
        #self.report_file_path = os.path.join(self.report_folder_path, "CryptoAnalysis-Report.json")
        if not os.path.exists(self.report_folder_path):
            os.mkdir(self.report_folder_path)

        # retrieve paths to execute the tool
        self.spotbugs_folder = self.get_tool_directory(self.tool_name)
        self.tool = self.get_tool_path(self.tool_name)
        print(self.tool)

        # get path of the FindSecBugs plugin
        self.findsecbugs_folder = self.get_tool_directory("FindSecBugs")
        self.findsecbugs_plugin = os.listdir(self.findsecbugs_folder)[0]
        self.findsecbugs_plugin_path = os.path.join(self.findsecbugs_folder, self.findsecbugs_plugin)

        self.report_file_path = f'{self.report_folder_path}/spotbugs.xml'
        self.cmd = f'java -jar {self.tool} -textui -pluginList "{self.findsecbugs_plugin_path}" -html:default.xsl={self.report_folder_path}/spotbugs.html -xml={self.report_file_path} "{self.project.project_path}"'

        self.parse = self.parse_XML


    def execute(self):
        print("====== Execute SpotBugs/FindSecBugs Analysis ======")
        self.finished_without_exception = False
        try:
            subprocess.check_output(self.cmd, shell=True).decode("utf-8")
            self.finished_without_exception = False
            #self.move_result_to_result_folder()
            self.reported_misuses = self.parse()
        except subprocess.CalledProcessError as cpe:
            print(cpe.stderr)
        except subprocess.TimeoutExpired:
            print("SpotBugs Timeout")

    def get_reported_misuses(self):
        self.misuses = self.reported_misuses
        return self.reported_misuses