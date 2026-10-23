from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session
    )

from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from todor import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_name = User.query.filter_by(username = username).first()
        if user_name is not None:
            flash('Ese nombre de usuario ya está en uso.')
            return render_template('auth/register.html')

        user = User(username, generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        flash('Usuario registrado correctamente. Ahora podés iniciar sesión.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username = username).first()

        if user is None or not check_password_hash(user.password, password):
            flash('Usuario o contraseña incorrectos.')
            return render_template('auth/login.html')

        session.clear()
        session['user_id'] = user.id
        return redirect(url_for('index'))

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

