from fastapi import FastAPI, HTTPException, UploadFile,File
from typing import List
from Users import users
from Educations import edu
from Exp import exp
from Project import project
from Skill import skill
from Publication import publication
from Ref import ref




app = FastAPI()

app.include_router(users.route)
app.include_router(edu.route)
app.include_router(exp.route)
app.include_router(project.route)
app.include_router(skill.route)
app.include_router(publication.route)
app.include_router(ref.route)




@app.get("/")
def home():
    return {"Message":"This is test"}
    
