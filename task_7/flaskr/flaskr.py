from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2
app = Flask(__name__)
app.config.from_object(__name__)

# Загружаем конфиг по умолчанию и переопределяем в конфигурации часть
# значений через переменную окружения
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
psw = 'user1'  # Пароль до БД
connect = psycopg2.connect(user='postgres', host='localhost', password=psw)
cursor = connect.cursor()


@app.route('/', methods=['GET', 'POST'])
def show_entries():
    sql = 'select author, title, price, currency, id from tbl_data_get_html'
    if request.method == 'POST':
        text = request.form['text']
        if text != '':
            sql = "SELECT author, title, price, currency, id FROM tbl_data_get_html WHERE title like '%"+text+"%' or text like '%"+text+"%'"
    cursor.execute(sql)
    connect.commit()
    table_res = cursor.fetchall()
    return render_template('show_entries.html', entries=table_res)

@app.route('/detail/<id>')
def detail(id):
    cursor.execute('select * from tbl_data_get_html WHERE id='+id)
    connect.commit()
    table_res = cursor.fetchall()
    return render_template('detail.html', entries=table_res[0])


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form['username']
        pasword = request.form['password']
        if  not user_exist(user_name) :
            error = 'Invalid username'
        elif pasword != select_psw(user_name):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user_name = request.form['username']
        pasword = request.form['password']
        paswordr = request.form['passwordr']
        email = request.form['email']
        if user_exist(user_name) or user_name == '':
            error = 'Such user already exists'
        elif email_exist(email) or email == '':
            error = 'Such email already exists'
        elif pasword != paswordr or pasword == '':
            error = 'Passwords do not match'
        else:
            add_user(user_name, pasword, email)
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

def user_exist(user_name):
    cursor.execute("select user_name from table_user WHERE user_name="+"'"+user_name+"'")
    connect.commit()
    sel = list(cursor)
    if sel == []:
        return False
    else:
        return True

def email_exist(email):
    cursor.execute("select email from table_user WHERE email="+"'"+email+"'")
    connect.commit()
    sel = list(cursor)
    if sel == []:
        return False
    else:
        return True

def add_user(user_name, password, email):
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS table_user("
                       "id  SERIAL PRIMARY KEY, "
                       "user_name varchar(50) UNIQUE,"
                       "pasword VARCHAR (50),"
                       "email VARCHAR (30) UNIQUE)"
                       )
        connect.commit()
        cursor.execute("INSERT INTO table_user (user_name, pasword, email)"
                       "VALUES(%s, %s, %s)"
                       "ON CONFLICT (user_name) DO NOTHING;", (user_name, password, email))
        connect.commit()
    except psycopg2.Error as e:
        print(e)

def select_psw(user_name):
    cursor.execute("select pasword from table_user WHERE user_name=" + "'" + user_name + "'")
    connect.commit()
    sel = list(cursor)
    if sel != []:
        return sel[0][0]

if __name__ == '__main__':
    app.run()