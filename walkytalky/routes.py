from flask import render_template, url_for, flash, redirect, request, send_from_directory, Response, jsonify, abort
from walkytalky import app, db, bcrypt
from walkytalky.forms import RegistrationForm, LoginForm, CalendarForm, CalendarForm2, PostForm, SearchFriend
from flask_login import login_user, current_user, logout_user, login_required
from walkytalky.models import User, Post
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

@app.route("/updateavail", methods=['GET', 'POST'])
@login_required
def updateavail():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('times'))
    return render_template('updateavail.html', form=form)

@app.route("/times")
@login_required
def times():
    posts = Post.query.all()
    for post in posts:
        if post.author != current_user:
            abort(403)
    return render_template('times.html', posts=posts)

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('times'))

# @app.route("/friends")
# @login_required
# def friends():
#     form = SearchFriend()
#     if form.validate_on_submit():
#         friends = form.search.data
#         return render_template('friends.html', friends=friends)
#     return render_template('search.html', form=form)

all_users = []
@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    all_users = jsonify(users=[i.serialize for i in users])
    return all_users

# @app.route('/post_user', methods=['POST'])
# def post_user():
#     data = request.get_json()
#     user = User(data['username'], data['email'])
#     db.session.add(user)
#     db.session.commit()
#     return jsonify(**data)