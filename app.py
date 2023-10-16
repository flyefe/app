from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask (__name__)
app.secret_key = '1234'


#MYSQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'maestro'
app.config['MYSQL_DB'] = 'user_sys'

mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)


@app.route('/check')
def check_db():
    if mysql is not None:
        return "Database is connected!"
    else:
        return "Database connection failed."

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('home.html')
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.cursor()
        cur.execute("SELECT username, password FROM user WHERE username = %s",(username,))
        user = cur.fetchone()
        cur.close()

        if user and password == user[1]:
            session['username'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error= 'invalid username or password')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        
        cursor = mysql.cursor()
        cursor.execute("INSERT INTO user (username, email, password, name) VALUES (%s, %s, %s, %s)", (username, email, password, name))
        mysql.commit()
        cursor.close()

        # flash('Account created successfully', 'success')
        return redirect(url_for('login'))  # You can redirect to your login page after successful signup

    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True, port=5050)
