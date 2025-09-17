from pydantic import BaseModel, Field
from datetime import datetime
from database import custome_query


# custome_query("DROP TABLE projects")
qr="""
           CREATE TABLE IF NOT EXISTS projects(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                image TEXT,
                link VARCHAR(100),
                github_link VARCHAR(100),
                is_publish  BOOLEAN NOT NULL,
                created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
custome_query(qr)


class ProjectModel(BaseModel):
    id:int = None
    title:str
    description:str=""
    image:str=""
    link: str =""
    github_link:str =""
    is_publish:bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

