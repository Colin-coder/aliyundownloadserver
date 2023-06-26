from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
from app.utils import md5

app = FastAPI()

class TaskData(BaseModel):
    id: str
    urlPath: str

allDownloadTasks = []

@app.get("/")
def get_hello():
    return {"hello": "world"}

@app.get("/alltasks")
def read_alltasks():
    return allDownloadTasks

@app.post("/addtasks")
def add_item(task: TaskData):
    print(f"input task: {task}")
    task.id = md5(task.urlPath)
    id_exists = False
    for singleTask in allDownloadTasks:
        if singleTask.id == task.id:
            id_exists = True
            break
    result = {}
    if id_exists:
        error_msg = f"path={task.urlPath} has been existed"
        status_code = 404
        result = {"error": error_msg, "status": status_code}
    else:
        allDownloadTasks.append(task)
        print(f"allDownloadTasks: {allDownloadTasks}")
        result = {"status": 200}

    return json.dumps(result)
