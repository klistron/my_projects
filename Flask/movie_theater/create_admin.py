from getpass import getpass
import sys

from webapp import create_app
from webapp.models import db, User

app = create_app()

with app.app_context():
    username = input('Введите login:')
    #first_name = input('Введите имя:')
    #last_name = input('Введите фамилию:')
    #phone = input('Введите телефон:')
    email = input('Введите почту:')

    if User.query.filter(User.username == username).count():
        print('Пользователь уже существует!')
        sys.exit(0)
    
    password1 = getpass('Введите пароль:')
    password2 = getpass('Повторите пароль:')

    if not password1 == password2:
        print('Пароли не совпадают!')
        sys.exit(0)

    new_user = User(username=username, email=email, is_admin=True)
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))