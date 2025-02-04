import pandas as pd
print(pd.__version__)

# 데이터 생성
data = {
    '이름': ['철수', '영희', '민수', '지은'],
    '나이': [25, 30, 28, 22],
    '도시': ['서울', '부산', '대구', '인천']
}

# DataFrame 생성
df = pd.DataFrame(data)

# 출력
print(df)