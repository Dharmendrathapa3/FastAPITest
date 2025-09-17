from pydantic import BaseModel, Field
from datetime import datetime
from database import custome_query



qr="""
           CREATE TABLE IF NOT EXISTS experiences(
                id INT AUTO_INCREMENT PRIMARY KEY,
                position VARCHAR(50) NOT NULL,
                organization VARCHAR(100) NOT NULL,
                start_date VARCHAR(100) NOT NULL,
                end_date VARCHAR(100) NOT NULL,
                is_publish  BOOLEAN NOT NULL,
                created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
custome_query(qr)


class ExpModel(BaseModel):
    id:int = None
    position:str
    organization: str
    start_date:str
    end_date:str
    is_publish:bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

