from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['news_db']  
users = db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('index.html', _anchor='about')

@app.route('/reviews')
def reviews():
    return render_template('index.html', _anchor='reviews')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match!")
        
        # Check if email or mobile already exists
        if users.find_one({"email": email}):
            return render_template('register.html', error="Email already exists!")
        
        if users.find_one({"mobile": mobile}):
            return render_template('register.html', error="Mobile number already exists!")
        
        # Insert user data into MongoDB
        users.insert_one({
            "name": name,
            "email": email,
            "mobile": mobile,
            "password": password  # In a real app, hash the password before storing
        })
        
        return redirect(url_for('login'))  # Redirect to login page
    
    return render_template('register.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)
