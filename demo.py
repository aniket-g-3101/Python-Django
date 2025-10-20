import mysql.connector as m
conn=m.connect(host="localhost",user="root",password="password",database="demo")
c1=conn.cursor()
q="create table emp(id int,name char(10))"
c1.execute(q)
print(successfull)
