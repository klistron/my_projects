from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    first_name = StringField('Имя',validators=[DataRequired()])
    last_name = StringField ('Фамилия', validators=[DataRequired()])
    middle_name = StringField ('Отчество')
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    phone = StringField('Номер телефона', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})



class LoginForm(FlaskForm):
    email = StringField('Введите почту для входа', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Войти', render_kw={"class": "btn btn-primary"})

 