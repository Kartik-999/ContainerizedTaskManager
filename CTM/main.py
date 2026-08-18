import json
from fastapi import FastAPI,HTTPException
from database import get_connection

app=FastAPI()
@app.on_event("startup")
def startup():
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS TaskManager (id int primary key, task Varchar(1000) NOT NULL)")
    
    conn.commit()
    cursor.close()
    conn.close()
    
@app.get("/health")
def health_check():
    return {"staus":"ok"}

@app.get("/CTM")
def get_alltasks():
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT id,task FROM TaskManager")
    rows=cursor.fetchall()
    
    conn.commit()
    cursor.close()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404,detail="No tasks at present")
    data=[{"id": row[0],"task":row[1]} for row in rows]
    return data

@app.get("/CTM/{id}")
def get_task(id: int):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT task,id FROM TaskManager Where id=%s",(id,))
    
    row=cursor.fetchone()
    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404,detail="Task with provided id is not present")
    data={"task":row[0],"id":row[1]}
    return data
@app.post("/CTM")
def create_task(id: int, task: str):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("INSERT INTO TaskManager(id,task) VALUES(%s,%s)",(id,task))
    
 
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":"task added"}

@app.put("/CTM_update")
def update_task(id: int,new_task: str):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("UPDATE TaskManager SET task =%s WHERE id=%s",(new_task,id))
    
 
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":"task updated"}
@app.delete("/CTM_delete/{id}")
def delete_task(id: int):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM TaskManager WHERE id=%s",(id,))
 
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":"Deleted"}
