

import glob
import sys

import yaml

from Project import Project
from tools.CryptoAnalysis.CryptoAnalysis import CryptoAnalysis
from tools.CryptoGuard.CryptoGuard import CryptoGuard
from Label import Label



if __name__ == '__main__':
    repo_path = sys.argv[1]
    project_path = sys.argv[2]

    if not (repo_path and project_path):
        print("missing input parameter")
        exit(1)

    # perform analysis with all tools and wrap results as AbstractMisuseReports

    project = Project(repo_path, project_path)
    #CryptoAnalysis(project)
    analyzer = [CryptoAnalysis(project), CryptoGuard(project)]

    for analysis in analyzer:
        print(f"execute {analysis.tool_name()} analysis")
        analysis.execute()
    

    # read labels
    print(f"parse labels")
    labels = []
    for label_path in glob.glob(f"{repo_path}/*.yaml"):
        with open(label_path, "r") as label:
            try:
                labels.append(Label(yaml.safe_load(label)))
            except yaml.YAMLError as exc:
                print(exc)
    print(f"{len(labels)} labels found")
    

    # match misuse with labels
    print(f"match reported misuses with labels for")
    for analysis in analyzer:
        print(f"... {analysis.tool_name()}")
        misuses = analysis.get_reported_misuses()
        if misuses == None:
            # TODO analysis failed!
            continue
        for misuse in misuses:
            for label in labels:
                misuse.check_if_matches_label(label)

    print("RESULTS")
    for label in labels:
        print(label.matching_errors)

    