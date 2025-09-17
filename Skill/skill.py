
from fastapi import APIRouter,  HTTPException
from Skill.skill_model import SkillModel
from database import get_connection
from typing import List



route=APIRouter()



# Listing skill
@route.get('/skills',response_model=List[SkillModel])
async def get_skills():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM skills")
    result=cursor.fetchall()

    if result ==[]:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="skills Data Not Found")
    
    conn.commit()
    cursor.close()
    conn.close()
    return result
     

#Get Specific skill
@route.get('/skill')
async def get_skill(skill_id: int):
    conn = get_connection()
    
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    cursor = conn.cursor()
    cursor.execute("SELECT  * FROM skills WHERE id = %s", (skill_id,))
    clu=["id","title","is_publish","created_at"]
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="skill not found")
    
    data={key:value for key,value in zip(clu,data)}
    
    conn.commit()
    cursor.close()
    conn.close()
    return data


#Create skill
@route.post("/skills/")
async def create_skill(skills: SkillModel):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()

   
    #Insert New skill Data
    sql = "INSERT INTO skills (title,is_publish) VALUES (%s, %s)"
    cursor.execute(sql, (skills.title,skills.is_publish))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message":f"'{skills.title}' skill added Successfully"}
    # return skills


#Update skill data
@route.put("/skills/{skill_id}")
async def update_skill(skill_id, skills:SkillModel):
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection error")
       
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM skills WHERE id = %s", (skill_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="skill not found")
        cursor.execute(
            "UPDATE skills SET title=%s,is_publish =%s WHERE id = %s",
            (skills.title,skills.is_publish, skill_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message":f"'{skills.title}' skill Updated Successfully"}
        # return skills


#Delete skill
@route.delete('/skills/{skill_id}')
async def delete_skill(skill_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
   
    cursor = conn.cursor()
    cursor.execute("SELECT title, id FROM skills WHERE id = %s", (skill_id,))
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="skill not found")
    cursor.execute("DELETE FROM skills WHERE id = %s", (skill_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":f" '{data[0]}' skill Deleted Successfully"}




