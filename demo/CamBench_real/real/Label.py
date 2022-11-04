from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from AbstractMisuseReport import KEY_API, KEY_DESCRIPTION, KEY_FILE_PATH, KEY_LINE, KEY_METHOD_NAME, KEY_METHOD_PARAMS, KEY_METHOD_RETURN, KEY_NAME
from base import Base
from sqlalchemy.orm import relationship



KEY_VIOLATION="is_violation"

class Label(Base):
    __tablename__="label"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_violation = Column(Boolean)
    file_path = Column(String)
    method_name=Column(String)
    method_parameter_types=Column(String)
    method_return_type=Column(String)
    line=Column(Integer)
    api=Column(String)
    name = Column(String(30))
    description = Column(String)

    project = Column(Integer, ForeignKey("project.id"))

    def __init__(self, label):
        #self.label = label

        self.name = str(label['name'])
        self.api = str(label['api'])
        self.file_path = str(label['crypto-usage']['location']['file'])
        method = label["crypto-usage"]["location"]["method"]
        self.method_name = str(method.split('(')[0].split(' ')[-1])
        self.method_parameter_types = str(map(lambda param: param.split(' ')[-2], method.split('(')[1].split(')')[0].split(',')))
        self.method_return_type = str(method.split('(')[0].split(' ')[-2])
        self.line = int(label['crypto-usage']['location']['line'])
        self.is_violation = bool(label['crypto-usage']['violation'])

    def __repr__(self):
        return f"Label({self.api}, {self.line})"


    


    

    