from sqlite3 import connect

class Database:
    db=None
    @staticmethod
    def connectDatabase():
        Database.db=connect("number.db")
        cursor=Database.db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, email text NOT NULL, password text NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS fact_table(id integer PRIMARY KEY, email text NOT NULL, fact_text text NOT NULL)")
        Database.db.commit()
        print("Connected")
        
    @staticmethod
    def insertdata(email,password):
        sql="INSERT INTO users (email,password) VALUES(?,?)"
        val=(f"{email}",f"{password}")
        cursor=Database.db.cursor()
        cursor.execute(sql,val)
        Database.db.commit()
        
    @staticmethod
    def isValid(email):
        sql=f"SELECT * FROM users WHERE email='{email}'"
        cursor=Database.db.cursor()
        cursor.execute(sql)
        has=cursor.fetchall()
        if(has):
            return False
        else:
            return True
        
    @staticmethod
    def isExist(email,password):
        sql=f"SELECT * FROM users WHERE email='{email}' and password='{password}'"
        cursor=Database.db.cursor()
        cursor.execute(sql)
        has=cursor.fetchall()
        if(has):
            return True
        else:
            return False
