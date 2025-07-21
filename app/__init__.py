from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    jwt.init_app(app)

    from .auth import auth_bp
    from .user import user_bp
    from .admin import admin_bp
    from .analyst import analyst_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analyst_bp)

    @app.route("/")
    def health():
        return "API is running!", 200

    return app
