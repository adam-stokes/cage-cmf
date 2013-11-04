from app.system.contrib.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    enable_comment = Column(Boolean)
    
    def __init__(self, enable_comment):
        self.enable_comment = enable_comment

    def __repr__(self):
        return "<Page('A page')>"
    
