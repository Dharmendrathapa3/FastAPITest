from pydantic import BaseModel, Field
from datetime import datetime
from database import custome_query


# custome_query("DROP TABLE refs")
qr="""
           CREATE TABLE IF NOT EXISTS refs(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                org VARCHAR(100),
                phone VARCHAR(100),
                email VARCHAR(100),
                is_publish  BOOLEAN NOT NULL,
                created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
custome_query(qr)


class RefModel(BaseModel):
    id:int = None
    name:str
    org:str=""
    phone:str=""
    email:str=""
    is_publish:bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

