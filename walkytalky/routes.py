from flask import render_template, url_for, flash, redirect, request, send_from_directory, Response
from walkytalky import app, db, bcrypt
from walkytalky.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def index():
    return render_template('index.html', title='Index')

