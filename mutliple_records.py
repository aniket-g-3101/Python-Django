import mysql.connector as m

conn=m.connect(host="localhost",user="root",password="password",database="demo")
c1=conn.cursor()
data=[(1,'Aniket'),(2,'Sanjay'),(3,'Gavali')]
q1=f"insert into emp(id,name) values(%s,%s)"
c1.executemany(f"insert into emp(id,name) values(%s,%s)",data)
conn.commit()   
print("Successfull")
                
