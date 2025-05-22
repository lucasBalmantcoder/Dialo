import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click
from scr.db import db

migrate = Migrate()

@click.command("init-db")
def init_db_command():
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database")

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.cli.add_command(init_db_command)

    db.init_app(app)
    migrate.init_app(app, db)

    from scr.controllers.user import app as user_blueprint
    app.register_blueprint(user_blueprint)

    return app
