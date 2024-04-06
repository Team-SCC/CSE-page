# 공부한 내용 정리

## FastAPI Docs - 파이썬 타입 소개

### Pydantic 모델

- Pydantic은 데이터 검증(validation)을 위한 라이브러리입니다.
- FastAPI는 모두 Pydantic 기반으로 만들어져 있다.
- Pydantic 사용시 개발시에 더 많은 에디터의 도움을 받을 수 있다.

### Pydantic 사용법

```python
from typing import List, Union
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    number: int | None = None
    friends: List[str] = []class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

user = User({
    "id": 1,
    "name": "LeeInGyu",
    "number": None,
    "friends": ["Lee", "Jung"],
})

print(User(user))
```

> 위와 같은 방식으로 작성 가능하다.

```python
me = User(user)

print(me.id)
print(me.name)
```

> 위의 방식대로 에디터의 도움을 받을 수 있어 편리하다.

---

## FastAPI Docs - 동시성과 async / await

### 비동기 코드란?

- 느린 I/O 작업에 묶이지 않고, 다른 일을 할 수 있게 작성하는 코드

### FastAPI에서 비동기 코드 적용

```python
results = await slow_io_task()

@app.get('/')
async def read_results():
    results = await slow_io_task() # await 키워드는 async 함수 내부에서만 사용 가능
    return results
```

> 이 방식대로 코드를 작성하면 비동기식으로 코드가 작동하게 된다.

### 코루틴 Coroutine

- ***비선점적 멀티태스킹***을 위한 ***서브 루틴***을 일반화한 컴퓨터 프로그램 구성요소
- 병행성은 지원하지만, 병렬성은 지원하지 않는다.
- 루틴간의 협력을 통한 비선점적 멀티태스킹 가능
- 동시성 지원프로그래밍 지원(2개 이상의 프로세스가 동시에 계산을 진행하는 상태)

> 기능을 메모리에 모아져있고, **호출시 해당 메모리로 이동한 후 반환되면 원래위치로 돌아오는** ***서브루틴*** 과 다르게 ***코루틴***은 기능이 메모리에 모아져있고, **호출 후 반환문이 없어도 동작을 중단하고 이후에 해당지점에서 진행재개 가능**하다.

#### 비선점적 멀티태스킹이란?

- 프로세스가 CPU를 할당 받으면 다른 프로세스가 차지 불가한 것

#### 3가지 루틴의 비교

- 메인루틴: 메인으로 실행되는 흐름
- 서브루틴: 서브로 실행되는 흐름(함수 호출)
- 코루틴: 비동기식으로 실행되는 흐름

---

## FastAPI Docs - 첫걸음

### 초기 라이브러리 설치

```bash
pip install "fastapi[all]"

or

pip install fastapi
pip install uvicorn
```

> 위의 설치 명령어는 fastapi의 모든 관련 패키지를 다운로드 하는 명령어이고, 아래는 최소한으로 필요한 라이브러리 목록이다. 나는 "[all]"을 설치하였다.

### uvicorn 이란?

- 비동기 서버 인터페이스 제공 라이브러리
- ***ASGI(Asynchronous Server Gateway Interface)*** 서버
- 기존의 표준이었던 **WSGI(Web Server Gateway Interface) 서버**가 비동기 지원을 하지 않아서 ASGI 서버를 사용한다.

> fastapi는 설치하지만, uvicorn은 무엇이길래 설치하나? 궁금해져서 찾아보았다.

### 기본 코드

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

> 라이브러리가 설치되어 있을 때, 파일명은 **main.py**로 한 후, 해당 코드를 작성하면 된다.

### 실행 명령어

```bash
uvicorn main:app --reload 
```

- uvicorn: 비동기 서버 인터페이스 라이브러리
- main: 실행하는 파이썬 파일명
- app: FastAPI() 인스턴스 생성
- --reload: 코드 변경시 자동으로 서버 재시작(디버깅, 개발 시에만 사용)

### 일반적인 CRUD 메소드

#### Create, 데이터 생성

```python
@app.post("/")
async def root():
    return {"message": "Hello World"}
```

- post 키워드를 사용한다.

 #### Read, 데이터 읽기

```python
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

- get 키워드를 사용한다.

#### Update, 데이터 수정

```python
@app.put("/")
async def root():
    return {"message": "Hello World"}
```

- put 키워드를 사용한다.

#### Delect, 데이터 삭제

```python
@app.delete("/")
async def root():
    return {"message": "Hello World"}
```

- delete 키워드를 사용한다.

### FastAPI 개발 docs

```url
localhost:port/docs
```

- 내가 개발한 API 문서를 제공하는 곳

### FastAPI 개발 redoc

```url
localhost:port/redoc
```

- 대안 자동 문서를 제공하는 곳

> 대안 자동 문서란 Alternative auto documentation으로 APi 문서를 자동으로 만들어주는 도구이다.

### docs, redoc 차이점

- docs: Swagger UI, 사용자 친화적 인터페이스
- redoc: ReDoc UI, 좀 더 직관적인 인터페이스

> 열심히 찾아봤지만, Swagger UI의 특징과 ReDoc UI의 특징은 딱히 없는듯...

---

## FastAPI Docs - 경로 매개변수

### 매개변수의 경로 지정

```python
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str): # 매개변수 지정
    return {"user_id": user_id}
```

```text
접속 url
localhost:port/users/me
localhost:port/users/{int}
```

- {int}에는 아무 정수를 넣으면 된다.
- "" 같은 것을 같이 넣지 않아도 숫자를 넣으면 int 형으로 인식한다.

> 기본적으로 경로를 지정하는 방법이며, 동적으로 경로를 변경하고 싶을 때에는 ***매개변수***로 전달해 url을 동적으로 생성하면 된다.

### Enum, 열거형 사용

- Python 3.4 이후 사용 가능하다.
- 파이썬의 List와 다르게 ***타입 안정성(의도와는 다른 타입으로 지정될 가능성)***을 지원한다.
- s코드의 유지보수성이 증가한다.

> 열거형이란 순서가 있는 인스턴스를 의미한다. 사용 예시로는 (배송전 - 배송중 - 배송완료) 같은 순서가 정해진 곳에서 사용

```python
from enum import Enum

class ModelName(MemberDtype, Enum):
    member1 = value1
    member2 = value2
    ...
```

```python
from enum import Enum

class Delivery(str, Enum): # 열거형의 멤버들은 str형을 가진다.
    before = "배송전"
    ing = "배송중"
    after = "배송후"
```

> 위와 같이 사용 가능하다. FastAPI에서 이런 부분을 계속 강조하는 것보니 데이터의 타입 안정성을 매우 중요하게 생각하는 것 같다.

### 파일 경로 매개변수로 전달

```python
@app.get("/files/{file_path: path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

> 테스트를 해봤는데, 파일에 어떻게 접근해야되는지는 아직 모르겠다.
> 나중에 다시 수정해야될 것 같다.

---
