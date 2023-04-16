from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if len(email) < 4:
            flash("Неверный формат электронной почты", category="error")
        elif len(firstname) < 2:
            flash("Длина имени должна быть больше, чем 1")
        elif password1 != password2:
            flash("Пароли должны совпадать", category="error")
        elif len(password1) < 7:
            flash("Пароль слишком короткий", category="error")
        else:
            flash("Регистрация успешна!", category="success")
    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "<p>Logout<p>"
