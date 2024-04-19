from pydantic import BaseModel

class NewsList(BaseModel):
    title: str
    thumbnail: str
    link: str
    date: str
    category: str
    source: str

    class Config:
        orm_mode = True
