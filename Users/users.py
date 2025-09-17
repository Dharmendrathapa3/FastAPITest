from fastapi import APIRouter,  HTTPException
from Users.user_model import Users, UpdateUsers
from database import get_connection, closed_connection
from typing import List



route=APIRouter()



# Listing Users
@route.get('/users',response_model=List[Users])
async def get_users():
    _,cursor = get_connection(True)
   
    cursor.execute("SELECT * FROM users")
    result=cursor.fetchall()
    if result is None:
        closed_connection()
        raise HTTPException(status_code=404, detail="Users Data Not Found")
    
    closed_connection()

    return result


     
#Get Specific User
@route.get('/user')
async def get_user(user_id: int):
    # field=["id","full_name","address","email","contact","github_link","about_me","created_at"]

    _,cursor = get_connection(dic=True)
    
    cursor.execute("SELECT  id, full_name, address, email, contact, github_link, about_me, created_at FROM users WHERE id = %s", (user_id,))
    data=cursor.fetchone()
    if  data is None:
        closed_connection()
        raise HTTPException(status_code=404, detail="User not found")
    # data={key:value for key,value in zip(field,data)}
    
    closed_connection()
    return data


#Create Users
@route.post("/users/")
async def create_users(user: Users):
    conn,cursor = get_connection()
    
    #Checking Email Already Exits or not
    cursor.execute("SELECT email FROM users")
    data=cursor.fetchall()
    emails=[email[0] for email in data]
    
    if user.email in emails:
        closed_connection()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #Insert New User Data
    sql = "INSERT INTO users (full_name, address, email,password,contact,github_link,about_me) VALUES (%s, %s, %s,%s, %s, %s,%s)"
    cursor.execute(sql, (user.full_name, user.address, user.email, user.password, user.contact,user.github_link,user.about_me))
    conn.commit()

    closed_connection()
    
    return {"message":f"User '{user.email}' is Created Successfully"}
    


#Update User data
@route.put("/users/{user_id}", )
async def update_users(user_id, user:UpdateUsers):
        conn,cursor = get_connection()
       
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if cursor.fetchone() is None:
            closed_connection()
            raise HTTPException(status_code=404, detail="User not found")
        cursor.execute(
            "UPDATE users SET full_name=%s, address=%s, email=%s,contact=%s,github_link=%s,about_me=%s WHERE id = %s",
            (user.full_name,user.address,user.email,user.contact,user.github_link,user.about_me, user_id)
        )
        conn.commit()

        closed_connection()
        return {"message":f"User {user.full_name} Update Successfully"}


#Delete user
@route.delete('/users/{user_id}')
async def delete_user(user_id: int):
    conn,cursor = get_connection()
    
    cursor.execute("SELECT full_name FROM users WHERE id = %s", (user_id,))
    data=cursor.fetchone()

    if  data is None:
        closed_connection()
        raise HTTPException(status_code=404, detail="User not found")
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    closed_connection()

    return {"message":f"User {data[0]} is Deleted Successfully"}




