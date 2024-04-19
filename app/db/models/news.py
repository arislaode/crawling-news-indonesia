# db/models/news.py
from sqlalchemy import Column, Integer, String
from ..base_class import Base

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False)
    thumbnail = Column(String(255), nullable=False)
    date = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    source = Column(String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "link": self.link,
            "thumbnail": self.thumbnail,
            "date": self.date,
            "category": self.category,
            "source": self.source
        }
