import pandas as pd
import numpy as np
# 1. xlsx 파일 경로
file_path = 'NutritionalManagement\\NMdata\\2020 한국인 영양소 섭취 기준표.xlsx'

# 2. Excel 파일 읽기 (첫 번째 시트를 기본으로 읽음)
# openpyxl 라이브러리 사용
# header=[0,1] 옵션을 사용하면 계층적 컬럼 구조
# 여러 줄의 헤더를 가질 경우
# 각 컬럼이 (대분류, 소분류) 형태로 계층 구조를 가짐
df = pd.read_excel(file_path, header=[0, 1], engine='openpyxl')

# 두 줄의 헤더를 연결하여 한 줄의 헤더로 만들기
df.columns = ['_'.join(col).strip() for col in df.columns]

# 컬럼명 \n 제거
df.columns = df.columns.str.replace("\n", "")
# 컬럼명에서 .1, .2, .3 패턴이 있는 컬럼 찾기
#cols_to_remove = [col for col in df.columns if ".1" in col or ".2" in col or ".3" or ".4" in col]
# 해당 컬럼 제거
#df = df.drop(columns=cols_to_remove)

 # \n으로 나누어져 있는 열들을 개별 행으로 분리하는 함수
 # 한 행에 한 줄씩 들어가도록 뒤의 값들도 마찬가지로 해줌
 # 중간 중간에 성별, 연령, 지방,비타민 이런식으로 header부분이 들어가므로 이부분에서 잠깐
 # 끊었다가 다시 이어서 붙이려고 체크포인트 지점 만들어줌
check_point_idx = 0
def split_and_expand(df, check_point_idx):
    temp_expanded_df = pd.DataFrame()
    for idx, row in df.iloc[check_point_idx:].iterrows():
        # 각 행에 대해 '\n'으로 나누고 빈 셀은 제거
        expanded_rows = []
        for cell in row:
            if isinstance(cell, str) and '\n' in cell:
                expanded_rows.append(cell.split('\n'))
            else:
                expanded_rows.append([cell])
        # 최대 길이에 맞춰 열을 확장
        max_len = max(len(items) for items in expanded_rows)
        expanded_rows = [items + [np.nan] * (max_len - len(items)) for items in expanded_rows]
        # 새로운 DataFrame으로 변환
        temp_df = pd.DataFrame(expanded_rows).T
        temp_df.columns = df.columns
        temp_expanded_df = pd.concat([temp_expanded_df, temp_df], ignore_index=True)
        # 값이 성별인 경우 끊었다가 다시 해야함.
        if '성별' in row.values:
            check_point_idx = idx + 1 # 한 단계 성별 라인의 행은 건너서 넘어가고
            return check_point_idx, temp_expanded_df
    
    return check_point_idx, temp_expanded_df

expanded_df = pd.DataFrame()  # 임시 DataFrame 생성
for idx, row in df.iterrows(): # 0 ~ 끝 인덱스까지
    if idx == check_point_idx:
        # DataFrame 확장
        check_point_idx, piece_expanded_df = split_and_expand(df, check_point_idx)
        expanded_df = pd.concat([expanded_df, piece_expanded_df], ignore_index=True)  # expanded_df에 덧붙이기
    else: # 현재 for문에서도 인덱스를 맞춰줌. 체크포인트부터 다시 시작하기 위해서
        idx += 1

# 첫 성별 부분, 남자면 쭉 남자, 여자면 쭉 여자, 유아면 쭉 유아 빈부분 채워넣기
#for col in expanded_df.columns:
expanded_df["성별_Unnamed: 0_level_1"] = expanded_df["성별_Unnamed: 0_level_1"].fillna(method='ffill')

expanded_df.reset_index(drop=True, inplace=True)

# 수유부 아래에 3 행을 처리(성별, 연령, 셀레늄_평균필요량) 이런 식으로 처리
target_cell = "수유부"
# target_cell과 정확히 일치하는 셀 찾기
matches = expanded_df.eq(target_cell)  # target_cell과 같은 셀이면 True, 아니면 False
# 빠르게 위치만 찾기(수유부 값 아래 두 번째 행에 값이 있다면 작업해주기)
matched_cells = matches.stack().loc[lambda x: x].index.tolist()
target_idx = [index + 2 for index, label in matched_cells]
print(target_idx)
for idx in target_idx[2:-1]:
    for x, data in expanded_df.loc[idx].items():
        if data:
            # idx-1에 값 변경
            expanded_df.loc[idx-1, x] = expanded_df.loc[idx-1, x] + "_" + expanded_df.loc[idx, x] + expanded_df.loc[idx+1, x]
    # idx와 idx+1 삭제
    expanded_df.drop([idx, idx+1], inplace=True)

for idx in target_idx[2:-1]:            
    for data in expanded_df.loc[idx-1]:
        print(data)

# 최종 엑셀 쓰기
# expanded_df.to_excel('modified_file8.xlsx', index=False)