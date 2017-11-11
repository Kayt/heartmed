import datetime
import os

from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc
from werkzeug.utils import secure_filename
 
from heart import app, db, login_manager, basic_auth, classifier, np, pd, sc, X_test
from models import User, Doctor, PatientFeedBack, DoctorFeedBack, Query, Response
from forms import LoginForm, SignupForm, AddUserForm, UserProfileForm, FeedbackForm, DiagnosisForm, AssignDocForm, DocFeedbackForm, DoctorProfileForm
from methods import float_formatter, get_doc, get_status, generate_res


@login_manager.user_loader
def load_user(userid):
	return User.query.get(int(userid))


# Patient Views 
@app.route('/', methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            if user.role == 'Patient':
                login_user(user, form.remember_me.data)
                flash("logged in successfully as {}".format(user.username))
                return redirect(request.args.get('next') or url_for('home'))
            flash(" You can not log into a Patient account using a doctor Account")
        flash("Incorrect username or password")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password_hash=form.password.data, role='Patient')
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route('/home')
@login_required
def home():
    print classifier.predict(X_test)
    return render_template('home.html')

@app.route('/edit_profile/<id>', methods=["GET","POST"])
@login_required
def editProfile(id):
    user = User.query.get(id)
    form = UserProfileForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        user.name = form.name.data
        user.surname = form.surname.data
        user.gender = form.gender.data
        user.weight = form.weight.data
        user.height = form.height.data 
        user.location = form.location.data
        user.email = form.email.data
        user.bio = form.about_me.data
        user.pic = filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.add(user)
        db.session.commit()
        flash('Updates were saved', 'message')
        return redirect(url_for('home'))
    form.name.data = user.name
    form.surname.data = user.surname
    form.gender.data = user.gender
    form.weight.data = user.weight
    form.height.data = user.height
    form.location.data = user.location
    form.email.data = user.email
    form.about_me.data = user.bio
    form.photo.data = user.pic
    return render_template('editProfile.html', user=user, form=form)

@app.route('/upload/<id>', methods=["GET", "POST"])
@login_required
def upload(id):
    user = User.query.get(id)
    form = UploadForm()
    if form.validate_on_submit():
        pic = form.photo.data
        filename = secure_filename(pic.filename)
        user.profile_picture = filename
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('profile', id=user.id))
    return render_template('profile.html#squarespaceModal', form=form, id = user.id)

@app.route('/profile/<id>')
def profile(id):
    patient = User.query.get(id)
    return render_template('profile.html')

@app.route('/viewPatient/<id>/<user>')
def viewPatient(id, user):
    doc = Doctor.query.get(id)
    patient = User.query.get(user)
    return render_template('patient.html', doc=doc, patient=patient)

@app.route('/selfDiagnosis', methods=["GET", "POST"])
def analyze():
    form = DiagnosisForm()
    if form.validate_on_submit():
        print type(form.slope.data)
        print form.slope.data
        chestpain = int(form.chestpain.data)
        slope = int(form.slope.data)
        sex = 1 if form.sex.data == 'Male' else 0

        print np.array([[form.age.data, sex, chestpain, form.heartrate.data, form.cholesterol.data,
                                    1, form.bloodsugar.data, form.angina.data, form.peak.data, form.vessel.data, form.electro.data, form.thal.data]])

        print 'i passed the first np array print'

        new_pred = classifier.predict(sc.transform(np.array([[form.age.data, sex, chestpain, form.bloodpressure.data, form.cholesterol.data, form.bloodsugar.data,
                                    form.electro.data, form.heartrate.data, form.angina.data, form.peak.data, slope, form.vessel.data, form.thal.data]])))

        print 'i passed the prediction'

        res = generate_res(new_pred)
        print res
        print type(float_formatter(new_pred))
        print new_pred
            
        user = current_user
        user.flagged = get_status(res)
        db.session.add(user)
        db.session.commit()
        flash('Diagnosis done', 'message')
        return redirect(url_for('result', res=res))
    return render_template('analyze.html', form=form)

@app.route('/result/<res>')
def result(res):
    return render_template('result.html', res=res)

@app.route('/my_doctor/<id>')
@login_required
def my_doctor(id):
    doc = Doctor.query.get(id)
    return render_template('doctor.html', doc=doc)

@app.route('/submitFeedback', methods=["GET","POST"])
@login_required
def submitFeedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        new = PatientFeedBack(content=form.content.data, patient_id=current_user.id)
        db.session.add(new)
        db.session.commit()
        flash('Feedback Submitted', 'message')
        return redirect(url_for('home'))
    return render_template('submitFeedback.html', form=form)

@app.route('/allmessages')
def allMessages():
    messages = Query.query.filter_by(patient_id=current_user.id)
    return render_template('messages.html', messages=messages)

