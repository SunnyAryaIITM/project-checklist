from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Course %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.level
        }

    def __init__(self, name, level, type):
        self.name = name
        self.level = level
        self.type = type

class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Checklist %r>' % self.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_completed': self.is_completed
        }
    
    def __init__(self, name, course_id, user_id):
        self.name = name
        self.course_id = course_id
        self.user_id = user_id

with app.app_context():
    db.create_all()

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)
    session.pop('user_role', None)
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
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html')

@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    print("Hii")
    if request.method == 'POST':
        print("Hi")
        name = request.form['name']
        level = request.form['level']
        type = request.form['type']
        course = Course(name=name, level=level, type=type)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('add-course.html')

@app.route('/create-admin')
def create_admin():
    user = User.query.filter_by(email='admin@bytebuddy.com').first()
    if not user:
        user = User(name='Admin', email='admin@bytebuddy.com', password='admin')
        user.role = 'admin'
        db.session.add(user)
        db.session.commit()
        return 'Admin user created'
    return 'Admin user already exists'

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('login')
    if request.method == 'POST':
        print(request.form)
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        print(user)
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_role'] = user.role
            if user.role == 'admin':
                print('you are admin')
                return redirect('/admin')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
            render_template('auth/login.html')
    return render_template('auth/login.html')

@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        tasks = Task.query.filter_by(user_id=user_id).all()
        flash('Welcome, {}!'.format(user.name), 'success')
        return render_template('index.html', user=user, tasks=tasks)
    return render_template('index.html', user=None, tasks=None)

@app.route('/admin')
def admin():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('admin/dashboard.html', user=user)
    flash('Login required', 'error')
    return redirect(url_for('login'))

@app.route('/iitm-courses', methods=['GET', 'POST'])
def iitm_courses():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('iitm-courses.html', user=user)
    return render_template('iitm-courses.html', user=None)

@app.route('/iitm-courses/foundation', methods=['GET', 'POST'])
def iitm_foundation():
    flash('We are under development. Please try to open Diploma Courses for now.', 'warning')
    return redirect(url_for('iitm_courses'))

@app.route('/iitm-courses/diploma', methods=['GET', 'POST'])
def iitm_diploma():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('iitm-courses/diploma.html', user=user, courses=Course.query.all())
    return render_template('iitm-courses/diploma.html', user=None, courses=Course.query.all())

@app.route('/iitm-courses/bsc', methods=['GET', 'POST'])
def iitm_bsc():
    flash('We are under development. Please try to open Diploma Courses for now.', 'warning')
    return redirect(url_for('iitm_courses'))

@app.route('/iitm-courses/bs', methods=['GET', 'POST'])
def iitm_bs():
    flash('We are under development. Please try to open Diploma Courses for now.', 'warning')
    return redirect(url_for('iitm_courses'))

@app.route('/iitm-courses/diploma/<int:course_id>', methods=['GET', 'POST'])
def iitm_diploma_detail(course_id, checklists=None):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        checklists = Checklist.query.filter_by(user_id=user_id, course_id=course_id).all()
        return render_template('iitm-courses/diploma-course.html', user=user, course=Course.query.get(course_id), checklists=checklists)
    flash('Login required', 'error')
    return redirect(url_for('login'))

@app.route('/add-checklist', methods=['GET', 'POST'])
def add_checklist():
    if 'user_id' in session:
        name = request.form['name']
        course_id = request.form['course_id']
        user_id = session['user_id']
        checklist = Checklist(name=name, course_id=course_id, user_id=user_id)
        db.session.add(checklist)
        db.session.commit()
        flash('Checklist added successfully', 'success')
        return redirect(url_for('iitm_diploma_detail', course_id=course_id, checklists=Checklist.query.filter_by(user_id=user_id, course_id=course_id).all()))
    flash('Enter the checklist name', 'info')
    return render_template('add-checklist.html', user=None)

@app.route('/mark_completed/<int:checklist_id>')
def mark_completed(checklist_id):
    checklist = Checklist.query.get(checklist_id)
    if checklist:
        checklist.is_completed = True
        db.session.commit()
    return redirect(url_for('iitm_diploma_detail', course_id=checklist.course_id, checklists=Checklist.query.filter_by(user_id=session['user_id'], course_id=checklist.course_id).all()))

@app.route('/mark_incompleted/<int:checklist_id>')
def mark_incompleted(checklist_id):
    checklist = Checklist.query.get(checklist_id)
    if checklist:
        checklist.is_completed = False
        db.session.commit()
    return redirect(url_for('iitm_diploma_detail', course_id=checklist.course_id, checklists=Checklist.query.filter_by(user_id=session['user_id'], course_id=checklist.course_id).all()))

@app.route('/result-prediction', methods=['GET', 'POST'])
def result_prediction():
    flash('We are under development. Please try to open IITM Courses for now.', 'warning')
    return redirect(url_for('index'))

@app.route('/yt-project', methods=['GET', 'POST'])
def yt_project():
    flash('We are under development. Please try to open IITM Courses for now.', 'warning')
    return redirect(url_for('index'))

@app.route('/delete_checklists', methods=['POST'])
def delete_checklists():
    try:
        data = request.get_json()
        checklist_ids = data.get('checklistIds', [])

        # Perform deletion logic here based on the checklist IDs
        for checklist_id in checklist_ids:
            checklist = Checklist.query.get(checklist_id)
            if checklist:
                db.session.delete(checklist)

        db.session.commit()
        flash('Checklists deleted successfully', 'success')
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/rename_checklist/<int:checklist_id>', methods=['POST'])
def rename_checklist(checklist_id):
    checklist = Checklist.query.get(checklist_id)
    if checklist:
        new_name = request.json.get('new_name')
        checklist.name = new_name
        db.session.commit()
        flash('Checklist renamed successfully', 'success')
        return jsonify(success=True)
    else:
        return jsonify(success=False, error='Checklist not found'), 404

# CORS(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
 