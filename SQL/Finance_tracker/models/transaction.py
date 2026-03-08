from datetime import datetime

class Transaction:
    def __init__(self, id, user_id, category_id, amount, date, descriptions, created_at):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount

        if isinstance(date, datetime):
            self.date = date.strftime("%Y-%m-%d")
        else:
            self.date = date

        self.descriptions = descriptions
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")