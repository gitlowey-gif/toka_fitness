import sqlite3

class database:

    def __init__(self):
        #define our database "toka_fitness.db"
        self.DBname = "toka_fitness.db"

        #create our database connection
    def connect (self):
        conn = None
        try:
            conn = sqlite3.connect(self.DBname)
        except Exception as e:
            print(e)
        return conn
    
    #execute a select query 
    def queryDB(self, command, params=[]):
        conn = self.connect()
        conn.row_factory = sqlite3.Row  # Add this line
        cur = conn.cursor()
        cur.execute(command, params)
        result = cur.fetchall()
        self.disconnect(conn)
        return result

    #updating database - commit to our database
    def updateDB(self, command, params=[]):  # Fixed typo: parmas -> params
        conn = self.connect()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(command, params)  # Fixed typo: parmas -> params
        conn.commit()
        self.disconnect(conn)  # Remove the result fetching and disconnect immediately
        return None  # Return None since we're not fetching results
    
    def disconnect(self,conn):
        conn.close()
        
