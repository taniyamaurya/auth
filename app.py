from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import bcrypt

app = Flask(__name__)
app.secret_key='super secret key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Taniya@123'
app.config['MYSQL_DB'] = 'user_db'

# Your registration and login routes will go here

@app.route('/home')
def home():
    # Your home page code goes here
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']

        # Connect to MySQL using pymysql
        conn = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = conn.cursor()

        # Check if the username already exists in the database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            flash('Username already exists. Please log in.', 'info')
            return redirect(url_for('register'))
        else:
            # User doesn't exist, so proceed with registration
            cursor.execute("INSERT INTO users (username, password, name) VALUES (%s, %s, %s)", (username, password, name))
            conn.commit()
            conn.close()

            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to MySQL using pymysql
        conn = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user['password'] == password:  # Check if the provided password matches the stored password
            session['loggedin'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the user's session to log them out
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Additional routes for your application

if __name__ == '__main__':
    app.run(debug=True)
