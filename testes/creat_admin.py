import sys
import os

# ADICIONE ESTE BLOCO NO INÍCIO DO ARQUIVO
# Do diretório 'testes', só precisa subir um nível para a raiz do projeto 'Dialo'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
# FIM DO BLOCO

# Agora sim, as importações do seu projeto (app, scr, etc.)
from app import create_app
from scr.db import db
from scr.controllers.models.models import User
from werkzeug.security import generate_password_hash


app = create_app()

with app.app_context():
    # Adicionei a verificação de existência para evitar erros se rodar várias vezes
    existing_user = User.query.filter_by(username="admin").first()
    if existing_user:
        print("Usuário administrador 'test' já existe. Pulando a criação.")
    else:
        admin_user = User(
            username="admin",
            email="admin@dialo.com",
            password_with_hash=generate_password_hash("admin"),
            is_confirmed=True,
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Usuário administrador criado com sucesso.")