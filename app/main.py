from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
 
app = FastAPI()
 
@app.get("/")
def root():
    return FileResponse("app/index.html")
 
@app.post("/user")
def user(name = Body(embed=True)):
    return {"message": f"Вас зовут {name}"}