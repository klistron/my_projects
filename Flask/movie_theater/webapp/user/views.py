from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from webapp.db import db
from webapp.user.models import User
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.main.models import Order

blueprint = Blueprint("user", __name__, url_prefix="/user")


@blueprint.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user.user_page"))
    title = "Регистрация нового пользователя"
    registration_form = RegistrationForm()
    return render_template(
        "user/registration.html", page_title=title, form=registration_form
    )


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        flash(f"Вы уже вошли, как пользователь: {current_user.username}")
        return redirect(url_for("user.user_page"))

    title = "Войдите в свой аккаунт"
    login_form = LoginForm()
    return render_template("user/login.html", page_title=title, form=login_form)


@blueprint.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.check_password(
            form.password.data
        ):  # поменять в будущем на метод проверки когда будет пароль+соль
            login_user(user)

            flash(f"{current_user.username}, Вы успешно вошли в свой аккаунт!")
            return redirect(
                url_for("user.user_page")
            )  # поменять потом на редирект на страницу пользователя
            # или админа(если пользователь админ)
    flash("Неправильный email или пароль")
    return redirect(url_for("user.login"))


@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Вы вышли из аккаунта")
    return redirect(url_for("main.index"))


@blueprint.route("/user_page")
@login_required
def user_page():
    orders = (
        Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    )
    return render_template("user/user_page.html", orders=orders)


@blueprint.route("/process-registration", methods=["POST"])
def process_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=False,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Вы успешно зарегистрировались!")
        return redirect(url_for("user.login"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Поле {getattr(form, field).label.text} - {error}", "danger")
