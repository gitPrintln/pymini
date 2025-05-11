from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# 1. PostgreSQL 연결 정보 설정
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"

# 2. SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL)

# 3. 기본 베이스 클래스 생성
Base = declarative_base()

# 4. 테이블 클래스 정의 (예: User 테이블)
class standard_calorie_data(Base):
    __tablename__ = 'standard_calorie_data' # 생성될 테이블 이름

    # 각 테이블 컬럼 정의
    id = Column(Integer, primary_key=True, index=True, nullable=False)  # 기본 키로 사용될 id 컬럼
    age_group = Column(String, index=True)
    gender = Column(String, index=True)
    calorie = Column(Integer)

# 5. DB 연결 및 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. 테이블 생성
Base.metadata.create_all(bind=engine)

# 7. 데이터 삽입
def create_standard_calorie(db_session, age_group: str, gender: str, calorie: int):
    db_standard_calorie = standard_calorie_data(age_group=age_group, username=gender, calorie=calorie)
    db_session.add(db_standard_calorie) # session에 객체 추가
    db_session.commit() # DB에 반영
    db_session.refresh(db_standard_calorie) # DB에서 다시 값을 불러옴
    return db_standard_calorie # 생성된 객체 반환

# 기준점 설정(한국영양학회(KDRIs, 한국인 영양소 섭취기준) 2020)
# 1일 권장 칼로리(에너지 필요량), 1일 영양소 권장량(탄:단:지 = 5:3:2 비율)
# 하루 물 섭취량(남:2.5L,여:2L 이상)
# 1일 권장 칼로리 데이터
calorie_data = {
    "연령대": ["19~29세", "30~49세", "50~64세"],
    "남성 (낮음)": [2400, 2300, 2100],
    "남성 (보통)": [2700, 2600, 2400],
    "남성 (높음)": [3000, 2900, 2700],
    "여성 (낮음)": [1900, 1800, 1700],
    "여성 (보통)": [2100, 2000, 1900],
    "여성 (높음)": [2400, 2300, 2200]
}

# 8. 세션을 이용한 DB 작업(칼로리 작업)
db = SessionLocal()
try:
    for i, age in enumerate(calorie_data["연령대"]):
        for key, values in calorie_data.items():
            if key != "연령대":
                gender = key.split(" ")[0]
                
                record = standard_calorie_data(
                    age_group = age,
                    gender = gender,
                    calorie = values[i]
                )
                
                db.add(record)
    db.commit()
except Exception as e:
    db.rollback()  # 오류 발생 시 롤백
    print("데이터 삽입 오류: ", e)
finally:
    db.close()
    
# 9. 세션을 이용한 DB 작업(영양소 작업)
try:
    print("dbcommit")
    # db.commit()
except Exception as e:
    db.rollback()  # 오류 발생 시 롤백
    print("데이터 삽입 오류: ", e)
finally:
    db.close()