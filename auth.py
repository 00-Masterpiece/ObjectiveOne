import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from forms import RegistrationForm, LoginForm, ChangePasswordForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Welcome back, {}'.format(user.username), category='success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', category='error')

    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already in use', category='error')
                return redirect(url_for('auth.register'))

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Account created successfully!', category='success')
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', category='success')
    return redirect(url_for('main.index'))


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, form.current_password.data):
            flash('Current password is incorrect.', 'error')
        else:
            current_user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('main.profile'))
        
    return render_template('change_password.html', form=form)


@auth.route('/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profile_pic' not in request.files:
        flash('No file part')
        return redirect(url_for('main.profile'))

    file = request.files['profile_pic']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('main.profile'))

    if file:
        filename = secure_filename(file.filename)
        # Optionally rename file to avoid collisions
        ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"user_{current_user.id}.{ext}"

        file_path = os.path.join(current_app.root_path, 'static/profile_pics', new_filename)
        file.save(file_path)

        # Update user's profile picture
        current_user.profile_pic = new_filename
        db.session.commit()

        flash('Profile picture updated!')
    return redirect(url_for('main.profile'))