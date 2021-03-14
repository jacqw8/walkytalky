from flask import render_template, url_for, flash, redirect, request, send_from_directory, Response, jsonify, abort
from walkytalky import app, db, bcrypt
from walkytalky.forms import RegistrationForm, LoginForm, CalendarForm, CalendarForm2, PostForm, SearchFriend, AddWalksForm
from flask_login import login_user, current_user, logout_user, login_required
from walkytalky.models import User, Post, Walk
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
    posts2 = Post.query.all()
    posts = list()
    for post in posts2:
        if post.author == current_user:
            posts.append(post)
    return render_template('times.html', posts=posts)

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('times'))

user = []
@app.route("/friends", methods=['GET', 'POST'])
@login_required
def friends():
    form = SearchFriend()
    if form.validate_on_submit():
        friend_username = form.search.data
        user.append(friend_username)
        try:
            friend = User.query.filter_by(username=friend_username).first()
            user.append(friend.email)
            posts2 = Post.query.all()
            posts = list()
            for post in posts2:
                if post.author.username == friend.username:
                    posts.append(post)
            posts1 = list()
            for post in posts2:
                if post.author == current_user:
                    posts1.append(post)
            return render_template('friends.html', posts=posts, posts1=posts1)
        except:
            flash("Doesn't exist!", 'danger')
    return render_template('search.html', form=form)

@app.route("/mywalks")
@login_required
def mywalks():
    posts = Walk.query.all()
    return render_template('mywalks.html', posts=posts)

@app.route("/updatewalks", methods=['GET', 'POST'])
@login_required
def updatewalks():
    form = AddWalksForm()
    if form.validate_on_submit():
        post = Walk(title=form.title.data, location=form.location.data, day=form.day.data, start=form.start.data,
                    end=form.end.data, distance=form.distance.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your walk has been created!', 'success')
        return redirect(url_for('mywalks'))
    return render_template('updatewalks.html', form=form)


@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    all_users = jsonify(users=[i.serialize for i in users])
    return all_users

@app.route('/request')
def request():
    username = user[0]
    email = user[1]
    user.pop()
    user.pop()
    posts = []
    dict1 = {}
    dict1['user'] = username
    dict1['email'] = email
    posts.append(dict1)
    return render_template('request.html', posts=posts)
