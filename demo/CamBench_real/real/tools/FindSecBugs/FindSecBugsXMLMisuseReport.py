from AbstractMisuseReport import AbstractMisuseReport
import xml.etree.ElementTree as ET


class FindSecBugsXMLMisuseReport(AbstractMisuseReport):

    __mapper_args__ = {'polymorphic_identity': 'findsecbugs'}
    
    def __init__(self, findsecbugs_error):
        self.findsecbugs_error: ET.Element
        self.findsecbugs_error = findsecbugs_error

        self.file_path = self.findsecbugs_error.find('Class').find('SourceLine').attrib.get('sourcepath')
        self.method_name = None if self.findsecbugs_error.find('Method') == None else self.findsecbugs_error.find('Method').attrib.get('name')
        self.method_parameter_types = None
        _start_line = None if self.findsecbugs_error.find('SourceLine') == None else self.findsecbugs_error.find('SourceLine').attrib.get('start')
        self.line = None if _start_line==None else _start_line
        self.api = None
        self.name = self.findsecbugs_error.attrib.get('type')
        self.description = None
        print(self.__repr__())