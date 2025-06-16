from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# PostgreSQL 연결 정보 설정
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"

# SQLAlchemy 엔진 생성 > PostgreSQL DB에 연결
engine = create_engine(
            DATABASE_URL,
            connect_args={"client_encoding": "utf8"},
            pool_size=10,  # 풀 크기
            max_overflow=20,  # 풀을 초과한 커넥션 수
            pool_timeout=30,  # 커넥션을 얻기 위한 최대 대기 시간
            pool_recycle=1800,  # 커넥션 재사용 시간 (초)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DB 연결 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()