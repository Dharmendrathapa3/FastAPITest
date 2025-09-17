
from fastapi import APIRouter,  HTTPException
from Skill.skill_model import SkillModel
from database import get_connection,closed_connection
from typing import List



route=APIRouter()



# Listing skill
@route.get('/skills',response_model=List[SkillModel])
async def get_skills():
    conn,cursor = get_connection(dic=True)
    
    cursor.execute("SELECT * FROM skills")
    result=cursor.fetchall()

    if result ==[]:
        closed_connection()
        raise HTTPException(status_code=404, detail="skills Data Not Found")
    
    closed_connection()
    return result
     

#Get Specific skill
@route.get('/skill')
async def get_skill(skill_id: int):
    conn,cursor = get_connection(dic=True)

    cursor.execute("SELECT  * FROM skills WHERE id = %s", (skill_id,))
    data=cursor.fetchone()
    if  data is None:
        closed_connection()
        raise HTTPException(status_code=404, detail="skill not found")
    
    closed_connection()
    return data


#Create skill
@route.post("/skills/")
async def create_skill(skills: SkillModel):
    conn,cursor = get_connection()

   
    #Insert New skill Data
    sql = "INSERT INTO skills (title,is_publish) VALUES (%s, %s)"
    cursor.execute(sql, (skills.title,skills.is_publish))
    conn.commit()
    
    closed_connection()
    
    return {"message":f"'{skills.title}' skill added Successfully"}
    # return skills


#Update skill data
@route.put("/skills/{skill_id}")
async def update_skill(skill_id, skills:SkillModel):
        conn,cursor = get_connection()

        cursor.execute("SELECT id FROM skills WHERE id = %s", (skill_id,))
        if cursor.fetchone() is None:
            closed_connection()
            raise HTTPException(status_code=404, detail="skill not found")
        cursor.execute(
            "UPDATE skills SET title=%s,is_publish =%s WHERE id = %s",
            (skills.title,skills.is_publish, skill_id)
        )
        conn.commit()

        closed_connection()
        return {"message":f"'{skills.title}' skill Updated Successfully"}
        # return skills


#Delete skill
@route.delete('/skills/{skill_id}')
async def delete_skill(skill_id: int):
    conn,cursor = get_connection()

    cursor.execute("SELECT title, id FROM skills WHERE id = %s", (skill_id,))
    data=cursor.fetchone()
    if  data is None:
        closed_connection()
        raise HTTPException(status_code=404, detail="skill not found")
    cursor.execute("DELETE FROM skills WHERE id = %s", (skill_id,))
    
    conn.commit()
    closed_connection()
    return {"message":f" '{data[0]}' skill Deleted Successfully"}




