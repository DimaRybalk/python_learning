from database.database import data
from models.category import Category


class CategoryRepository:

    def create_category(self, category: Category):

        category_exists = self.find_category_by_name(category.name)

        if category_exists:
            print(f"Категория '{category.name}' уже существует")
            return

        query = "INSERT INTO categories (name, type) VALUES (?, ?)"

        cursor = data.execute(query, (
            category.name,
            category.type
        ))

        data.connection.commit()

        return cursor.lastrowid


    def find_category_by_id(self, id: int):
        return data.execute(
            "SELECT * FROM categories WHERE id = ?",
            (id,)
        ).fetchone()


    def find_category_by_name(self, name: str):
        return data.execute(
            "SELECT * FROM categories WHERE name = ?",
            (name,)
        ).fetchone()


    def get_all_categories(self):
        return data.execute(
            "SELECT * FROM categories"
        ).fetchall()


    def delete_category(self, category_id: int):

        if not self.find_category_by_id(category_id):
            print("Категория не найдена")
            return

        data.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,)
        )

        data.connection.commit()


    def update_category(self, category: Category):

        if not self.find_category_by_id(category.id):
            print("Категория не найдена")
            return

        query = "UPDATE categories SET name = ?, type = ? WHERE id = ?"

        data.execute(query, (
            category.name,
            category.type,
            category.id
        ))

        data.connection.commit()