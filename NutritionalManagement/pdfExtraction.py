import pandas as pd
import numpy as np

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
            
# print(indices_to_remove)  # 타겟이 포함된 행 출력

df = df.drop(indices_to_remove)

# 2. xi, xiv 등 x로 시작하는 모든 행 삭제
df = df[~df.apply(lambda row: row.astype(str).str.startswith('x').any(), axis=1)]

# 3. columns에서 모두 NaN, 빈 값인 부분 없애고 앞으로 당기기(1)
df = df.dropna(axis=1, how='all')

# 4-0. 인덱스 재설정(기존 인덱스 필요 없음) 행, 열 차례대로
df = df.reset_index(drop=True)
df.columns = range(df.shape[1])

# 4. 빈 값이 있는 컬럼 삭제(2)
# 평균 필요량 이후로 따라오는 셀 중에서 빈 값이 있는 부분은 그 아래 6개 셀 삭제
# 빈 값이 아닌 셀이 나오면 중지
target_cell = "평균\n필요량"

# target_cell과 정확히 일치하는 셀 찾기
matches = df.eq(target_cell)  # target_cell과 같은 셀이면 True, 아니면 False

# matches는 원래 2차원 데이터프레임이었지만, .stack()을 사용하면 이를 1차원 Series 형태로 변환
# .index.tolist() 리스트 형식으로 변환
# df.where(matches).stack().index.tolist() : 컬럼명이 포함된 (행, 열) 튜플 리스트 반환(df자체를 재활용>컬럼명 유지)
# matches.stack().loc[lambda x: x].index.tolist() : 빠르게 위치만 찾으려면 이게 나음
matched_cells = matches.stack().loc[lambda x: x].index.tolist()
print(matched_cells)

# test. matched_cells 에 해당하는 값 실제로 불러와보기
# values = [df.at[row, col] for row, col in matched_cells]
# next_col_values = [df.iat[row, col + 1] if col + 1 < df.shape[1] else None for row, col in matched_cells]

# print(next_col_values)

# 타겟 셀 다음 열이 비어있는지 확인 후 비어 있으면 좌측으로 이동시킴, 그게 아니라면 break
# 타겟 셀을 기준으로 이동
for row, col in matched_cells:
    next_cell = col + 1  # 타겟 셀 다음 열 (b)
    
    # 반복 작업 : 값이 있는열을 만날때까지 계속 한칸씩 당겨줘야함
    max_col = df.shape[1]  # 데이터프레임의 열 수
    while next_cell < max_col: # 다음 열이 존재하면 진행
        # 다음 열(b)의 값이 NaN인지 확인
        # Pandas의 .iat[] 속성을 사용해서 특정 행(row)과 열(next_col)의 값을 가져오는 역할
        if pd.isna(df.iat[row, next_cell]):
            # b가 속한 행과 아래 7개의 행에 대해 열을 좌측으로 이동
            for r in range(row, min(row + 7, df.shape[0])):  # 범위를 벗어나지 않도록 조정/공백이 있는 셀 포함해서 아래행으로 7개까지
                                                            #  만약 남은 행 개수가 7개 미만이라면, 가능한 범위까지만 반복
                # 좌측으로 이동
                # df.iloc[r, next_cell:-1] 이동 대상 구역
                # df.iloc[r, next_cell+1:] 옮길 대상 구역
                # r-1까지 해줘서 header도 함께 이동 TODO: 나중에 중간 중간 header도 지울 거면 r-1 > r로 수정
                df.iloc[r-1, next_cell:-1] = df.iloc[r-1, next_cell+1:].values
        else:
            break
        
    
# 타겟의 한 칸 뒤 열 찾기
# next_cell = df.shift(-1, axis=1)  # 한 칸 뒤 열로 이동
# empty_next = next_cell.isna()  # 빈 셀인지 확인




# df.to_csv('modified_file2.csv', index=False, encoding="utf-8-sig")