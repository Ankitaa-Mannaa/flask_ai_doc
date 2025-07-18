from flask import Flask
<<<<<<< HEAD
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

=======
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

mongo = PyMongo()
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

<<<<<<< HEAD
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

=======
    app.config['SECRET_KEY'] = 'myflasksecretkey123'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'

    mongo.init_app(app)
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
    jwt.init_app(app)

    from .auth import auth_bp
    from .user import user_bp
    from .admin import admin_bp
    from .analyst import analyst_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analyst_bp)

    return app
<<<<<<< HEAD

=======
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
