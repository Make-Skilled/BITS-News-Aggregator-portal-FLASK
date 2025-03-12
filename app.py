from flask import Flask, render_template, request, jsonify,session,redirect,url_for
from pymongo import MongoClient
import pyttsx3

app = Flask(__name__)
app.secret_key="NewsApp"

# MongoDB configuration
client = MongoClient('mongodb+srv://kr4785543:1234567890@cluster0.220yz.mongodb.net/')
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

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:  # Check if user is in session
        return redirect(url_for('login'))  # Redirect to login page
    return render_template('dashboard.html')

@app.route('/news')
def news():
    if 'user' not in session:  # Check if user is in session
        return redirect(url_for('login'))  # Redirect to login page
    return render_template('news.html')

@app.route("/content")
def content():
    return render_template('content.html')

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = users.find_one({"email": email, "password": password})
        
        if user:
            session['user'] = email  # Store user session
            return redirect(url_for('dashboard'))  # Redirect to a dashboard page
        else:
            return render_template('login.html', error="Invalid email or password!")
    
    return render_template('login.html', error=None)

@app.route("/article")
def article():
    return render_template("article.html")

@app.route("/all-news")
def all_news():
    return render_template('allNews.html')

@app.route('/read_summary', methods=['POST'])
def read_summary():
    data = request.json
    text = data.get("text", "")

    engine = pyttsx3.init()

    # Adjust voice settings
    voices = engine.getProperty('voices')  
    engine.setProperty('voice', voices[1].id)  # Change index (0 for male, 1 for female)
    engine.setProperty('rate', 150)  # Adjust speech speed (default is ~200)
    engine.setProperty('volume', 1.0)  # Set volume (0.0 to 1.0)

    engine.say(text)
    engine.runAndWait()

    return jsonify({"message": "Reading summary aloud!"})

@app.route('/details')
def details():
    return render_template('details.html')

if __name__ == '__main__':
    app.run(debug=True)
