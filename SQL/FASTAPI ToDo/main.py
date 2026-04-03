from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from repository import UserRepository, TaskRepository
from models import CreateUser, CreateTask, BaseTask, UserLogin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_repo = UserRepository()
task_repo = TaskRepository()


@app.post("/registration")
def registration(user: CreateUser):
    new_user = user_repo.create_user(user)

    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")

    return new_user


@app.post("/login")
def login(user_data: UserLogin):

    user = user_repo.login(user_data.email, user_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid data")

    return user


@app.get("/tasks")
def get_all_tasks(user_id: int):

    return task_repo.get_all_tasks(user_id)


@app.get("/tasks/{task_id}")
def get_one_task(user_id: int, task_id: int):

    task = task_repo.get_one_task(task_id, user_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.post("/tasks")
def create_task(task: CreateTask):

    return task_repo.create_task(task)


@app.patch("/tasks/{task_id}")
def update_task(user_id: int, task_id: int, new_data: BaseTask):

    task = task_repo.update_task(task_id, user_id, new_data)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.patch("/tasks/{task_id}/toggle")
def toggle_task(task_id: int, user_id: int):

    task = task_repo.toggle_task_status(task_id, user_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user_id: int):

    deleted = task_repo.delete_task(task_id, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted"}



















# class User(BaseModel):
#     id: int
#     name: str
#     age: int

# class Task(BaseModel):
#     id: int
#     name: str
#     do_until: str
#     author: User

# class TaskCreate(BaseModel):
#     title: str
#     body: str
#     author_id: int

# class UserCreate(BaseModel):
#     name: Annotated[str,Field(...,title='name',min_length=1,max_length=25)]
#     age: Annotated[int,Field(..., title='age',ge=1,le=100)]



# users = [
#     {"id": 1, "name": "Antony", "age":33},
#     {"id": 2, "name": "Demon", "age":22},
#     {"id": 3, "name": "Grinch", "age":43},
# ]

# exercises = [
#     {"id": 1, "name": "Buy milk", "do_until": "2026-03-20","author":users[0]},
#     {"id": 2, "name": "Learn FastAPI", "do_until": "2026-03-21","author":users[1]},
#     {"id": 3, "name": "Workout", "do_until": "2026-03-22","author":users[2]},
# ]



# @app.get("/tasks")
# def tasks() -> List[Task]:
#     return [Task(**task) for task in exercises]

# @app.post("/tasks/add")
# def add_item(task: TaskCreate) -> Task:
#     author = next((user for user in users if user["id"] == task.author_id), None)
#     if not author:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     new_task_id = len(exercises) + 1

#     new_task = {"id" :new_task_id,"name": task.title,"do_until":task.body,"author": author}
#     exercises.append(new_task)
#     return Task(**new_task)



# @app.post("/user/add")
# def add_user(user: Annotated[UserCreate,Body(...,example={"name": "Username","age":1})]) -> User:
    
#     new_user_id = len(users) + 1

#     new_user = {"id" :new_user_id,"name": user.name ,"age":user.age,}
#     users.append(new_user)
#     return User(**new_user)


# @app.get("/tasks/{id}")
# def one_task(id: Annotated[int,Path(..., title="12345", ge=1)]) -> Task:
#     for task in exercises:
#         if task["id"] == id:
#             return Task(**task)
    
#     raise HTTPException(status_code=404, detail="Not Found")

# @app.get("/search")
# def search(post_id: Annotated[Optional[int],Query(title="54321",)]) -> Dict[str, Optional[Task]]:
#     if post_id:
#         for task in exercises:
#             if task["id"] == post_id:
#                 return {"data" : Task(**task)}
           
#         raise HTTPException(status_code=404, detail="Not Found")
#     else:
#         return {"data": None}