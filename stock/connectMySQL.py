import pymysql
db = pymysql.connect("localhost","root","112233","forq" )# Open database connection
cursor = db.cursor()  # prepare a cursor object using cursor() method
cursor.execute("DROP TABLE IF EXISTS employee ")
# Create table as per requirement
sql = """CREATE TABLE `employee` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `first_name` char(20) NOT NULL,
  `last_name` char(20) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `sex` char(1) DEFAULT NULL,
  `income` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

cursor.execute(sql)
print("Created table Successfull.")
# disconnect from server


# Prepare SQL query to INSERT a record into the database.
sql2 = """INSERT INTO EMPLOYEE(FIRST_NAME,
   LAST_NAME, AGE, SEX, INCOME)
   VALUES ('Mac', 'Su', 20, 'M', 5000)"""
try:
   # Execute the SQL command
   cursor.execute(sql2)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

## 再次插入一条记录
# Prepare SQL query to INSERT a record into the database.
sql3 = """INSERT INTO EMPLOYEE(FIRST_NAME,
   LAST_NAME, AGE, SEX, INCOME)
   VALUES ('Kobe', 'Bryant', 40, 'M', 8000)"""
try:
   # Execute the SQL command
   cursor.execute(sql3)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
print (sql)
print('Yes, Insert Successfull.')
# disconnect from server
db.close()

