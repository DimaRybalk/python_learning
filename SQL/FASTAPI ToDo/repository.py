from models import CreateTask,CreateUser,User,Task,BaseTask
from typing import Optional
from database import data


class UserRepository:
    def __init__(self):
        pass

    def get_user_by_email(self, user_email: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE email = ?"
        user = data.execute(query,(user_email,)).fetchone()
        if user:
            return User(**dict(user))
        return None
        
    def create_user(self,user: CreateUser) -> User:
        existed_user = self.get_user_by_email(user.email)
        if existed_user:
            return None
        
        query = "INSERT INTO users (email,password) VALUES (?,?)"
        cursor = data.execute(query,(user.email, user.password,))
        data.connection.commit()
        new_id = cursor.lastrowid
        return User(id=new_id, email=user.email, password=user.password)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = "SELECT * FROM users WHERE id = ?"
        user = data.execute(query,(user_id,)).fetchone()
        if user:
            return User(**dict(user))
        return None


    def login(self,email:str, password:str) -> Optional[User]:
        user_data = self.get_user_by_email(email)
        if not user_data:
            return None

        if password == user_data.password:
            return user_data
        
        return None


class TaskRepository:
    def __init__(self):
        pass

    def create_task(self, task: CreateTask) -> Task:
        query = "INSERT INTO tasks (name, description, user_id) VALUES (?, ?, ?)"
        cursor = data.execute(query, (task.name, task.description, task.user_id,))
        data.connection.commit()
        new_id = cursor.lastrowid

        return self.get_one_task(new_id, task.user_id)

    def toggle_task_status(self,task_id: int, user_id: int) -> Optional[Task]:
        task = self.get_one_task(task_id, user_id)
        if task:
            new_status = not task.is_complete
            query = "UPDATE tasks SET is_complete = ? WHERE id = ? AND user_id = ?"
            data.execute(query, (int(new_status), task_id, user_id))
            data.connection.commit()
            return self.get_one_task(task_id, user_id)
        return None

    def update_task(self,task_id: int, user_id: int, data_task: BaseTask) -> Optional[Task]:
        task = self.get_one_task(task_id, user_id)
        if task:
            query = "UPDATE tasks SET name = ? , description = ? WHERE id = ? AND user_id = ?"
            data.execute(query,(data_task.name, data_task.description, task_id,user_id))
            data.connection.commit()
            return self.get_one_task(task_id,user_id)
        
        return None

    def get_one_task(self,task_id: int, user_id: int) -> Optional[Task]:
        query = "SELECT * FROM tasks WHERE id = ? AND user_id = ?"
        task = data.execute(query,(task_id,user_id,)).fetchone()
        if task:
            return Task(**dict(task))
        
        return None

    def get_all_tasks(self, user_id: int) -> list[Task]:
        query = "SELECT * FROM tasks WHERE user_id = ?"
        tasks = data.execute(query,(user_id,)).fetchall()
        if not tasks:
            return []
        
        return [Task(**dict(task)) for task in tasks]

    def delete_task(self,task_id: int, user_id: int) -> bool:
        task = self.get_one_task(task_id,user_id)
        if not task:
            return False
        
        query = "DELETE FROM tasks WHERE id = ? AND user_id = ?"
        data.execute(query,(task_id,user_id,))
        data.connection.commit()
        return True