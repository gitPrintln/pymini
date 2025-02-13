import pandas as pd

# 엑셀 파일 불러오기
file_path = "NutritionalManagement\\NMdata\\2020 한국인 영양소 섭취기준 요약표(kcal, 영양소별).csv"  # 엑셀 파일 경로
df = pd.read_csv(file_path, encoding="cp949", header=None)

# 1. 보건복지부, 2020 를 포함한 행 위로 4줄 불필요 -> 삭제
# 특정 단어 포함한 행 찾기
target_row = "보건복지부, 2020"

filtered_rows = df[df.apply(lambda row: row.astype(str).str.contains(target_row).any(), axis=1)]

# 특정 단어(보건복지부, 2020)가 포함된 행의 인덱스 찾기(제거해야할 행)
indices_to_remove = filtered_rows.index

# 위쪽 4개 행까지 포함하여 삭제할 인덱스 모두 찾기
indices_to_remove = set(indices_to_remove)  # 중복 방지
for idx in filtered_rows.index:
    for i in range(0, 4):  # 위쪽 4줄까지 포함
        if idx - i >= 0:  # 인덱스가 음수가 되지 않도록 체크
            indices_to_remove.add(idx - i)
            
print(indices_to_remove)  # 타겟이 포함된 행 출력

df = df.drop(indices_to_remove)

# 2. xi, xiv 등 x로 시작하는 모든 행 삭제
df = df[~df.apply(lambda row: row.astype(str).str.startswith('x').any(), axis=1)]

# 3. 빈 값이 있는 컬럼 삭제(평균 필요량 이후로 따라오는 셀 중에서 빈 값이 있는 부분은 그 아래 6개 셀 삭제)
target_cell = "평균\n필요량"

#filtered_cells = df[df.apply(lambda row: row.astype(str) == target_cell, axis=1)]

# target_cell과 정확히 일치하는 셀 찾기
matches = df.eq(target_cell)  # target_cell과 같은 셀이면 True, 아니면 False
matched_cells = df[matches]
print(matched_cells)

# print(filtered_cells)

# df = df.dropna(axis=1, how='all')
# df.to_csv('modified_file2.csv', index=False, encoding="utf-8-sig")