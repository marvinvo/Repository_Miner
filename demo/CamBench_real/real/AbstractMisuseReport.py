from sqlalchemy import INTEGER, Column, ForeignKey, Integer, String
from matcher import AbstractMatcher

from base import Base
from sqlalchemy.orm import relationship


KEY_FILE_PATH="file_path"
KEY_METHOD_NAME="method_name"
KEY_METHOD_PARAMS="method_param_types"
KEY_METHOD_RETURN="method_return_type"
KEY_LINE="line"
KEY_API="api"
KEY_NAME="name"
KEY_DESCRIPTION="description"



class AbstractMisuseReport(Base):
    __tablename__="misuse"

    id = Column(Integer, primary_key=True)
    file_path = Column(String)
    method_name=Column(String)
    method_parameter_types=Column(String)
    method_return_type=Column(String)
    line=Column(Integer)
    api=Column(String)
    name = Column(String(30))
    description = Column(String)

    analysis_tool = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': analysis_tool}

    analysis_id = Column(Integer, ForeignKey("analysis.id"))

    def __repr__(self) -> str:
        return f"{self.__tablename__}({self.file_path},{self.method_name},{self.line})"