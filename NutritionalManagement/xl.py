import pandas as pd

# 1. xlsx 파일 경로
file_path = 'NutritionalManagement\\NMdata\\2020 한국인 영양소 섭취 기준표.xlsx'

# 2. Excel 파일 읽기 (첫 번째 시트를 기본으로 읽음)
# openpyxl 라이브러리 사용
# header=[0,1] 옵션을 사용하면 계층적 컬럼 구조
# 여러 줄의 헤더를 가질 경우
# 각 컬럼이 (대분류, 소분류) 형태로 계층 구조를 가짐
df = pd.read_excel(file_path, engine='openpyxl', header=[0, 1])

# '\n' 기준으로 문자열을 리스트로 변환
# 모든 컬럼을 '\n' 기준으로 리스트로 변환 
# for col in ['연령', '평균\n필요량', '권장\n섭취량', '충분\n섭취량', '상한\n섭취량']:
# for col in ['연령', '에너지(kcal/일)', '탄수화물(g/일)', '식이섬유(g/일)']:
#    df[col] = df[col].str.split('\n')

# 데이터를 세분화하려면 pd.DataFrame.explode()를 활용해서 행을 펼침
# 리스트를 개별 행으로 변환 (explode 적용)
# reset_index(drop=True)로 인덱스 정리.
# df = df.explode(['연령', '에너지(kcal/일)', '탄수화물(g/일)', '식이섬유(g/일)']).reset_index(drop=True)

# 3. 병합된 셀 처리 (앞쪽 데이터 채우기)
# 병합된 셀 때문에 일부 값이 NaN으로 표시되는 것을 해결
# fillna로 위쪽의 값을 아래로 채움
#df.iloc[:, 0] = df.iloc[:, 0].fillna(method='ffill')  # 성별
#df.iloc[:, 1] = df.iloc[:, 1].fillna(method='ffill')  # 연령



# 4. 컬럼명 정리 (멀티 인덱스를 단일 컬럼으로 변환)
# '_'를 사용하여 두 개의 헤더를 하나의 컬럼명으로 합침. strip() : 공백 제거
# 리스트 컴프리헨션(List Comprehension)
# isinstance(col, tuple) 의 의미 : col이 튜플(tuple)인지 아닌지 체크하는 조건
# True이면 튜플을 _로 연결하여 문자열로 변환
# False이면 변환하지 않고 그대로 유지
# 단일 컬럼 > 다중 인덱스가 아니라 _로 연결된 단일 컬럼 형태로 변경
# 예를 들면 에너지_필요량	에너지_권장섭취량 형식으로
#df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

#print(df.head(15))

# 5. 데이터 변환 (melt 적용)
# melt() 를 사용하면 데이터를 긴 형태 (long format)로 변환
# df_melted = df.melt(id_vars=['성별', '연령'], var_name='영양소', value_name='섭취량')

# print(df_melted.head(20))

# 최종 엑셀 쓰기
# df.to_excel('modified_file2.xlsx', index=False)