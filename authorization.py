from flask import Blueprint, render_template, request, flash, redirect, url_for
from data.users import User
from data import db_session
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(email=email).first()
        if user:
            flash("Аккаунт с данным email уже существует.")
        elif len(email) < 4:
            flash("Неверный формат электронной почты.", category="error")
        elif len(firstname) < 2:
            flash("Длина имени должна быть больше, чем 1.")
        elif password1 != password2:
            flash("Пароли должны совпадать.", category="error")
        elif len(password1) < 7:
            flash("Пароль слишком короткий.", category="error")
        else:
            new_user = User()
            new_user.email = email
            new_user.password = generate_password_hash(password1, method="sha256")
            new_user.first_name = firstname
            db_sess = db_session.create_session()
            db_sess.add(new_user)
            db_sess.commit()
            db_sess.close()
            flash("Регистрация успешна!", category="success")
            return redirect(url_for("view.homepage"))
    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Вы успешно вошли в аккаунт!", category="success")
                return redirect(url_for("view.homepage"))
            else:
                flash("Неверный пароль, попробуйте снова.", category="error")
        db_sess.close()
    else:
        flash("Пользователя с указанным email не существует.", category="error")


@auth.route("/logout")
def logout():
    return "<p>Logout<p>"
