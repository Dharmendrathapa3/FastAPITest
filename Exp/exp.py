
from fastapi import APIRouter,  HTTPException
from Exp.exp_model import ExpModel
from database import get_connection
from typing import List



route=APIRouter()



# Listing Exprience
@route.get('/exps',response_model=List[ExpModel])
async def get_exps():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM experiences")
    result=cursor.fetchall()

    if result ==[]:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Exprience Data Not Found")
    
    conn.commit()
    cursor.close()
    conn.close()
    return result


     
#Get Specific Exprience
@route.get('/exp')
async def get_exp(exp_id: int):
    conn = get_connection()
    
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()
    cursor.execute("SELECT  * FROM experiences WHERE id = %s", (exp_id,))
    clu=["id","position", "organization","start_date","end_date","is_publish","created_at"]
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="exprience not found")
    
    data={key:value for key,value in zip(clu,data)}
    
    conn.commit()
    cursor.close()
    conn.close()
    return data


#Create Exprience
@route.post("/exps/")
async def create_exp(exps: ExpModel):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()

   
    #Insert New Exprience Data
    sql = "INSERT INTO experiences (position, organization, start_date,end_date,is_publish) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (exps.position,exps.organization,exps.start_date,exps.end_date,exps.is_publish))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message":f"'{exps.position}'Exprience added Successfully"}
    # return exps


#Update Exprience data
@route.put("/exps/{exp_id}")
async def update_exp(exp_id, exps:ExpModel):
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection error")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM experiences WHERE id = %s", (exp_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Exprience not found")
        cursor.execute(
            "UPDATE experiences SET position=%s, organization=%s, start_date=%s,end_date=%s,is_publish =%s WHERE id = %s",
            (exps.position,exps.organization,exps.start_date,exps.end_date,exps.is_publish, exp_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message":f"'{exps.position}'Exprience Updated Successfully"}
        # return exps


#Delete Exprience
@route.delete('/exps/{exp_id}')
async def delete_exp(exp_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()
    cursor.execute("SELECT position,id FROM experiences WHERE id = %s", (exp_id,))
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Exprience not found")
    cursor.execute("DELETE FROM experiences WHERE id = %s", (exp_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":f"'{data[0]}'Exprience Deleted Successfully"}




