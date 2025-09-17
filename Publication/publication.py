
from fastapi import APIRouter,  HTTPException
from Publication.publication_model import PublicationModel
from database import get_connection
from typing import List



route=APIRouter()



# Listing publications
@route.get('/publications',response_model=List[PublicationModel])
async def get_publications():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM publications")
    result=cursor.fetchall()

    if result ==[]:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="publications Data Not Found")
    
    conn.commit()
    cursor.close()
    conn.close()
    return result
     

#Get Specific publication
@route.get('/publication')
async def get_publication(publication_id: int):
    conn = get_connection()
    
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    cursor = conn.cursor()
    cursor.execute("SELECT  * FROM publications WHERE id = %s", (publication_id,))
    clu=["id","title","publication","link","is_publish","created_at"]
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="publication not found")
    
    data={key:value for key,value in zip(clu,data)}
    
    conn.commit()
    cursor.close()
    conn.close()
    return data


#Create publication
@route.post("/publications/")
async def create_publication(publications: PublicationModel):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()

   
    #Insert New publication Data
    sql = "INSERT INTO publications (title,publication,link,is_publish) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (publications.title,publications.publication,publications.link,publications.is_publish))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message":f"'{publications.title}' publication added Successfully"}
    # return publications


#Update publication data
@route.put("/publications/{publication_id}")
async def update_publication(publication_id, publications:PublicationModel):
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection error")
       
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM publications WHERE id = %s", (publication_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="publication not found")
        cursor.execute(
            "UPDATE publications SET title=%s, publication=%s, link=%s,is_publish =%s WHERE id = %s",
            (publications.title,publications.publication,publications.link,publications.is_publish, publication_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message":f"'{publications.title}' publication Updated Successfully"}
        # return publications


#Delete publication
@route.delete('/publications/{publication_id}')
async def delete_publication(publication_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
   
    cursor = conn.cursor()
    cursor.execute("SELECT title, id FROM publications WHERE id = %s", (publication_id,))
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="publication not found")
    cursor.execute("DELETE FROM publications WHERE id = %s", (publication_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":f" '{data[0]}' publication Deleted Successfully"}




