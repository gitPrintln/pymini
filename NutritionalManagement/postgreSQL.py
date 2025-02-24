import psycopg2
import psycopg2.extras # 딕셔너리 형태로 결과 반환하기위함

# PostgreSQL 연결 정보
config = {
    'host': 'localhost',        # 호스트 주소 (예: 'localhost')
    'port': '5432',             # 기본 포트는 5432
    'database': 'postgres',     # 연결할 데이터베이스 이름
    'user': 'postgres',         # 사용자 이름
    'password': 'tiger'         # 비밀번호
}
conn = None

try:
    # 데이터베이스 연결
    # with 절 : 자원 관리와 코드의 간결성, 가독성, 재사용성, 성능, 복잡한 쿼리 분할 용도
    # 자원 누수를 방지, 예외 처리 시에도 자원이 안전하게 해제
    with psycopg2.connect(**config) as conn:
        
        # conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # SQL 쿼리 결과를 튜플이 아니라, 필드명이 키로, 각 행의 데이터가 값으로 담긴 딕셔너리로 받을 수 있음
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor: 
            print("PostgreSQL 연결 성공")

            # 예제 쿼리 실행
            # cursor.execute("SELECT version();")
            # version = cursor.fetchone()
            # print("PostgreSQL 버전:", version)
            
            # 시작 전에 table 초기화
            cursor.execute('drop table if exists test')
            
            create_script = ''' CREATE TABLE IF NOT EXISTS test(
                                    id          int PRIMARY KEY,
                                    name        varchar(40) NOT NULL,
                                    username    varchar(40) NOT NULL UNIQUE,
                                    age         int)'''
            
            cursor.execute(create_script)
            
            insert_script = 'INSERT INTO test (id, name, username, age) VALUES (%s, %s, %s, %s)'
            insert_value = [(1, '홍길동', 'mann', 25), (2, '이순신', 'lee', 26), (3, '신립', 'sin', 33)]
            
            for data in insert_value:
                cursor.execute(insert_script, data)
            
            # cursor.execute('SELECT * FROM test')
            # for data in cursor.fetchall():
            #     print(data)
                
            update_script = "UPDATE test SET age = 29 where name = '이순신'"
            cursor.execute(update_script)
            
            cursor.execute('SELECT * FROM test')
            for data in cursor.fetchall():
                print(data['name'], data['username'], data['age'])
            
            # 값을 쿼리와 분리함으로써 SQL 인젝션 공격을 예방
            # 쿼리에서 name 값 '홍길동'을 플레이스홀더(%s)로 바인딩하려면 튜플 형태로 전달
            # 괄호 ()로 값을 묶으면 튜플로 간주. 
            # 그러나 단 하나의 값을 괄호로 묶을 경우, 그것이 튜플로 인식되기 위해서는 쉼표가 필요
            delete_script = 'DELETE FROM test WHERE name = %s'
            delete_value = ('홍길동',) 
            cursor.execute(delete_script, delete_value)
            
            cursor.execute('SELECT * FROM test')
            for data in cursor.fetchall():
                print(data['name'], data['username'], data['age'])
            
            conn.commit()
            # cursor.execute('drop table if exists test')
            
except Exception as e:
    print("오류: ", e)
finally:
    if conn:
        conn.close()