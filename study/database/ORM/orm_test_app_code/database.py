from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 Url 생성
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"ns
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"    

# SQLite에서 필요함, 하나의 쓰레드만 허용하는 SQLite가 동일한 연결을 공유하는 것을 방지하기 위함
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SQLAlchemy 엔진 만들기
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 데이터베이스 세션 인스턴스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델 또는 클래스 생성
Base = declarative_base()
