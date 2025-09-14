from pydantic import BaseModel, Field
from datetime import datetime
from database import custome_query
from typing import Optional



qr="""
           CREATE TABLE IF NOT EXISTS educations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                degree VARCHAR(50) NOT NULL,
                organization VARCHAR(100) NOT NULL,
                pass_year VARCHAR(100) NOT NULL,
                is_publish  BOOLEAN NOT NULL,
                created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
custome_query(qr)


class EduModel(BaseModel):
    id:int = None
    degree:str
    organization: str
    pass_year:str
    is_publish:bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

