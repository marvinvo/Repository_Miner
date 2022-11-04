from sqlalchemy import create_engine
from Label import Label
from sqlalchemy.orm import sessionmaker

from AbstractMisuseReport import AbstractMisuseReport


engine = create_engine("sqlite:///test.db", echo=True)

Session = sessionmaker(bind=engine)
session = Session()

for class_instance in session.query(AbstractMisuseReport, Label).all():
    print(class_instance)



session.close()



#def misuse_match_request(must_match_labels, must_not_match_labels, unrelated_labels):
    
    
