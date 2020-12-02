from flask import Flask
from flask_login import LoginManager
from inventory.config import Config


login_manager = LoginManager()
login_manager.login_view = "main.home"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)

    from inventory.main.routes import main
    from inventory.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app
