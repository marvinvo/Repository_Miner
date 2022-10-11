import glob

import yaml


class Project():

    def __init__(self, repository_path, project_path):
        self.repository_path = repository_path
        self.project_path = project_path
        self.labels = None


    def _parse_labels(self):
        # get labels
        self.labels = []
        for label_path in glob.glob(f"{self.repository_path}/*.yaml"):
            with open(label_path, "r") as label:
                try:
                    self.labels.append(yaml.safe_load(label))
                except yaml.YAMLError as exc:
                    print(exc)

    def get_labels(self):
        if not self.labels:
            self._parse_labels()
        return self.labels
