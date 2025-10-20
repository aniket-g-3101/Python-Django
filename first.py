import mysql.connector as m
conn=m.connect(host="localhost",user="root",password="password",database="demo")
c1=conn.cursor()

q2="delete from emp where id=1"
c1.execute(q2)
q1="select * from emp "
c1.execute(q1)
for i in c1.fetchall():
    print(i[0] , " " ,i[1])
print("FILE IS EMPTY")
conn.close()
