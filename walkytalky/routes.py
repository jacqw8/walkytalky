from flask import render_template, url_for, flash, redirect, request, send_from_directory, Response
from walkytalky import app
from walkytalky.forms import RegistrationForm, LoginForm

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('about.html')
