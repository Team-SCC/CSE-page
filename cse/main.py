from fastapi import FastAPI, HTTPException, Depends, status, Cookie
import bcrypt
import psycopg2
from typing import Optional
from uuid import uuid4

from config import load_config
import schemas

app = FastAPI()

# 데이터베이스 연결 설정
config = load_config()
conn = psycopg2.connect(**config)

# 학생 등록 - (수정) 나중에 파일 올리면 등록되게 하는것으로 수정
@app.post("/student/info/")
def register_user(user: schemas.UserCreate):
    cursor = conn.cursor()
    # 이미 존재하는지 확인
    cursor.execute(
        "SELECT COUNT(*) FROM STUDENT WHERE ID = %s OR EMAIL = %s;",
        (user.id, user.email)
    )
    result = cursor.fetchone()
    if result[0] > 0:
        raise HTTPException(status_code=400, detail="입력한 ID 또는 Email이 이미 존재합니다.")
    
    # 비밀번호 암호화
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # 데이터베이스에 사용자 정보 저장
    cursor.execute(
        "INSERT INTO STUDENT (ID, NAME, EMAIL, PASSWORD, AUTH) "
        "VALUES (%s, %s, %s, %s, %s);",
        (user.id, user.name, user.email, hashed_password, user.auth)
    )
    conn.commit()
    cursor.close()
    
    return {"message": "successfully"}

# 학생 정보 수정
@app.put("/student/info/{user_id}/")
def update_user(user_id: int, user: schemas.UserUpdate):
    # 비밀번호 암호화
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE STUDENT SET NAME = %s, GENDER = %s, GRADE = %s, PHONE = %s, BIRTH = %s, "
        "EMAIL = %s, PASSWORD = %s, NICKNAME = %s WHERE ID = %s;",
        (user.name, user.gender, user.grade, user.phone, user.birth, user.email, hashed_password, user.nickname, user_id)
    )
    conn.commit()
    cursor.close()
    return {"message": "successfully"}

# 임시
session_data = {}

def generate_session_id():
    return str(uuid4())

@app.post("/login/")
async def login(username: str):
    session_id = generate_session_id()
    session_data[session_id] = {"id": id}
    
    # 쿠키로 세션 아이디를 전달
    response = {"session_id": session_id}
    
    # 쿠키에 HttpOnly 속성을 추가하여 JavaScript에서 접근할 수 없게 만듦
    cookie = f"session_id={session_id}; Path=/; HttpOnly"
    
    print(session_id)
    
    return response, {"headers": {"Set-Cookie": cookie}}

# 클라이언트의 요청에 따라 세션 ID를 사용하여 세션 데이터를 반환하는 엔드포인트
@app.get("/user/")
async def get_user(session_id: Optional[str] = Cookie(None)):
    if session_id is None or session_id not in session_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="세션이 유효하지 않습니다.")
    return {"id": session_data[session_id]["id"]}