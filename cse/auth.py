import bcrypt
import psycopg2
from config import load_config

config = load_config()
conn = psycopg2.connect(**config)

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def authenticate_user(user_id: int, password: str):
    cursor = conn.cursor()
    cursor.execute("SELECT PASSWORD FROM STUDENT WHERE ID = %s;", (user_id,))
    record = cursor.fetchone()
    cursor.close()
    if record is None:
        return False
    return verify_password(password, record[0])
