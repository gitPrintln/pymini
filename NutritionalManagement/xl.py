import pandas as pd

# xlsx 파일 경로
file_path = 'NutritionalManagement\\NMdata\\2020 한국인 영양소 섭취 기준표.xlsx'

# Excel 파일 읽기 (첫 번째 시트를 기본으로 읽음)
df = pd.read_excel(file_path, engine='openpyxl')

# 데이터 확인
print(df.head())  # 첫 5행 출력