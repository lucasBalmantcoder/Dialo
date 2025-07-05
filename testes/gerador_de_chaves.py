from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

import sys
import os

# Adiciona a raiz do projeto ao sys.path
# Agora, do diretório 'testes', só precisa subir um nível para a raiz do projeto 'Dialo'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Agora sim, importe seus módulos internos
from scr.db import db
from scr.controllers.models.models import User
from app import create_app


def gerar_chaves():
    # Gerar o par de chaves RSA (2048 bits)
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Serializar chave privada em PEM
    pem_privada = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serializar chave pública em PEM
    pem_publica = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return pem_privada.decode(), pem_publica.decode()


# ID do usuário que receberá a chave pública
user_id = 3  # Altere conforme necessário

# Criar app context e salvar chave pública
app = create_app()

with app.app_context():
    priv_key, pub_key = gerar_chaves()

    # Use db.session.get para buscar um objeto pelo ID
    # get_or_404 é um método de Flask-SQLAlchemy que funciona em rotas Flask
    # Para scripts, é melhor usar session.get ou query.get_or_404
    user = db.session.get(User, user_id) # Alterado para db.session.get

    if user:
        user.public_key = pub_key
        db.session.commit()
        print(f"Chave pública atribuída ao usuário {user.username} (ID={user.id}) com sucesso.")
        print("\n=== CHAVE PRIVADA (guarde com segurança) ===\n")
        print(priv_key)
    else:
        print(f"Erro: Usuário com ID={user_id} não encontrado.")