
from fastapi import APIRouter,  HTTPException
from Ref.ref_model import RefModel
from database import get_connection,closed_connection
from typing import List



route=APIRouter()



# Listing refs
@route.get('/refs',response_model=List[RefModel])
async def get_refs():
    _,cursor = get_connection(dic=True)
   
    cursor.execute("SELECT * FROM refs")
    result=cursor.fetchall()

    if result ==[]:
        closed_connection()
        raise HTTPException(status_code=404, detail="References Data Not Found")
    closed_connection()
    return result
     

#Get Specific ref
@route.get('/ref')
async def get_ref(ref_id: int):
    _,cursor = get_connection(dic=True)
    
    cursor.execute("SELECT  * FROM refs WHERE id = %s", (ref_id,))
    data=cursor.fetchone()
    if  data is None:
        closed_connection()
        raise HTTPException(status_code=404, detail="Reference not found")
    
    closed_connection()
    return data


#Create ref
@route.post("/refs/")
async def create_ref(refs: RefModel):
    conn,cursor = get_connection()
    
    #Insert New ref Data
    sql = "INSERT INTO refs (name,org,phone,email,is_publish) VALUES (%s, %s,%s,%s,%s)"
    cursor.execute(sql, (refs.name,refs.org,refs.phone,refs.email,refs.is_publish))
    conn.commit()

    closed_connection()
    
    return {"message":f"'{refs.name}' reference added Successfully"}
    # return refs


#Update ref data
@route.put("/refs/{ref_id}")
async def update_ref(ref_id, refs:RefModel):
        conn,cursor = get_connection()
        
        cursor.execute("SELECT id FROM refs WHERE id = %s", (ref_id,))
        if cursor.fetchone() is None:
            closed_connection()
        cursor.execute(
            "UPDATE refs SET name=%s,org=%s,phone=%s,email=%s,is_publish =%s WHERE id = %s",
            (refs.name,refs.org,refs.phone,refs.email,refs.is_publish, ref_id)
        )
        conn.commit()
        
        closed_connection()
        return {"message":f"'{refs.name}' reference Updated Successfully"}
        # return refs


#Delete ref
@route.delete('/refs/{ref_id}')
async def delete_ref(ref_id: int):
    conn,cursor = get_connection()
  
    cursor.execute("SELECT name, id FROM refs WHERE id = %s", (ref_id,))
    data=cursor.fetchone()
    if  data is None:
        closed_connection()
        raise HTTPException(status_code=404, detail="Reference not found")
    cursor.execute("DELETE FROM refs WHERE id = %s", (ref_id,))
    conn.commit()
    closed_connection()
    return {"message":f" '{data[0]}' reference Deleted Successfully"}




