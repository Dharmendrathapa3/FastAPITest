
from fastapi import APIRouter,  HTTPException
from Educations.edu_model import EduModel
from database import get_connection
from typing import List



route=APIRouter()



# Listing Education
@route.get('/edus',response_model=List[EduModel])
async def get_edus():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM educations")
    result=cursor.fetchall()
    if result is []:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Eduactions Data Not Found")
    
    conn.commit()
    cursor.close()
    conn.close()
    return result


#Get Specific Education
@route.get('/edu')
async def get_edu(edu_id: int):
    conn = get_connection()
    field=["id","degree", "organization","pass_year","is_publish"]
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()
    cursor.execute("SELECT  * FROM educations WHERE id = %s", (edu_id,))
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    data={key:value for key,value in zip(field,data)}
    
    conn.commit()
    cursor.close()
    conn.close()
    return data


     
#Create Education
@route.post("/edus/")
async def create_edu(edus: EduModel):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()

   
    #Insert New Education Data
    sql = "INSERT INTO educations (degree, organization, pass_year,is_publish) VALUES (%s, %s, %s,%s)"
    cursor.execute(sql, (edus.degree,edus.organization,edus.pass_year,edus.is_publish))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message":f"'{edus.degree}' Education added Successfully"}
    # return edus


#Update Education data
@route.put("/edus/{edu_id}")
async def update_edu(edu_id, edus:EduModel):
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection error")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM educations WHERE id = %s", (edu_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Education not found")
        cursor.execute(
            "UPDATE educations SET degree=%s, organization=%s, pass_year=%s,is_publish =%s WHERE id = %s",
            (edus.degree,edus.organization,edus.pass_year,edus.is_publish, edu_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message":f"'{edus.degree}' Education Updated Successfully"}
        # return edus


#Delete Education
@route.delete('/edus/{edu_id}')
async def delete_edu(edu_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()
    cursor.execute("SELECT degree, id FROM educations WHERE id = %s", (edu_id,))
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Education not found")
    cursor.execute("DELETE FROM educations WHERE id = %s", (edu_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":f"'{data[0]}'Education Deleted Successfully"}

