# fastapi-sessions
> session 이용해서 코드 작성한거 아니였어? 근데 더 공부해보니 fastapi-sessions가 있다는걸 알게 되었다 일단 이해를 위해 문서에 있는 코드를 이해하자

### 설치
```python
pip install fastapi-sessions
```

### 기본 사용법
* SessionFrontend 추상 클래스
  * 쿠키, 헤더 등 요청에서 세션 ID를 추출하기 위함
* SessionBackend 추상 클래스
  * CRUD 작업을 위한 인터페이스 제공
* SessionVerifer 추상 클래스
  * 세션 ID가 유효한지 확인

#### 1. 사용할 모델
```python
from pydantic import BaseModel

class SessionData(BaseModel):
    username: str
```

#### 2. Session Frontend
```python
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

# CookieParameters: 쿠키의 구성 지정
cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie", # 쿠키 이름
    identifier="general_verifier", # 세션을 식별하는 데 사용
    auto_error=True, # 세션을 확인하고 실패하면 오류 반환 여부
    secret_key="DONOTUSE", # 세션을 서명하기 위함
    cookie_params=cookie_params, # CookieParameters 클래스의 인스턴스
)
"""
 "cookie"라는 이름의 세션 쿠키를 생성하고, 해당 쿠키의 식별자를 "general_verifier"로 설정하며, 세션을 자동으로 확인하고 오류를 반환하도록 설정한다. 세션의 서명에 사용될 비밀 키는 "DONOTUSE"로 설정되었고, 쿠키의 구성은 기본값을 사용한다
"""
```

#### 3. Session Backend
```python
from uuid import UUID
from fastapi_sessions.backends.implementations import InMemoryBackend

# UUID: 세션 식별자
# SessionData: 세션에 저장될 데이터 모델. 앞서 정의한 SessionData 클래스를 의미
backend = InMemoryBackend[UUID, SessionData]()
```
* 여기서 InMemoryBackend란?
  * 개발 및 테스트를 위해 사용 실제 운영할 때는 데이터베이스를 사용해야 함 model 정의 끝나면 수정 예정
  * 간단한 구현 : 메모리에 데이터를 저장하므로 별도의 데이터베이스 설정이 필요 X
  * 서버 재시작시 초기화 : 서버를 재시작하면 메모리 내의 모든 세션 데이터가 삭제

#### 4. Session Verifier
```python
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi import HTTPException

# SessionVerifier를 상속받아 세션을 검증하는 기능을 구현
class BasicVerifier(SessionVerifier):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: SessionBackend,
        auth_http_exception: HTTPException,
    ):
        # 이 값은 세션 쿠키의 이름과 동일하게 설정
        self._identifier = identifier
        # 세션이 유효하지 않을 경우 자동으로 오류를 반환할지 여부
        self._auto_error = auto_error
        # 세션 데이터를 저장하는 백엔드, 위에 정의
        self._backend = backend
        # 인증 오류가 발생했을 때 반환할 HTTP 예외입니다. 일반적으로 401(Unauthorized)이나 403(Forbidden) 등이 사용
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    async def verify_session(self, session_id: str) -> bool:
        """Check if the session exists and is valid"""
        return await self._backend.exists(session_id)


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="Invalid session"),
)

```


### 참고자료
* [fastapi-session 문서](https://jordanisaacs.github.io/fastapi-sessions/guide/getting_started/)