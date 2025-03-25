import sqlite3
import pandas as pd
import os

class PanDb:

    path = None

    def __init__(self, path=None):
        if path is None:
            self.path = ":memory:"
        else:
            self.path = path
        print(self.path)

    def createTable(self, table, /, **args):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        body = ", ".join([f"{col} {dtype}" for col, dtype in args.items()])
        sqlstr = f"CREATE TABLE IF NOT EXISTS {table} ( id INTEGER PRIMARY KEY AUTOINCREMENT, {body})"
        cursor.execute(sqlstr)
        conn.commit()
        cursor.close()
        conn.close()

    def getData(self, table):
        with sqlite3.connect(self.path) as conn:
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        return df

    def appendData(self, table, data):
        with sqlite3.connect(self.path) as conn:
            data.to_sql(f"{table}", conn, if_exists="append", index=False)

    def updateData(self):
        pass

class bookfs:

    def __init__(self, path):
        self.path = path
    
    def getFiles(self):
        file_files = []
        file_paths = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_files.append(file)
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
        for file, path in zip(file_files, file_paths):
            print(file, path)

if __name__ == "__main__":

    data = {
        "bookname" : ["test", ],
        "bookpath" : ["test", ]       
    }

    fs = bookfs("/studio/project/mochen/source/_posts/")
    fs.getFiles()

    df = pd.DataFrame(data)
    print(df)
    # db = PanDb("./book.db")
    # db.createTable("Books", bookname="string", bookpath="string")
