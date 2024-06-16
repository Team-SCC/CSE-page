from fastapi import FastAPI, HTTPException
import bcrypt
import psycopg2

from config import load_config
import schemas

app = FastAPI()

# 데이터베이스 연결 설정
config = load_config()
conn = psycopg2.connect(**config)