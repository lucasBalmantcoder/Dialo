from app import create_app
from scr.db import db
from scr.controllers.models.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin_user = User(
        username="test",
        email="test@dialo.com",
        password_with_hash=generate_password_hash("test"),
        is_confirmed=True,
        is_admin=True
    )

    db.session.add(admin_user)
    db.session.commit()

    print("Usuário administrador criado com sucesso.")
    
    