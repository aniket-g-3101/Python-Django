import mysql.connector as m

conn=m.connect(host="localhost",user="root",password="password",database="demo")
c1=conn.cursor()
n=int(input(" How Many Records to Insert : "))
data=[]
for i in range (n):
    srno=int(input("Enter Value for Id : "))
    name=input("Enter Value for Name :")
    print("Record Inserted..")
    data.append((srno,name))
    
q1 = "INSERT INTO emp(id, name) VALUES (%s, %s)"
c1.executemany(q1, data)

conn.commit()
print("Records Inserted Successfully")

    
