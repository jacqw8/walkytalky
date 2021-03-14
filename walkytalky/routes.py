from flask import render_template, url_for, flash, redirect, request, send_from_directory, Response
from walkytalky import app, db, bcrypt
from walkytalky.forms import RegistrationForm, LoginForm, CalendarForm, CalendarForm2
from flask_login import login_user, current_user, logout_user, login_required
from walkytalky.models import User
from walkytalky import cal

@app.route("/", methods=['GET'])
def index():
    return render_template('about.html', title='Index')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('about'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('about'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('about'))

@app.route('/home')
def about():
    return render_template('about.html')

timesd = []
@app.route('/avail', methods=['GET', 'POST'])
def avail():
    form = CalendarForm()
    if form.validate_on_submit():
        time = {}
        time['day'] = form.day.data
        time['beg'] = form.input.data
        timesd.append(time)
        return redirect(url_for('myavail'))
    return render_template('avail.html', form=form)

@app.route('/myavail')
def myavail():
    times = cal.check_cal(timesd)
    return render_template('mytime.html', times=times)

@app.route('/deleteavail', methods=['GET', 'POST'])
def editavail():
    form = CalendarForm2()
    if form.validate_on_submit():
        day = form.removeday.data
        time = form.removeinput.data
        remove = {'day': day, 'beg': time}
        if remove in timesd:
            timesd.remove(remove)
        return redirect(url_for('myavail'))
    return render_template('editavail.html', form=form)