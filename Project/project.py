
from fastapi import APIRouter,  HTTPException
from Project.project_model import ProjectModel
from database import get_connection,closed_connection
from typing import List



route=APIRouter()



# Listing Project
@route.get('/projects',response_model=List[ProjectModel])
async def get_projects():
    _,cursor = get_connection(dic=True)
   
   
    cursor.execute("SELECT * FROM projects")
    result=cursor.fetchall()

    if result ==[]:
        closed_connection()
        raise HTTPException(status_code=404, detail="Projects Data Not Found")
    
    closed_connection()
    return result
     

#Get Specific Project
@route.get('/project')
async def get_project(project_id: int):
    _,cursor = get_connection()

    cursor.execute("SELECT  * FROM projects WHERE id = %s", (project_id,))
    data=cursor.fetchone()
    if  data is None:
        closed_connection()
        raise HTTPException(status_code=404, detail="Project not found")
    
    closed_connection()
    return data


#Create Project
@route.post("/projects/")
async def create_project(projects: ProjectModel):
    conn,cursor = get_connection()

   
    #Insert New Project Data
    sql = "INSERT INTO projects (title,description,image,link,github_link,is_publish) VALUES (%s, %s, %s, %s,%s,%s)"
    cursor.execute(sql, (projects.title,projects.description,projects.image,projects.link,projects.github_link,projects.is_publish))
    conn.commit()

    closed_connection()
    
    return {"message":f"'{projects.title}' Project added Successfully"}
    # return projects


#Update Project data
@route.put("/projects/{project_id}")
async def update_project(project_id, projects:ProjectModel):
        
        conn,cursor = get_connection()

        cursor.execute("SELECT id FROM projects WHERE id = %s", (project_id,))
        if cursor.fetchone() is None:
            closed_connection()
            raise HTTPException(status_code=404, detail="Project not found")
        cursor.execute(
            "UPDATE projects SET title=%s, description=%s, image=%s, link=%s,github_link=%s,is_publish =%s WHERE id = %s",
            (projects.title,projects.description,projects.image,projects.link,projects.github_link,projects.is_publish, project_id)
        )
        conn.commit()
        closed_connection()
        return {"message":f"'{projects.title}' Project Updated Successfully"}
        # return projects


#Delete Project
@route.delete('/projects/{project_id}')
async def delete_project(project_id: int):
    conn,cursor = get_connection()
    
    cursor.execute("SELECT title, id FROM projects WHERE id = %s", (project_id,))
    data=cursor.fetchone()
    if  data is None:
        closed_connection()
        raise HTTPException(status_code=404, detail="Project not found")
    cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
    
    conn.commit()
    closed_connection()
    return {"message":f" '{data[0]}' Project Deleted Successfully"}




