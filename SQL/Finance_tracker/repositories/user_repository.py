from database.database import data
from models.user import User


class UserRepository:

    def find_user_by_id(self, id: int):
        query = "SELECT * FROM users WHERE id = ?"
        return data.execute(query, (id,)).fetchone()


    def get_all_users(self):
        return data.execute("SELECT * FROM users").fetchall()


    def get_user_by_email(self, email: str):
        query = "SELECT * FROM users WHERE email = ?"
        return data.execute(query, (email,)).fetchone()


    def create_user(self, user: User):
        user_exists = self.get_user_by_email(user.email)

        if user_exists:
            print(f"Пользователь с email {user.email} уже существует")
            return

        query = "INSERT INTO users (email, password, created_at) VALUES (?, ?, ?)"

        data.execute(query, (
            user.email,
            user.password,
            user.created_at
        ))

        data.connection.commit()


    def update_user(self, user: User):
        user_exists = self.find_user_by_id(user.id)

        if not user_exists:
            print("Пользователь не найден")
            return

        fields_to_update = []
        values = []

        for key, value in user.__dict__.items():
            if key != "id" and value is not None:
                fields_to_update.append(f"{key} = ?")
                values.append(value)

        if not fields_to_update:
            print("Нет данных для обновления")
            return

        query = f"UPDATE users SET {', '.join(fields_to_update)} WHERE id = ?"

        values.append(user.id)

        data.execute(query, tuple(values))
        data.connection.commit()


    def delete_user(self, user: User):
        user_exists = self.find_user_by_id(user.id)

        if not user_exists:
            print("Пользователь не существует")
            return

        query = "DELETE FROM users WHERE id = ?"
        data.execute(query, (user.id,))
        data.connection.commit()