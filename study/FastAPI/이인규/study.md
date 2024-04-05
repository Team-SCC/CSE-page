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
    friends: List[str] = []

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

