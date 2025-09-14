from fastapi import APIRouter,  HTTPException
from Users.user_model import Users, UpdateUsers
from database import get_connection
from typing import List



route=APIRouter()



# Listing Users
@route.get('/users',response_model=List[Users])
async def get_users():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    result=cursor.fetchall()
    if result is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Users Data Not Found")
    
    conn.commit()
    cursor.close()
    conn.close()
    return result
     
     
#Create Users
@route.post("/users/")
async def create_users(user: Users):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()

    #Checking Email Already Exits or not
    cursor.execute("SELECT email FROM users ")
    emails=[email[0] for email in cursor.fetchall()]
    
    if user.email in emails:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #Insert New User Data
    sql = "INSERT INTO users (full_name, address, email,password,contact,github_link,about_me) VALUES (%s, %s, %s,%s, %s, %s,%s)"
    cursor.execute(sql, (user.full_name, user.address, user.email, user.password, user.contact,user.github_link,user.about_me))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message":f"User {user.email} is Created Successfully"}


#Update User data
@route.put("/users/{user_id}", )
async def update_users(user_id, user:UpdateUsers):
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection error")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="User not found")
        cursor.execute(
            "UPDATE users SET full_name=%s, address=%s, email=%s,contact=%s,github_link=%s,about_me=%s WHERE id = %s",
            (user.full_name,user.address,user.email,user.contact,user.github_link,user.about_me, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message":f"User {user.full_name} Update Successfully"}


#Delete user
@route.delete('/users/{user_id}')
async def delete_user(user_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()
    cursor.execute("SELECT full_name FROM users WHERE id = %s", (user_id,))
    data=cursor.fetchone()
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":f"User {data[0]} is Deleted Successfully"}

#Get Specific User
@route.get('/user')
async def get_user(user_id: int):
    conn = get_connection()
    field=["id","full_name","address","email","contact","github_link","about_me","created_at"]
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    cursor = conn.cursor()
    cursor.execute("SELECT  id, full_name, address, email, contact, github_link, about_me, created_at FROM users WHERE id = %s", (user_id,))
    data={key:value for key,value in zip(field,cursor.fetchone())}
    if  data is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    conn.commit()
    cursor.close()
    conn.close()
    return data


