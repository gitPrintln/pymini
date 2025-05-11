from sqlalchemy import create_engine, Column, Integer, Numeric, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

# 1. PostgreSQL 연결 정보 설정
# postgresql://사용자이름:비밀번호@호스트 주소:기본포트:연결할 DB이름
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"

# 2. SQLAlchemy 엔진 생성 > PostgreSQL DB에 연결
engine = create_engine(
            DATABASE_URL,
            pool_size=10,  # 풀 크기
            max_overflow=20,  # 풀을 초과한 커넥션 수
            pool_timeout=30,  # 커넥션을 얻기 위한 최대 대기 시간
            pool_recycle=1800,  # 커넥션 재사용 시간 (초)
)

# 3. 기본 베이스 클래스 생성 > ORM의 기반이 되는 클래스인 Base 생성
#    DB 테이블과 Python 클래스 간의 매핑을 정의
Base = declarative_base()

# 4. 테이블 클래스 정의
class Nutrient(Base):
    __tablename__ = "NUTRIENT"
    nutrient_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)

class Age(Base):
    __tablename__ = "AGE"
    age_id = Column(Integer, primary_key=True)
    age_min = Column(Integer, nullable=False)
    age_max = Column(Integer, nullable=False)
    label = Column(String(20), nullable=False)

class Sex(Base):
    __tablename__ = "SEX"
    sex_id = Column(Integer, primary_key=True)
    sex_code = Column(String(10), nullable=False, unique=True)

class NutrientRef(Base):
    __tablename__ = "NUTRIENT_REFERENCE"
    nutrient_id  = Column(Integer, ForeignKey("NUTRIENT.nutrient_id"), primary_key=True)
    age_id       = Column(Integer, ForeignKey("AGE.age_id"), primary_key=True)
    sex_id       = Column(Integer, ForeignKey("SEX.sex_id"), primary_key=True)
    rda_amount   = Column(Numeric(10, 3))
    ul_amount    = Column(Numeric(10, 3))
    ai_amount   = Column(Numeric(10, 3))

class CalorieRef(Base):
    __tablename__ = "CALORIE_REFERENCE"
    age_id       = Column(Integer, ForeignKey("AGE.age_id"), primary_key=True)
    sex_id       = Column(Integer, ForeignKey("SEX.sex_id"), primary_key=True)
    kcal         = Column(Integer, nullable=False)


# 5. DB 연결 및 세션 생성
#    세션은 데이터베이스 트랜잭션을 관리하고, 데이터베이스에 쿼리를 실행하는 작업을 처리
#    autocommit=False: 이 설정은 트랜잭션이 자동으로 커밋되지 않도록 한다/기본값은 False
#                      명시적으로 commit()호출할 때만 DB에 반영
#    autoflush=False: 이 설정은 세션이 자동으로 플러시되지 않도록 한다/기본적으로 True로 설정
#                      False로 설정하면 세션의 변경사항을 명시적으로 플러시할 때까지 데이터베이스에 반영되지 않음.
#    bind=engine: engine은 SQLAlchemy의 데이터베이스 연결 객체/세션을 어느 데이터베이스에 연결할지 결정
#    SessionLocal은 세션을 생성할 수 있는 함수/실제로 세션 객체를 생성할 때 사용
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. 테이블 생성
Base.metadata.create_all(bind=engine)

# 7. 데이터 삽입

# 8. 세션을 이용한 DB 작업
# 세션 객체로 DB에서 데이터를 조회하거나 추가, 수정, 삭제하는 작업을 수행하는 데 사용
if __name__ == "__main__":
    # 세션 시작
    # 새로운 세션 객체를 생성
    # 세션 객체는 DB에서 데이터를 조회하거나 추가, 수정, 삭제하는 작업을 수행하는 데 사용
    db = SessionLocal()
