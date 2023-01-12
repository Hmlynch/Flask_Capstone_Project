from . import bp as app
from .models import User
from flask import render_template, redirect, url_for, request, flash
from app import db
from flask_login import login_user, logout_user, current_user, login_required

# Login Section
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html.j2')

    email = request.form['email']
    password = request.form['password']
    next_url = request.form['next']

    user = User.query.filter_by(email=email).first()

    if user is None:
        flash(f"{email} does not exist...", 'danger')
    elif user.check_my_password(password):
        login_user(user)
        flash(f"Welcome back {user.username}!", 'success')
        if next_url != '':
            return redirect(next_url)
        return redirect(url_for('main.home'))
    else: 
        flash("Password incorrect...", 'danger')
    return render_template('login.html.j2')

# Register Section
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html.j2')
    
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirmPassword']
    first_name = request.form['firstName']
    last_name = request.form['lastName']

    check_user = User.query.filter_by(email=email).first()

    if check_user is not None:
        flash(f"{email} already exist...")
    elif password != confirm_password:
        flash('Password does not match confirm password...')
    else:
        try:
            new_user = User(email=email, username=username, password='', first_name=first_name, last_name=last_name)
            new_user.hash_my_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('New User has now been created!', 'success')
            return redirect(url_for('auth.login'))
        except:
            flash("An error has occured...", 'danger')
    return render_template('register.html.2')

# Logout Section
@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out!', 'success')
    return redirect(url_for('auth.login'))

# Reset Password Section
@app.route('/reset-password', methods=["GET", "POST"])
@login_required
def reset_password():
    if request.method == 'GET':
        return render_template('reset-password.html')

    old_password = request.form['oldPassword']
    confirm_old_password = request.form['confirmOldPassword']
    new_password = request.form['newPassword']

    if old_password != confirm_old_password:
        flash("Confirmation password and password do not match...", 'danger')
    elif not current_user.check_my_password(old_password):
        flash("Old password is not correct...", 'danger')
    else:
        current_user.hash_my_password(new_password)
        db.session.add(current_user)
        db.session.commit()
        flash("Password has been successfully changed!", 'success')
    return render_template('reset-password.html.j2')