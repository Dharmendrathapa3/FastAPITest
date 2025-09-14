from fastapi import FastAPI, HTTPException, UploadFile,File
from typing import List
from Users import users




app = FastAPI()

app.include_router(users.route)


@app.get("/")
def home():
    return {"Message":"This is test"}


##Create Users



# # Create item
# @app.post("/items/", response_model=Item)
# def create_item(item: Item):
#     conn = get_connection()
#     if conn is None:
#         raise HTTPException(status_code=500, detail="Database connection error")
#     cursor = conn.cursor()
#     sql = "INSERT INTO items (name, description) VALUES (%s, %s)"
#     cursor.execute(sql, (item.name, item.description))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return item

# # Read all items
# @app.get("/items/", response_model=List[Item])
# def read_items():
#     conn = get_connection()
#     if conn is None:
#         raise HTTPException(status_code=500, detail="Database connection error")
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT id, name, description FROM items")
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return rows

# # Read single item
# @app.get("/items/{item_id}", response_model=Item)
# def read_item(item_id: int):
#     conn = get_connection()
#     if conn is None:
#         raise HTTPException(status_code=500, detail="Database connection error")
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT id, name, description FROM items WHERE id = %s", (item_id,))
#     row = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     if not row:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return row

# # Update item
# @app.put("/items/{item_id}", response_model=Item)
# def update_item(item_id: int, item: Item):
#     conn = get_connection()
#     if conn is None:
#         raise HTTPException(status_code=500, detail="Database connection error")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM items WHERE id = %s", (item_id,))
#     if cursor.fetchone() is None:
#         cursor.close()
#         conn.close()
#         raise HTTPException(status_code=404, detail="Item not found")
#     cursor.execute(
#         "UPDATE items SET name = %s, description = %s WHERE id = %s",
#         (item.name, item.description, item_id)
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {**item.dict(), "id": item_id}

# # Delete item
# @app.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     conn = get_connection()
#     if conn is None:
#         raise HTTPException(status_code=500, detail="Database connection error")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM items WHERE id = %s", (item_id,))
#     if cursor.fetchone() is None:
#         cursor.close()
#         conn.close()
#         raise HTTPException(status_code=404, detail="Item not found")
#     cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return {"detail": "Item deleted"}



# @app.post("/upload_file")
# def file_upload(file:UploadFile=File(...)):
#     with open(f"upload_file/{file.filename}","wb") as f:
#         f.write(file.file.read())
#     return {"message":f"{file.filename} save succ"}
    

