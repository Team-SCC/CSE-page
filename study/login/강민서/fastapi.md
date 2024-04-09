# 세션 적용하기

## 💻 코드

```python
from fastapi import FastAPI, HTTPException, Depends, status, Cookie
from typing import Optional
from uuid import uuid4

app = FastAPI()

# 세션 데이터를 저장할 딕셔너리(임시)
session_data = {}

# 세션 ID를 생성하는 함수
def generate_session_id():
    return str(uuid4())

# 세션을 생성하고 세션 ID를 클라이언트에게 전달하는 엔드포인트
@app.post("/login/")
async def login(username: str):
    session_id = generate_session_id()
    session_data[session_id] = {"username": username}
    
    # 쿠키로 세션 아이디를 전달
    response = {"session_id": session_id}
    return response, {"headers": {"Set-Cookie": f"session_id={session_id}; Path=/"}}  # 쿠키 설정

# 클라이언트의 요청에 따라 세션 ID를 사용하여 세션 데이터를 반환하는 엔드포인트
@app.get("/user/")
async def get_user(session_id: Optional[str] = Cookie(None)):
    if session_id is None or session_id not in session_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="세션이 유효하지 않습니다.")
    return {"username": session_data[session_id]["username"]}
```

### 🔎 uuid4가 뭐야?
>  UUID(Universally Unique Identifier)를 생성하기 위한 Python의 내장 모듈인 uuid 모듈에 있는 함수 중 하나다. UUID는 전 세계적으로 고유한 값을 생성하는 데 사용되는 표준 형식이다

> 주로 세션 식별자, 쿠키 값, 무작위 데이터베이스 키 등에 사용

#### 💡 일련의 번호를 사용해도 되지 않나...?
> uuid4는 무작위로 생성된 값이므로 예측하기 어려워 보안성을 강화할 수 있다

이외에도,,,
1. 고유성
2. 무작위성<br>: 완전히 무작위로 생성되므로 생성된 값에서 어떠한 정보도 추론할 수 없다
3. 이식성과 범용성<br>: 어떤 시스템이나 애플리케이션에서도 고유한 식별자로 사용될 수 있다

#### 💡 uuid4 어떻게 생겼을까..?
* x는 무작위로 생성된 16진수 숫자(0-9, a-f)로 채워진다
* y는 8, 9, a, b 중 하나의 값으로 설정

![alt text](./img/uuid.png)

#### 💡 겹치지 않을까?
> 340,282,366,920,938,463,463,374,607,431,768,211,456개의 사용 가능한 UUID가 존재한다 별의 개수보다 더 많다고 하니.. 걱정은 안해도 되겠죠..?

![alt text](./img/uuid별.png)


### 참고자료
* [uuid4란](https://yoonminlee.com/uuid-uniqueness-duplication)