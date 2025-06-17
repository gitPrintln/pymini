from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database, config
from pydantic import BaseModel
from datetime import date

app = FastAPI()

# CORS 설정
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",  # 프론트 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 테이블 생성
models.Base.metadata.create_all(bind=database.engine)

# 일정 입력용 Pydantic 모델
# FastAPI는 요청 바디(body) 데이터를 받을 때, BaseModel을 상속한 클래스를 사용해 자동으로 데이터 유효성 검증(validation)을 해줌
class ScheduleCreate(BaseModel):
    date: date
    title: str
    memo: str | None = None

# 일정 등록
@app.post("/api/schedules/")
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(database.get_db)):
    db_schedule = models.Schedule(date=schedule.date, title=schedule.title, memo=schedule.memo)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return {"id": db_schedule.id, "message": "일정이 저장되었습니다."}

# 일정 보기
@app.get("/api/schedules/{schedule_date}")
def get_schedules(schedule_date: date, db: Session = Depends(database.get_db)):
    schedules = db.query(models.Schedule).filter(models.Schedule.date == schedule_date).all()
    return schedules


class ScheduleUpdate(BaseModel):
    title: str
    memo: str | None = None
# 일정 수정
@app.put("/api/schedules/{schedule_id}")
def update_schedule(schedule_id: int, schedule: ScheduleUpdate, db: Session = Depends(database.get_db)):
    db_schedule = db.query(models.Schedule).get(schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")
    db_schedule.title = schedule.title
    db_schedule.memo = schedule.memo
    db.commit()
    return {"message": "일정이 수정되었습니다."}

# 일정 삭제
@app.delete("/api/schedules/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(database.get_db)):
    schedule = db.query(models.Schedule).get(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")
    db.delete(schedule)
    db.commit()
    return {"message": "일정이 삭제되었습니다."}