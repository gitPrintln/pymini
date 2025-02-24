import psycopg2

# PostgreSQL 연결 정보
config = {
    'host': 'localhost',  # 호스트 주소 (예: 'localhost')
    'port': '5432',       # 기본 포트는 5432
    'database': 'postgres',  # 연결할 데이터베이스 이름
    'user': 'postgres',           # 사용자 이름
    'password': 'tiger'        # 비밀번호
}
cursor = None
conn = None

try:
    # 데이터베이스 연결
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    print("PostgreSQL 연결 성공")

    # 예제 쿼리 실행
    # cursor.execute("SELECT version();")
    # version = cursor.fetchone()
    # print("PostgreSQL 버전:", version)
    
    create_script = ''' CREATE TABLE IF NOT EXISTS test(
                            id          int PRIMARY KEY,
                            name        varchar(40) NOT NULL,
                            username    varchar(40) NOT NULL UNIQUE,
                            age         int)'''
    
    cursor.execute(create_script)
    
    conn.commit()
    
    

except Exception as e:
    print("오류: ", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()