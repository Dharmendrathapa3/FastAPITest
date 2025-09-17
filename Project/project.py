
from fastapi import APIRouter,  HTTPException
from Project.project_model import ProjectModel
from database import get_connection
from typing import List



route=APIRouter()



# Listing Project
@route.get('/projects',response_model=List[ProjectModel])
async def get_projects():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects")
    result=cursor.fetchall()

    if result ==[]:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Projects Data Not Found")
    
    conn.commit()
    cursor.close()
    conn.close()
    return result
     

#Get Specific Project
@route.get('/project')
async def get_project(project_id: int):
    conn = get_connection()
    
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    cursor = conn.cursor()
    cursor.execute("SELECT  * FROM projects WHERE id = %s", (project_id,))
    clu=["id","title","description","image", "link","github_link","is_publish","created_at"]
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Project not found")
    
    data={key:value for key,value in zip(clu,data)}
    
    conn.commit()
    cursor.close()
    conn.close()
    return data


#Create Project
@route.post("/projects/")
async def create_project(projects: ProjectModel):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()

   
    #Insert New Project Data
    sql = "INSERT INTO projects (title,description,image,link,github_link,is_publish) VALUES (%s, %s, %s, %s,%s,%s)"
    cursor.execute(sql, (projects.title,projects.description,projects.image,projects.link,projects.github_link,projects.is_publish))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message":f"'{projects.title}' Project added Successfully"}
    # return projects


#Update Project data
@route.put("/projects/{project_id}")
async def update_project(project_id, projects:ProjectModel):
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection error")
       
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE id = %s", (project_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Project not found")
        cursor.execute(
            "UPDATE projects SET title=%s, description=%s, image=%s, link=%s,github_link=%s,is_publish =%s WHERE id = %s",
            (projects.title,projects.description,projects.image,projects.link,projects.github_link,projects.is_publish, project_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message":f"'{projects.title}' Project Updated Successfully"}
        # return projects


#Delete Project
@route.delete('/projects/{project_id}')
async def delete_project(project_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
   
    cursor = conn.cursor()
    cursor.execute("SELECT title, id FROM projects WHERE id = %s", (project_id,))
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Project not found")
    cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":f" '{data[0]}' Project Deleted Successfully"}




