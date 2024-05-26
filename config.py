from dotenv import dotenv_values

config_env = dotenv_values(".env")


class Config:
    SECRET_KEY = config_env.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config_env.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
