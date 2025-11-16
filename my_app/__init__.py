from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    from my_app.resources.user import blp as UserBlueprint
    from my_app.resources.category import blp as CategoryBlueprint
    from my_app.resources.record import blp as RecordBlueprint
    from my_app.resources.currency import blp as CurrencyBlueprint

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(RecordBlueprint)
    api.register_blueprint(CurrencyBlueprint)
    
    return app