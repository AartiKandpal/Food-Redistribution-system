import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'food-rescue-super-secret'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(id=user['id'], username=user['username'], email=user['email'])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                         (username, email, hashed_pw))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Email already registered!"
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        user_db = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user_db and check_password_hash(user_db['password'], password):
            user_obj = User(id=user_db['id'], username=user_db['username'], email=user_db['email'])
            login_user(user_obj)
            return redirect(url_for('index'))
        return "Login Error: Check your details."
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/donor')
@login_required
def donor():
    return render_template('donor.html')

@app.route('/add_food', methods=['POST'])
@login_required
def add_food():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    address = request.form.get('address')
    cooked_time = request.form.get('cooked_time')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO food (name, quantity, address, cooked_time, donor_id) VALUES (?, ?, ?, ?, ?)',
                 (name, quantity, address, cooked_time, current_user.id))
    conn.commit()
    conn.close()
    return redirect(url_for('recipient'))

@app.route('/recipient')
def recipient():
    conn = get_db_connection()
    # Sirf Available food dikhayenge
    food_items = conn.execute('SELECT * FROM food WHERE status = "Available"').fetchall()
    conn.close()
    return render_template('recipient.html', food_list=food_items)

@app.route('/claim_food/<int:food_id>')
@login_required
def claim_food(food_id):
    conn = get_db_connection()
    conn.execute('UPDATE food SET status = "Claimed" WHERE id = ?', (food_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('recipient'))

@app.route('/map')
def view_map():
    conn = get_db_connection()
    # Sirf wahi khana dikhao jo claim nahi hua hai
    food_items = conn.execute('SELECT * FROM food WHERE status = "Available"').fetchall()
    conn.close()
    return render_template('map.html', food_list=food_items)

if __name__ == '__main__':
    app.run(debug=True)