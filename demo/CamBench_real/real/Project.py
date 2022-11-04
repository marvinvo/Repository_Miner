import glob
from sqlalchemy import Column, Integer, String

import yaml

from Label import Label

from sqlalchemy.orm import relationship
from base import Base

PROJECT_PATH="project_path"
REPO_PATH="repository_path"
LABELS="labels"


class Project(Base):

    __tablename__="project"

    id = Column(Integer, primary_key=True)
    repository_path= Column(String)
    project_path = Column(String)

    labels = relationship("Label", backref="project.id")
    analysis = relationship("AbstractAnalysis", backref="project")

    def __init__(self, repository_path, project_path):
        self.repository_path = repository_path
        self.project_path = project_path
        self.labels = self._parse_labels()


    def _parse_labels(self):
        # get labels
        labels = []
        for label_path in glob.glob(f"{self.repository_path}/*.yaml"):
            with open(label_path, "r") as label:
                try:
                    labels.append(Label(yaml.safe_load(label)))
                except yaml.YAMLError as exc:
                    print(exc)
        return labels

    def get_labels(self):
        return self.labels

    def get_as_dict(self):
        res = dict()
        res[PROJECT_PATH] = self.project_path
        res[REPO_PATH] = self.repository_path
        res[LABELS] = [label.get_as_dict() for label in self.get_labels()]
        return res