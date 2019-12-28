from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_message='Do login first!!!'
#login_manager.session_protection
#login_manager.user_callback
#login_manager.request_loader()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    login_manager.init_app(app)
    from app.auth import auth_bp
    from app.route import main_bp
    from app.lander import general_bp
    db.init_app(app)
    with app.app_context():
        # Import parts of our application
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(general_bp)

        # Initialize Global db
        db.create_all()
        app.debug=True
        return app
