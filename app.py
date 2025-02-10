from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

app = Flask(__name__)
app.secret_key = "CHAVE_SECREATA"

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form['email']
        telephone = request.form['telephone']
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_user = User.get_by_email(email)
        if existing_user:
            flash("Email already in use", "error")
            return render_template('register.html')

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template('register.html')

        hashed_password = generate_password_hash(password)

        User.create(name=name, email=email, telephone=telephone, password=hashed_password)

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('password')

        user = User.get_by_email(email)

        if not user:
            flash("E-mail not registered!", "error")
            return render_template('login.html')

        if not check_password_hash(user.password, senha):
            flash("Incorrect password!", "error")
            return render_template('login.html')

        login_user(user, remember=True)

        flash("Login successful!", "success")
        return redirect(url_for('index'))

    return render_template('login.html')
