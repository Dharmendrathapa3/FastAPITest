from pydantic import BaseModel, Field
from datetime import datetime
from database import custome_query


custome_query("DROP TABLE publications")
qr="""
           CREATE TABLE IF NOT EXISTS publications(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title TEXT NOT NULL,
                publication TEXT,
                link TEXT,
                is_publish  BOOLEAN NOT NULL,
                created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
custome_query(qr)


class PublicationModel(BaseModel):
    id:int = None
    title:str
    publication:str=""
    link: str =""
    is_publish:bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

