from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'myflasksecretkey123'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'

    mongo.init_app(app)
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
