

import glob
import sys
from sqlalchemy import create_engine

import yaml

from Project import Project
from AbstractMisuseReport import AbstractMisuseReport
from AbstractAnalysis import AbstractAnalysis
from matcher.AbstractMatcher import AbstractMatcher
from tools.CryptoAnalysis.CryptoAnalysisAnalysis import CryptoAnalysis
from tools.CryptoGuard.CryptoGuardAnalysis import CryptoGuard
from Label import Label

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session




if __name__ == '__main__':
    repo_path = sys.argv[1]
    project_path = sys.argv[2]
    db_path = sys.argv[3]

    if not (repo_path and project_path):
        print("missing input parameter")
        exit(1)

    # connect to database
    engine = create_engine("sqlite:///test.db", echo=True)

    # create tables if not exist
    Project.metadata.create_all(engine)
    AbstractAnalysis.metadata.create_all(engine)
    AbstractMisuseReport.metadata.create_all(engine)
    Label.metadata.create_all(engine)
    AbstractMatcher.metadata.create_all(engine)
    

    Session = sessionmaker(bind=engine)
    session = Session()

    project = Project(repo_path, project_path)
    for label in project.get_labels():
        print(label)
        session.add(label)
    session.commit()

    # perform analysis with all tools and wrap results as AbstractMisuseReports
    analyzer = [CryptoAnalysis(project), CryptoGuard(project)]
    for analysis in analyzer:
        analysis.execute()
        session.add_all(analysis.get_reported_misuses())

    # calculate matches
    for analysis in analyzer:
        for misuse in analysis.get_reported_misuses():
            for label in project.get_labels():
                session.add(AbstractMatcher(label, misuse))

    

            
    session.commit()

    # # match misuse with labels
    # print(f"match reported misuses with labels for")
    # for analysis in analyzer:
    #     print(f"... {analysis.tool_name()}")
    #     misuses = analysis.get_reported_misuses()
    #     if misuses == None:
    #         # TODO analysis failed!
    #         continue
    #     for misuse in misuses:
    #         for label in labels:
    #             misuse.check_if_matches_label(label)

    # print("RESULTS")
    # for label in labels:
    #     print(label.matching_errors)

    