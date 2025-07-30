from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app=app)
    from app import commands
    app.cli.add_command(commands.init_db_command)
    
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app