@app.route('/sendMessage', methods=["GET", "POST"])
def sendMessage():
    form = FeedbackForm()
    if form.validate_on_submit():
        new = Query(content=form.content.data, name=current_user.username, patient_id=current_user.id, doctor_id=current_user.mydoctor)
        db.session.add(new)
        db.session.commit()
        flash('Message sent', 'message')
        return redirect(url_for('home'))
    return render_template('sendMessage.html', form=form)

@app.route('/signs')
def signs():
    return render_template('signs.html')

@app.route('/prevention')
def prevention():
    return render_template('prevention.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')


# Doctor's Views

@app.route('/doclogin', methods=["GET","POST"])
def docLogin():
    form = LoginForm()
    if form.validate_on_submit():
        user = Doctor.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("logged in successfully as {}".format(user.username))
            return redirect(url_for('docHome', id=user.id))
            flash("Incorrect username or password")
    return render_template("doclogin.html", form=form)

@app.route('/docHome/<id>')
def docHome(id):
    doc = Doctor.query.get(id)
    return render_template('dochome.html', doc=doc)

@app.route('/docmessages/<id>')
def docMessages(id):
    doc = Doctor.query.get(id)
    messages = Query.query.filter_by(doctor_id=id)
    return render_template('docmessages.html', messages=messages, doc=doc)


@app.route('/docProfile/<id>', methods=["GET", "POST"])
def docProfile(id):
    doc = Doctor.query.get(id)
    return render_template('docProfile.html', doc=doc)


@app.route('/edit_doctor/<id>', methods=["GET", "POST"])
def editDocProfile(id):
    doc = Doctor.query.get(id)
    form = DoctorProfileForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        doc.name = form.name.data
        doc.surname = form.surname.data
        doc.gender = form.gender.data
        doc.email = form.email.data
        doc.achievements = form.achievements.data
        doc.years_in_practice = form.years_in_practice.data
        doc.rank = form.rank.data
        doc.career = form.career.data
        doc.bio = form.about_me.data
        doc.pic = filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('docProfile', id=doc.id))
    form.name.data = doc.name 
    form.surname.data = doc.surname 
    form.gender.data = doc.gender
    form.email.data = doc.email 
    form.achievements.data = doc.achievements
    form.years_in_practice.data = doc.years_in_practice
    form.rank.data = doc.rank 
    form.career.data = doc.career
    form.about_me.data = doc.bio
    form.photo.data = doc.pic
    return render_template('editDoctor.html', doc=doc, form=form)


@app.route('/viewPatients/<id>')
def viewPatients(id):
    doc = Doctor.query.get(id)
    return render_template('patients.html', doc=doc)

@app.route('/messagePatient/<id>/<query>', methods=["GET","POST"])
def messagePatient(id, query):
    doc = Doctor.query.get(id)
    form = FeedbackForm()
    if form.validate_on_submit():
        new = Response(content=form.content.data, doctor_id=doc.id, query_id=query)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('docMessages', id=doc.id))
    return render_template('respond.html', doc=doc, form=form)

@app.route('/submitDocFeedback/<id>', methods=["GET","POST"])
@login_required
def submitDocFeedback(id):
    doc = Doctor.query.get(id)
    form = DocFeedbackForm()
    if form.validate_on_submit():
        new = DoctorFeedBack(content=form.content.data, patient=form.patient.data, doctor_id=doc.id)
        db.session.add(new)
        db.session.commit()
        flash('Feedback Submitted')
        return redirect(url_for('home'))
    return render_template('submitFeedback.html', form=form)



# Admin Views 

@app.route('/admin')
@basic_auth.required
def dashboard():
    users = User.query.all()
    doctors = Doctor.query.all()
    return render_template('dashboard.html', users=users, doctors=doctors)

@app.route('/viewFlags')
def viewFlagged():
    users = User.query.filter_by(flagged=True)
    return render_template('flagged.html', users=users)

@app.route('/asignDoc/<id>', methods=["GET","POST"])
def assigndoc(id):
    user=User.query.get(id)
    form = AssignDocForm()
    form.doctor.choices = [(doc.username, doc.username) for doc in Doctor.query.all() ]
    if form.validate_on_submit():
        user.mydoctor = get_doc(form.doctor.data)
        db.session.add(user)
        db.session.commit()
        flash('Patient assigned')
        return redirect(url_for('viewFlagged'))
    form.username.data = user.username
    return render_template('assign.html', form=form)


@app.route('/addUser', methods=["GET","POST"])
def addUser():
    form = AddUserForm()
    if form.validate_on_submit():
        new = Doctor(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        db.session.add(new)
        db.session.commit()
        flash('New {} added!!'.format(new.username))
        return redirect(url_for('dashboard'))
    return render_template('addUser.html', form=form)

@app.route('/deleteUser/<id>', methods=["GET", "POST"])
def deleteUser(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/deleteDoc/<id>', methods=["GET", "POST"])
def deleteDoc(id):
    Doctor.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/patientFeedback', methods=["GET","POST"])
def viewPatientFeedback():
    feedback = PatientFeedBack.query.all()
    return render_template('patientsFeedback.html', feedback=feedback)
