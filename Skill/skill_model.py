from pydantic import BaseModel, Field
from datetime import datetime
from database import custome_query


# custome_query("DROP TABLE projects")
qr="""
           CREATE TABLE IF NOT EXISTS skills(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                is_publish  BOOLEAN NOT NULL,
                created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
custome_query(qr)


class SkillModel(BaseModel):
    id:int = None
    title:str
    is_publish:bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

