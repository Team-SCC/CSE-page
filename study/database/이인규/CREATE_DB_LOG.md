# 데이터베이스 생성 로그

## postgres 사용자 데이터베이스 연결

```sql
sudo -u postgres psql
```

## 데이터베이스 유저 비밀번호 설정

```sql
ALTER USER postgres PASSWORD 'csepage20';
```

## 데이터베이스 생성

```sql
CREATE DATABASE CSE_PAGE_DB;
```

## 데이터베이스 나가기

```sql
\q
```

> 다음 할 것, 데이터베이스 접속 후 Student 테이블 생성
