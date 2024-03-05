"""
JSON socket agent
Agent receives json file.s and stores data to database server
Author: jan.novotny.cz@gmail.com
Dev. started: 2.3.2024
"""


from classOdbc import DBOdbc
from classSocket import Socket

def main():
    ipAddress = "127.0.0.1"
    db = DBOdbc()
    sock = Socket(ipAddress)

    # DB connection parameters
    dsn = "MariaDB"
    server = "192.168.240.50"
    database = "asterisk"
    username = "lelek"
    password = "Dbuser*9999"
    connectionString = f"DSN={dsn};SERVER={server};DATABASE={database};UID={username};PWD={password}"

    try:
        db.connect(connectionString)
        queryString = "select exten, context from asterisk.extensions order by exten, priority;"
        print(db.query(queryString))
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()
