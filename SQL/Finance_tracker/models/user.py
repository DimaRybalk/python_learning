from datetime import datetime
import hashlib

class User:
    def __init__(self,id,email,password,created_at=None):
        self.id = id
        self.email = email
        self.password = self._hash_password(password)
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()