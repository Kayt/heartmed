from datetime import date

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from heart import db 

def get_name(id):
    user = User.query.get(id)
    return user.name

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    query_id = db.Column(db.Integer, db.ForeignKey('query.id'))

    def __init__(self, content, doctor_id, query_id):
        self.content = content
        self.doctor_id = doctor_id
        self.query_id = query_id

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    name = db.Column(db.String(100))
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    responses = db.relationship('Response', backref='query', lazy='dynamic')

    def __init__(self, content,name, patient_id, doctor_id):
        self.content = content
        self.name = name
        self.patient_id = patient_id
        self.doctor_id = doctor_id

class DoctorFeedBack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    patient = db.Column(db.String(100))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

    def __init__(self, content, patient, doctor_id):
        self.content = content
        self.patient = patient
        self.doctor_id = doctor_id

    def __repr__(self):
        return '<FeedBack %r>' % self.content

class PatientFeedBack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    name = db.Column(db.String(100))
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, content, patient_id):
        self.content = content
        self.patient_id = patient_id
        self.name = get_name(patient_id)

    def __repr__(self):
        return '<FeedBack %r>' % self.content


class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(80))
    achievements = db.Column(db.Text)
    years_in_practice = db.Column(db.Integer)
    rank = db.Column(db.String(100))
    career = db.Column(db.Text)
    bio = db.Column(db.Text)
    pic = db.Column(db.String(200))
    feedback = db.relationship('DoctorFeedBack', backref='doctor', lazy='dynamic')
    response = db.relationship('Response', backref='doctor', lazy='dynamic')
    patients = db.relationship('User', backref='doctor', lazy='dynamic')
    messages = db.relationship('Query', backref='doctor', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return Doctor.query.filter_by(username=username).first()

    def __init__(self, username, email, password_hash ):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password_hash)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    location = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(80))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    bio = db.Column(db.Text)
    pic = db.Column(db.String(200))
    role = db.Column(db.String(20))
    flagged = db.Column(db.Boolean)
    feedback = db.relationship('PatientFeedBack', backref='user', lazy='dynamic')
    message = db.relationship('Query', backref='user', lazy='dynamic')
    mydoctor = db.Column(db.Integer, db.ForeignKey('doctor.id'))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, email, password_hash, role):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password_hash)
        self.role = role


