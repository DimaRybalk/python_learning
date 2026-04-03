from database.database import data
from models.transaction import Transaction
from datetime import datetime

class TransactionsRepository:

    def get_all_transactions(self):
        return data.execute(
            "SELECT * FROM transactions"
        ).fetchall()


    def find_transactions_by_id(self, id: int):
        return data.execute(
            "SELECT * FROM transactions WHERE id = ?",
            (id,)
        ).fetchone()


    def get_transaction_by_user(self, user_id: int):
        query = "SELECT * FROM transactions WHERE user_id = ?"
        return data.execute(query, (user_id,)).fetchall()


    def create_transaction(self, transaction: Transaction):
        query = """
        INSERT INTO transactions
        (user_id, category_id, amount, date, descriptions, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        data.execute(query, (
            transaction.user_id,
            transaction.category_id,
            transaction.amount,
            transaction.date,
            transaction.descriptions,
            transaction.created_at
        ))

        data.connection.commit()


    def update_transaction(self, transaction: Transaction):
        transaction_exists = self.find_transactions_by_id(transaction.id)

        if not transaction_exists:
            print("Транзакция не существует")
            return

        query = """
        UPDATE transactions
        SET user_id = ?, category_id = ?, amount = ?, date = ?, descriptions = ?
        WHERE id = ?
        """

        data.execute(query, (
            transaction.user_id,
            transaction.category_id,
            transaction.amount,
            transaction.date,
            transaction.descriptions,
            transaction.id
        ))

        data.connection.commit()


    def delete_transaction(self, transaction_id: int):
        transaction_exists = self.find_transactions_by_id(transaction_id)

        if not transaction_exists:
            print("Транзакция не существует")
            return

        data.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )

        data.connection.commit()

    def get_transactions_by_date(self,user_id,start_date,end_date):
            query = ("SELECT * FROM transactions WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date DESC")
            results =  data.execute(query, (user_id,start_date,end_date)).fetchall()

            if not results:
                print(f"Транзакции за период с {start_date} по {end_date} не найдены.")
        
            return results
    

    def get_today_transactions(self, user_id: int):
        today = datetime.now().strftime("%Y-%m-%d")
        query = "SELECT * FROM transactions WHERE user_id = ? AND date = ?"
        results = data.execute(query, (user_id, today)).fetchall()
        if not results:
            print(f"Транзакции за период {today} не найдены.")
        
        return results

    def get_monthly_transactions(self, user_id: int):
        current_month = datetime.now().strftime("%Y-%m-%")
        query = "SELECT * FROM transactions WHERE user_id = ? AND date LIKE ?"
        results = data.execute(query, (user_id, current_month)).fetchall()
        if not results:
            print(f"Транзакции за период {current_month} не найдены.")
        
        return results 
    
    def get_this_year_transactions(self,user_id: int):
        current_year = datetime.now().strftime("%Y-%")
        query = "SELECT * FROM transactions WHERE user_id = ? AND date LIKE ?"
        results = data.execute(query, (user_id, current_year)).fetchall()
        if not results:
            print(f"Транзакции за период {current_year} не найдены.")
        
        return results 
    
    def get_totals(self, user_id: int):
        query = """
        SELECT 
        SUM(CASE WHEN c.type = 'income' THEN t.amount ELSE 0 END) as income,
        SUM(CASE WHEN c.type = 'expense' THEN t.amount ELSE 0 END) as expense 
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ?
        """
    
        result = data.execute(query, (user_id,)).fetchone()
    
        return {
        "income": result[0] if result[0] else 0,
        "expense": result[1] if result[1] else 0,
        "balance": (result[0] or 0) - (result[1] or 0)
        }