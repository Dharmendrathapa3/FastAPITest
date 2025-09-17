from pydantic import BaseModel, Field
from datetime import datetime
from database import custome_query
from typing import Optional



qr="""
           CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(50) NOT NULL,
                address TEXT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                contact VARCHAR(20),
                github_link VARCHAR(100) NULL,
                about_me TEXT NULL,
                created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
custome_query(qr)


class Users(BaseModel):
    id:int = None
    full_name:str
    address: str =None
    email:str
    password:str
    contact:str =None
    github_link:str =None
    about_me:str=None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UpdateUsers(BaseModel):
    id:int = None
    full_name:Optional[str]
    address: Optional[str] =None
    email:Optional[str]
    contact:Optional[str] =None
    github_link:Optional[str] =None
    about_me:Optional[str]=None
    created_at: datetime = Field(default_factory=datetime.utcnow)