import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://movie:movie@localhost/movie'
SECRET_KEY = "whhfsdfpsflweazczlczlcvxcv"

SQLALCHEMY_TRACK_MODIFICATIONS = False
