import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Sex, Age, Nutrient, NutrientRef  # 정의된 ORM 클래스

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

# 1: 성별 미리 등록 (남자, 여자, 영아, 유아 등)
sex_list = ['남자', '여자', '영아', '유아']
for code in sex_list:
    if not session.query(Sex).filter_by(sex_code=code).first():
        session.add(Sex(sex_code=code))
session.commit()
sex_map = {s.sex_code: s.sex_id for s in session.query(Sex).all()}

# 2: 기준 매핑 초기화
criteria_map = {
    '권장섭취량': 'rda_amount',
    '평균필요량': 'ai_amount',
    '상한섭취량': 'ul_amount'
}
age_map = {}
nutrient_map = {}

# 3: 엑셀 파싱
excel_file = pd.ExcelFile('final.xlsx', engine='openpyxl')

for sheet_name in excel_file.sheet_names:
    df = excel_file.parse(sheet_name, header=0)

    df_melt = df.melt(id_vars=['성별', '연령'],
                      var_name='영양소_기준명', value_name='값') # 정규화
    df_melt = df_melt.dropna(subset=['값']) # 빈 셀  제거

    def parse_column(col):
        return col.rsplit('_', 1) if '_' in col else (col, None)

    for _, row in df_melt.iterrows():
        sex, age, nutrient_col, value = row['성별'], row['연령'], row['영양소_기준명'], row['값']
        nutrient_full, criteria_name = parse_column(nutrient_col)
        if criteria_name not in criteria_map:
            continue

        # 단위 처리
        if '(' in nutrient_full:
            name, unit = nutrient_full.split('(', 1)
            unit = unit.replace(')', '')
        else:
            name, unit = nutrient_full.strip(), ''

        name = name.strip()

        # 성별 ID
        sex_id = sex_map.get(sex)
        if sex_id is None:
            print(f"[경고] SEX 테이블에서 '{sex}' 찾을 수 없음")
            continue

        # 연령 ID
        if age not in age_map:
            age_obj = session.query(Age).filter_by(label=age).first()
            if not age_obj and '-' in age:
                try:
                    parts = age.replace('개월', '').replace('세', '').split('-')
                    age_obj = session.query(Age).filter_by(
                        age_min=int(parts[0]), age_max=int(parts[1])
                    ).first()
                except:
                    pass
            if not age_obj:
                print(f"[경고] AGE 테이블에서 '{age}' 찾을 수 없음")
                continue
            age_map[age] = age_obj.age_id
        age_id = age_map[age]

        # 영양소 ID
        nutrient_key = (name, unit)
        if nutrient_key not in nutrient_map:
            nutrient_obj = session.query(Nutrient).filter_by(name=name, unit=unit).first()
            if not nutrient_obj:
                nutrient_obj = Nutrient(name=name, unit=unit)
                session.add(nutrient_obj)
                session.commit()
            nutrient_map[nutrient_key] = nutrient_obj.nutrient_id
        nutrient_id = nutrient_map[nutrient_key]

        # 기준값 반영
        field_name = criteria_map[criteria_name]
        nutrient_ref = session.query(NutrientRef).filter_by(
            nutrient_id=nutrient_id, age_id=age_id, sex_id=sex_id
        ).first()

        if nutrient_ref is None:
            nutrient_ref = NutrientRef(nutrient_id=nutrient_id, age_id=age_id, sex_id=sex_id)

        setattr(nutrient_ref, field_name, value)
        session.merge(nutrient_ref)

    session.commit()

print("모든 시트 처리 완료.")