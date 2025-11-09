from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pickle, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ML model load
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create database if not exists
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if "user" in session:
        return render_template('index.html', username=session["user"])
    return render_template('index.html', username=None)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if User.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "Username already exists!"})
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "success", "message": "Signup successful!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session["user"] = username
        return jsonify({"status": "success", "message": "Login successful!"})
    return jsonify({"status": "error", "message": "Invalid credentials!"})

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('home'))

@app.route('/chat', methods=['POST'])
def chat():
    if "user" not in session:
        return jsonify({'reply': 'Please log in to use the chatbot.'})
    user_message = request.json['message']
    X = vectorizer.transform([user_message])
    reply = model.predict(X)[0]
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
