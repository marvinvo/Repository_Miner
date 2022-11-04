from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from base import Base

MATCHES=1
NOT_FOUND=0
NOT_MATCHES=-1


class AbstractMatcher(Base):

    __tablename__="matches"
    
    id = Column(Integer, primary_key=True)
    misuse_id = Column(Integer, ForeignKey("misuse.id"))
    label_id = Column(Integer, ForeignKey("label.id"))
    misuse = relationship("AbstractMisuseReport", backref="matches", enable_typechecks=False)
    label = relationship("Label", backref="matches")

    api = Column(Integer)
    path = Column(Integer)
    line = Column(Integer)
    method_name = Column(Integer)
    method_parameter_types = Column(Integer)
    method_return_type = Column(Integer)
    name = Column(Integer)
    description = Column(Integer)

    
    #type = Column(String)
    #is_match = Column(Integer)

    def __init__(self, label, misuse):
        self.misuse = misuse
        self.label = label
        self.matches()

    def matches(self) -> int:
        self.api = self._matches_api()
        self.path = self._matches_path()
        self.line = self._matches_line()
        self.method_name = self._matches_method_name()


    def _matches_line(self):
        if not self.label.line or not self.misuse.line:
            return NOT_FOUND
        elif self.label.line==self.misuse.line:
            return MATCHES
        else:
            return NOT_MATCHES


    def _matches_api(self):
        if not self.label.api or not self.misuse.api:
            return NOT_FOUND
        elif self.label.api == self.misuse.api:
            return MATCHES
        else:
            return NOT_MATCHES


    def _matches_path(self):
        label_path = self.label.file_path
        misuse_path = self.misuse.file_path

        if not label_path or not misuse_path:
            return NOT_FOUND

        misuse_path = misuse_path.replace(".java", "").replace(".class", "")
        if ".jar" in misuse_path:
            misuse_path = misuse_path.split(".jar")[-1]

        
        if misuse_path in label_path:
            return MATCHES
        else:
            return NOT_MATCHES

    def _matches_method_name(self):
        label_method_name = self.label.method_name
        misuse_method_name = self.misuse.method_name

        if not label_method_name or not misuse_method_name:
            return NOT_FOUND

        if label_method_name == misuse_method_name:
            return MATCHES
        
        return NOT_MATCHES


    
