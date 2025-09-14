
from fastapi import APIRouter,  HTTPException
from Educations.edu_model import EduModel
from database import get_connection
from typing import List



route=APIRouter()



# Listing Education
@route.get('/edus',response_model=List[EduModel])
async def get_edu():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM educations")
    result=cursor.fetchall()
    if result is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Eduactions Data Not Found")
    
    conn.commit()
    cursor.close()
    conn.close()
    return result
     
     
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
    
    # return {"message":f"Education added Successfully"}
    return edus


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
        # return {"message":f"Education Updated Successfully"}
        return edus


#Delete Education
@route.delete('/edus/{edu_id}')
async def delete_edu(edu_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM educations WHERE id = %s", (edu_id,))
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Education not found")
    cursor.execute("DELETE FROM educations WHERE id = %s", (edu_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":f"Education Deleted Successfully"}

#Get Specific Education
@route.get('/edu')
async def get_edu(edu_id: int):
    conn = get_connection()
    
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()
    cursor.execute("SELECT  * FROM educations WHERE id = %s", (edu_id,))
    clu=["id","degree", "organization"," pass_year","is_publish"]
    if  cursor.fetchone() is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Education not found")
    data={key:value for key,value in zip(clu,cursor.fetchone())}
    
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Education not found")
    
    conn.commit()
    cursor.close()
    conn.close()
    return data


