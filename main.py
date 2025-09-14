from fastapi import FastAPI, HTTPException, UploadFile,File
from typing import List
from Users import users
from Educations import edu




app = FastAPI()

app.include_router(users.route)
app.include_router(edu.route)



@app.get("/")
def home():
    return {"Message":"This is test"}
    
