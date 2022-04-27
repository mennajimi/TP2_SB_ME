import sqlite3

def init_db():
    conn = sqlite3.connect('params.db')
    query = ''' CREATE TABLE IF NOT EXISTS params (requestID INTEGER NOT NULL,
                    params   TEXT NOT NULL,
		            PRIMARY KEY (requestID)) '''
    conn.cursor().execute(query)

def clean():
    try:
        conn = sqlite3.connect('params.db')
        conn.cursor().execute("DELETE FROM params")
        conn.commit()
    except sqlite3.Error as error:
        print (error)

def add(params):
    try:
        conn = sqlite3.connect('params.db')
        conn.cursor().execute("INSERT INTO params (params) VALUES (?)", (params,))
        conn.commit()
    except sqlite3.Error as e:
        print (e)

def save(params):
    try:
        conn = sqlite3.connect('params.db')
        conn.cursor().execute("UPDATE params SET montant=? WHERE code=?", params)
        conn.commit()
    except sqlite3.Error as e:
        print (e)

def getParamsList():
    try:
        con = sqlite3.connect('params.db')
        cur = con.cursor()
        cur.execute("SELECT params FROM params")
        items = cur.fetchall()[0]
        con.close()
    except sqlite3.Error as e:
        print (e)
    return items

def getParams():
    params_list = []
    try:
        con = sqlite3.connect('params.db')
        cur = con.cursor()
        cur.execute("SELECT params FROM params")
        items = cur.fetchall()
        for par in items:
            par = str(par)
            par = par.replace("('", "")
            par = par.replace("',)", "")
            params_list.append(par)
        con.close()
    except sqlite3.Error as e:
        print(e)
    return params_list