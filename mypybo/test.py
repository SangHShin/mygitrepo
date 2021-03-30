import cx_Oracle
# import os
# 테스트 코드
# Connect as user "hr" with password "oracle4U" to the "orcl" instanceName#service running on this computer.
connection = cx_Oracle.connect("hr", "oracle4U", "localhost/orcl")

cursor = connection.cursor()
cursor.execute("""
        SELECT first_name, last_name
        FROM hr.employees
        WHERE department_id = :did AND employee_id > :eid""",
        did = 50,
        eid = 190)
for fname, lname in cursor:
    print("Values:", fname, lname)



# # 한글지원방법
# os.putenv('NLS_LANG', '.UTF8')
#
#
#
#
# # 함수 정의
# def connect():
#     # 라이브러리 연결
#     cx_Oracle.init_oracle_client(lib_dir=r"C:\myPyDev\instantclient_19_10")
#
#     db_ip = 'localhost:1526/testdb'
#     con_id = 'user'
#     con_pw = 'password'
#
#     # 연결에 필요한 기본 정보(유저, 비밀번호, 데이터베이스 서버 주소)
#     connection = cx_Oracle.connect(con_id, con_pw, con_ip)
#     cursor = connection.cursor()
#     cursor.execute("""
#         select *
#         from member
#         where name='홍길동'
#         """)
#
#     for list in cursor:
#         print(list)
#
#     cursor.close()
#     connection.close()
#
#
# # 함수 실행
# connect()