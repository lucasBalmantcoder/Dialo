import sys
import os
from werkzeug.security import generate_password_hash

# Adiciona a raiz do projeto ao sys.path.
# Do diretório 'testes', só precisa subir um nível para a raiz do projeto 'Dialo'.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Agora sim, as importações do seu projeto
from app import create_app
from scr.db import db
from scr.controllers.models.models import User

def add_new_user():
    """
    Adiciona um novo usuário ao banco de dados com base na entrada do usuário.
    """
    print("\n--- Adicionar Novo Usuário ---")

    username = input("Digite o nome de usuário: ").strip()
    email = input("Digite o e-mail do usuário: ").strip()
    password = input("Digite a senha do usuário: ").strip()

    if not username or not email or not password:
        print("Erro: Todos os campos (nome de usuário, e-mail, senha) são obrigatórios.")
        return

    app = create_app()

    with app.app_context():
        # Verifica se o nome de usuário ou e-mail já existem para evitar duplicatas
        existing_user_by_username = User.query.filter_by(username=username).first()
        existing_user_by_email = User.query.filter_by(email=email).first()

        if existing_user_by_username:
            print(f"Erro: O nome de usuário '{username}' já existe. Por favor, escolha outro.")
        elif existing_user_by_email:
            print(f"Erro: O e-mail '{email}' já está em uso. Por favor, use outro.")
        else:
            # Gera o hash da senha
            hashed_password = generate_password_hash(password)

            # Cria o novo objeto User
            new_user = User(
                username=username,
                email=email,
                password_with_hash=hashed_password,
                is_confirmed=True,  # Você pode ajustar isso se tiver um processo de confirmação de e-mail
                is_admin=False      # Por padrão, não é admin
            )

            # Adiciona e comita o usuário ao banco de dados
            db.session.add(new_user)
            db.session.commit()

            print(f"\nUsuário '{username}' (ID: {new_user.id}) criado com sucesso!")
            print("-----------------------------------\n")

if __name__ == "__main__":
    add_new_user()
