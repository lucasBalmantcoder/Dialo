# Importação do dotenv
from dotenv import load_dotenv
load_dotenv()

import os
import click
from flask import Flask, current_app, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, verify_jwt_in_request

# Implementação de envio de e-mails
from flask_mail import Mail, Message

from scr.db import db  # Certifique-se de que esse caminho está correto

from flask_cors import CORS

# Proteção automática de rotasdef protect_all_routes(bp):
def protect_all_routes(bp):
    @bp.before_request
    def before_request():
        # Permitir POST em /users (criação de usuário) sem autenticação
        if request.endpoint == 'users.handler_user' and request.method == 'POST':
            return  # não exige token
        if request.endpoint == 'users' == 'GET':
            return

        verify_jwt_in_request()

migrate = Migrate()

@click.command("init-db")
def init_db_command():
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database")
    
mail = Mail()

def create_app(test_config=None):
     
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "fallback_secreta"),
        SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite",
        JWT_SECRET_KEY="sua_chave_secreta_segura",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        
        # Configurações do Flask-Mail
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),  # seu_email@gmail.com
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),  # senha de app do Gmail
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME"))
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    app.cli.add_command(init_db_command)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    jwt = JWTManager(app)

    # Rota raiz
    @app.route("/")
    def index():
        return "API Flask está funcionando!"

    # Importa Blueprints
    from scr.controllers.user import users as user_blueprint
    from scr.controllers.auth import  auth as auth_blueprint
    from scr.controllers.admin import admin as admin_blueprint

    # Protege rotas do blueprint de usuário
    # protect_all_routes(user_blueprint)

    # Registra Blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    
    app.debug = True
    
    # print("MAIL_USERNAME:", repr(app.config['MAIL_USERNAME']))
    # print("MAIL_PASSWORD:", repr(app.config['MAIL_PASSWORD']))

    return app
