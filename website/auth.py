from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask import session
from flask_login import login_user, logout_user, login_required, current_user   

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('user_first_name', None)
    session.pop('user_last_name', None)
    session.pop('user_password', None)
    session.pop('user_created_at', None)
    session.pop('user_updated_at', None)
    session.pop('user_deleted_at', None)
    session.pop('user_is_active', None)
    session.pop('user_is_admin', None)
    session.pop('user_is_staff', None)
    session.pop('user_is_superuser', None)
    session.pop('user_last_login', None)
    session.pop('user_date_joined', None)
    session.pop('user_groups', None)
    session.pop('user_permissions', None)
    session.pop('user_is_authenticated', None)
    session.pop('user_is_anonymous', None)
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash("Email must be greater than 3 characters", category='error')
        elif len(first_name) < 2 and len(last_name) < 2:
            flash('First name and last name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash("Passwords don't match", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters", category='error')
        elif User.query.filter_by(email=email).first():
            flash("Email already exists", category='error')
        
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")