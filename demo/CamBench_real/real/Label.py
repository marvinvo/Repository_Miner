
class Label():

    def __init__(self, label):
        self.label = label
        self.matching_errors = dict()

    def get_name(self) -> str:
        return str(self.label['name'])

    def get_api(self) -> str:
        return str(self.label['api'])

    def get_file_path(self) -> str:
        return str(self.label['crypto-usage']['location']['file'])
    
    def get_method(self) -> str:
        return str(self.label['crypto-usage']['location']['method'])

    def get_line(self) -> int:
        return int(self.label['crypto-usage']['location']['line'])

    def is_violation(self) -> bool:
        return self.label['crypto-usage']['violation']

    def add_matching_error(self, tool, error, list_of_matcher):
        if not tool in self.matching_errors:
            self.matching_errors[tool] = dict()
        self.matching_errors[tool][error] = list_of_matcher
        
    


    

    