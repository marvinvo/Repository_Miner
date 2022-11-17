import os
import pathlib

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from base import Base
from Project import Project

TOOL_NAME="tool_name"
MISUSE_REPORTS="misuse_reports"


class AbstractAnalysis(Base):

    __tablename__="analysis"

    id = Column(Integer, primary_key=True)
    tool_name = Column(String)
    finished_without_exception = Column(Integer)

    analysis_tool = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': analysis_tool}

    project_id = Column(Integer, ForeignKey("project.id"))
    misuses = relationship("AbstractMisuseReport", backref="analysis")

    def execute(self):
        pass

    def get_path_for_tool(self, tool_name):
        root_path = pathlib.Path(__file__).parent.parent.resolve()
        print(root_path)
        tool_path = os.path.join(root_path, "tools", tool_name)
        if os.path.exists(tool_path):
            return tool_path
        raise FileNotFoundError(tool_path)

    def get_tool_directory(self, tool_name):
        root_path = pathlib.Path(__file__).parent.parent.resolve()
        print(root_path)
        tool_path = os.path.join(root_path, "tools", tool_name)
        if os.path.exists(tool_path):
            return tool_path
        raise FileNotFoundError(tool_path)

    def get_tool_path(self, tool_name):
        tool_directory = self.get_tool_directory(tool_name)
        generator = pathlib.Path(tool_directory).rglob(f'{tool_name}.jar')
        tool_path = next(generator, None)
        if(tool_path):
            return tool_path

        raise FileNotFoundError(tool_directory)

    def get_reported_misuses(self):
        pass

    