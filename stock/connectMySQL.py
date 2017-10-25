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
db.close()