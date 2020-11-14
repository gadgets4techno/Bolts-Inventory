from flask import Flask
from inventory.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from inventory.main.routes import main
    from inventory.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app