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


# 임시
session_data = {
    "example_session_id": {"id": 1}
}

def generate_session_id():
    return str(uuid4())

async def get_user(session_id: Optional[str] = Cookie(None)):
    if session_id is None or session_id not in session_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="세션이 유효하지 않습니다.")
    return {"id": session_data[session_id]["id"]}

@app.post("/login/")
async def login(username: Optional[str] = None, session_id: Optional[str] = Cookie(None)):
    if session_id:
        # 세션이 유효한지 확인
        try:
            user = await get_user(session_id)
            return {"message": "세션이 유효합니다.", "user_id": user["id"]}
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username이나 유효한 session_id가 필요합니다.")

    if username:
        # 사용자 이름이 제공되었을 경우 세션 생성
        new_session_id = generate_session_id()
        user_id = ...  # 사용자의 ID를 가져오는 로직 필요 (예: 데이터베이스 조회)
        session_data[new_session_id] = {"id": user_id}
        
        # 쿠키로 세션 아이디를 전달
        response = {"message": "로그인 성공", "session_id": new_session_id}
        
        # 쿠키에 HttpOnly 속성을 추가하여 JavaScript에서 접근할 수 없게 만듦
        cookie = f"session_id={new_session_id}; Path=/; HttpOnly"
        
        return response, {"headers": {"Set-Cookie": cookie}}
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username이나 유효한 session_id가 필요합니다.")


# 학생 등록 - (수정) 나중에 파일 올리면 등록되게 하는것으로 수정
@app.post("/student/info/")
async def register_user(user: schemas.UserCreate):
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
async def update_user(user_id: int, user: schemas.UserUpdate, session_id: Optional[str] = Cookie(None)):
    await get_user(session_id)
    
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