from fastapi import FastAPI

app = FastAPI()


@app.get("/tasks")
def get_tasks():
    return [
        {"id": 1, "title": "Start Python", "completed": False},
        {"id": 2, "title": "Build FastAPI", "completed": False},
        {"id": 3, "title": "Learn Docker", "completed": False},
    ]