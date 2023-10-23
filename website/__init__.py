from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:maestro@localhost/fullweb'
    db.init_app(app)

    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    # create_database(app)

    Login_manager = LoginManager()
    Login_manager.login_view = 'auth.login'
    Login_manager.init_app(app)

    @Login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app

# def create_database(app):
#     db.create_all(app=app)
#     print('Created Database!')