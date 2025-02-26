from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# 1. PostgreSQL 연결 정보 설정
# postgresql://사용자이름:비밀번호@호스트 주소:기본포트:연결할 DB이름
DATABASE_URL = "postgresql://postgres:tiger@localhost:5432/postgres"

# 2. SQLAlchemy 엔진 생성 > PostgreSQL DB에 연결
engine = create_engine(DATABASE_URL)

# 3. 기본 베이스 클래스 생성 > ORM의 기반이 되는 클래스인 Base 생성
#    DB 테이블과 Python 클래스 간의 매핑을 정의
Base = declarative_base()

# 4. 테이블 클래스 정의 (예: User 테이블)
class User(Base):
    __tablename__ = 'users' # 생성될 테이블 이름

    # 각 테이블 컬럼 정의
    id = Column(Integer, primary_key=True, index=True, nullable=False)  # 기본 키로 사용될 id 컬럼
    name = Column(String, index=True, nullable=False)
    username = Column(String, index=True, nullable=False, unique=True)
    age = Column(Integer)

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
def create_user(db_session, name: str, username: str, age: int):
    db_user = User(name=name, username=username, age=age) # user 객체 생성
    db_session.add(db_user) # session에 객체 추가
    db_session.commit() # DB에 반영
    db_session.refresh(db_user) # DB에서 다시 값을 불러옴
    return db_user # 생성된 객체 반환

# 8. 세션을 이용한 DB 작업
# 세션 객체로 DB에서 데이터를 조회하거나 추가, 수정, 삭제하는 작업을 수행하는 데 사용
if __name__ == "__main__":
    # 세션 시작
    # 새로운 세션 객체를 생성
    # 세션 객체는 DB에서 데이터를 조회하거나 추가, 수정, 삭제하는 작업을 수행하는 데 사용
    db = SessionLocal()

    try:
        # 새로운 사용자 생성
        new_user = create_user(db, "홍길동", "hong112", 30)
        print(f"새로 생성된 사용자: {new_user.name}, {new_user.username}, {new_user.age}")
    except SQLAlchemyError as e:
        print(f"DB 작업 중 오류: {e}")
    finally:
        # 세션 종료
        db.close()