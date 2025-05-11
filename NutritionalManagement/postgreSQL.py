import psycopg2
import psycopg2.extras # 딕셔너리 형태로 결과 반환하기위함

# PostgreSQL 연결 정보
config = {
    'host': 'localhost',        # 호스트 주소 (예: 'localhost')
    'port': '5432',             # 기본 포트는 5432
    'database': 'postgres',     # 연결할 데이터베이스 이름
    'user': 'postgres',         # 사용자 이름
    'password': '1234'         # 비밀번호
}
conn = None

try:
    # 데이터베이스 연결
    # with 절 : 자원 관리와 코드의 간결성, 가독성, 재사용성, 성능, 복잡한 쿼리 분할 용도
    # 자원 누수를 방지, 예외 처리 시에도 자원이 안전하게 해제
    with psycopg2.connect(**config) as conn:

        # conn.set_client_encoding('UTF8')
        # conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # SQL 쿼리 결과를 튜플이 아니라, 필드명이 키로, 각 행의 데이터가 값으로 담긴 딕셔너리로 받을 수 있음
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor: 
            print("PostgreSQL 연결 성공")

            cursor.executemany("""
                INSERT INTO "SEX" (sex_id, sex_code) VALUES (%s, %s)
            """, [
                (1, '남성'),
                (2, '여성')
            ])

            # 연령대 데이터 삽입
            cursor.executemany("""
                INSERT INTO "AGE" (age_id, age_min, age_max, label) VALUES (%s, %s, %s, %s)
            """, [
                (1, 0, 0, '0-5개월'),
                (2, 0, 0, '6-11개월'),
                (3, 1, 2, '1-2세'),
                (4, 3, 5, '3-5세'),
                (5, 6, 8, '6-8세'),
                (6, 9, 11, '9-11세'),
                (7, 12, 14, '12-14세'),
                (8, 15, 18, '15-18세'),
                (9, 19, 29, '19-29세'),
                (10, 30, 49, '30-49세'),
                (11, 50, 64, '50-64세'),
                (12, 65, 74, '65-74세'),
                (13, 75, None, '75세 이상'),
            ])
            conn.commit()
            # cursor.execute('drop table if exists test')
            cursor.close()
except Exception as e:
    print("오류: ", e)
finally:
    if conn:
        conn.close()