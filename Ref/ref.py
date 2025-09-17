
from fastapi import APIRouter,  HTTPException
from Ref.ref_model import RefModel
from database import get_connection
from typing import List



route=APIRouter()



# Listing refs
@route.get('/refs',response_model=List[RefModel])
async def get_refs():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM refs")
    result=cursor.fetchall()

    if result ==[]:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="References Data Not Found")
    
    conn.commit()
    cursor.close()
    conn.close()
    return result
     

#Get Specific ref
@route.get('/ref')
async def get_ref(ref_id: int):
    conn = get_connection()
    
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    cursor = conn.cursor()
    cursor.execute("SELECT  * FROM refs WHERE id = %s", (ref_id,))
    clu=["id","name","org","phone","email","created_at"]
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Reference not found")
    
    data={key:value for key,value in zip(clu,data)}
    
    conn.commit()
    cursor.close()
    conn.close()
    return data


#Create ref
@route.post("/refs/")
async def create_ref(refs: RefModel):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()

   
    #Insert New ref Data
    sql = "INSERT INTO refs (name,org,phone,email,is_publish) VALUES (%s, %s,%s,%s,%s)"
    cursor.execute(sql, (refs.name,refs.org,refs.phone,refs.email,refs.is_publish))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message":f"'{refs.name}' reference added Successfully"}
    # return refs


#Update ref data
@route.put("/refs/{ref_id}")
async def update_ref(ref_id, refs:RefModel):
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection error")
       
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM refs WHERE id = %s", (ref_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Reference not found")
        cursor.execute(
            "UPDATE refs SET name=%s,org=%s,phone=%s,email=%s,is_publish =%s WHERE id = %s",
            (refs.name,refs.org,refs.phone,refs.email,refs.is_publish, ref_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message":f"'{refs.name}' reference Updated Successfully"}
        # return refs


#Delete ref
@route.delete('/refs/{ref_id}')
async def delete_ref(ref_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
   
    cursor = conn.cursor()
    cursor.execute("SELECT name, id FROM refs WHERE id = %s", (ref_id,))
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Reference not found")
    cursor.execute("DELETE FROM refs WHERE id = %s", (ref_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":f" '{data[0]}' reference Deleted Successfully"}




