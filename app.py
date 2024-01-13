from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.secret_key = 'your-secret-key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')

    def __repr__(self):
        return '<User %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id

with app.app_context():
    db.create_all()

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(name=name, email=email, password=password)
        user.role = 'user'
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/create-admin')
def create_admin():
    user = User.query.filter_by(email='admin').first()
    if not user:
        user = User(name='Admin', email='admin', password='admin')
        user.role = 'admin'
        db.session.add(user)
        db.session.commit()
    return 'Admin user created'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            return redirect(url_for('index'))
        else:
            return 'Invalid email or password'
    return render_template('login.html')

@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        tasks = Task.query.filter_by(user_id=user_id).all()
        return render_template('index.html', user=user, tasks=tasks)
    return render_template('index.html', user=None, tasks=None)

@app.route('/iitm-courses', methods=['GET', 'POST'])
def iitm_courses():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('iitm-courses.html', user=user)
    return render_template('iitm-courses.html', user=None)

@app.route('/iitm-courses/diploma', methods=['GET', 'POST'])
def iitm_diploma():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('iitm-courses/diploma.html', user=user)
    return render_template('iitm-courses/diploma.html', user=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
 