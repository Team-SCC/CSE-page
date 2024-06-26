# 데이터베이스 ORM

## Students 데이터베이스 생성

```sql
CREATE TABLE students (
    SID INT PRIMARY KEY,
    name VARCHAR(16) NOT NULL,
    gender VARCHAR(6) CHECK (gender IN ('male', 'female')),
    grade INT,
    phone VARCHAR(13),
    birth DATE NOT NULL,
    email VARCHAR(30) NOT NULL,
    password VARCHAR(1024),
    nickname VARCHAR(16),
    auth INT NOT NULL CHECK (auth IN (0, 1, 2))
);
```

## 비밀번호 제약조건을 위한 함수, 트리거 생성

### 함수 생성

```sql
CREATE OR REPLACE FUNCTION set_default_password() RETURNS TRIGGER AS $$
BEGIN
  IF NEW.PASSWORD IS NULL THEN
    NEW.PASSWORD := TO_CHAR(NEW.BIRTH, 'YYMMDD');
  END IF;  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 트리거 생성

```sql
CREATE TRIGGER insert_student
BEFORE INSERT ON STUDENTS
FOR EACH ROW
EXECUTE FUNCTION set_default_password();
```

- 트리거 함수 생성 후 트리거 생성
- 트리거 생성 후 트리거가 실행될 조건을 생성
- $$ 새로운 본문의 시작과 끝 지정
- Plpgsql: PostgresSQL Procedural Language/PostgresSQL, 함수가 작성된 언어를 지정 해당 코드에서는 PostgreSQL 이라 지정

## 세션 데이터베이스

### 세션 데이터베이스 생성

```sql
CREATE TABLE SESSIONS(
  ID SERIAL PRIMARY KEY,
  UUID INT NOT NULL,
  SID INT,
  FOREIGN KEY (SID) REFERENCES STUDENTS(SID)
);
```

### 학생 데이터 삽입 쿼리문

```sql
INSERT INTO STUDENTS (SID, NAME, BIRTH, EMAIL, AUTH) VALUES (20204062, ‘이인규’, ‘2001-03-04’, ‘dldlsrb1414@gmail.com’ 3);
```

## 파이썬에서 ORM 코드 작성

### 데이터베이스 기본 연결 코드

```python
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

if __name__ == '__main__':
    config = load_config()
    print(config)
```

### 테이블에 레코드 삽입

```python
import psycopg2

# sid | name | gender | grade | phone | birth | email | password | nickname | auth 
command = '''INSERT INTO STUDENTS(SID, NAME, BIRTH, EMAIL, AUTH) VALUES(20204062, '이인규', '010304', 'dldlsrb1414@gmail.com', 2)'''
student_id = None
config = load_config()

try:
    command += " RETURNING SID;"
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(command)
            rows = cur.fetchone()
            if rows:
                student_id = rows[0]
                
            conn.commit()
            conn.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    print(student_id)
```

```shell
connection already closed
20204062
```

```sql
csepage=# select * from students;
   sid    |  name  | gender | grade | phone |   birth    |         email         | password | nickname | auth 
----------+--------+--------+-------+-------+------------+-----------------------+----------+----------+------
 20204062 | 이인규 |        |       |       | 2001-03-04 | dldlsrb1414@gmail.com | 010304   |          |    2
(1개 행)
```

## 문제해결

```text
close()를 하지 않으면, 데이터베이스 쿼리문은 다른 곳에서 반응하지 않고 대기함
데이터베이스 조회 명령어 \l
테이블 조회 명령어 \d
데이터베이스 변경 명령어 \c
```
