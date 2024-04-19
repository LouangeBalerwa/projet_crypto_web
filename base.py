import mysql.connector

def connecter():

    db = mysql.connector.connect(
        host ='localhost',
        user = 'root',
        password='',
        database = 'transfert_agent',
    )
    
    return db
