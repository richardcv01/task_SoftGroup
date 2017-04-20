import psycopg2

psw = 'user1'# Пароль до БД
connect = psycopg2.connect(user='postgres', host='localhost', password=psw)
cursor = connect.cursor()

def create_table():

    cursor.execute("CREATE TABLE IF NOT EXISTS tbl_data_get_html("
                   "id  serial PRIMARY KEY, "
                   "title varchar(500),"
                   "href VARCHAR (500),"
                   "author VARCHAR (20),"
                   "text TEXT DEFAULT NULL ,"
                    "price INT DEFAULT NULL ,"
                   "currency VARCHAR(10) DEFAULT NULL)"
                   )


def insertBD(title, href, author, text, price, currency):
    create_table()
    try:
        cursor.execute("INSERT INTO tbl_data_get_html (title, href, author, text, price, currency)"
                       "VALUES(%s, %s, %s, %s, %s, %s)", (title, href, author, text, price, currency))
        connect.commit()
    except psycopg2.Error as e:
        print(e)

def close():
    connect.close()



