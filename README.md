# 🔐 API de Autenticação com Flask

Esta é uma API de autenticação e gerenciamento de usuários desenvolvida com Flask. É uma aplicação simplificada, mas que já cobre os principais fundamentos de segurança e boas práticas:

## 🚀 Funcionalidades

- 🔧 Criação automática do banco de dados com SQLite
- 👤 CRUD completo de usuários
- 🔐 Autenticação com JWT
- 📧 Validação de e-mail real com envio de link de confirmação
- 🔒 Recuperação de senha via e-mail real
- 🌐 Suporte a CORS (Cross-Origin Resource Sharing)

## 🧱 Tecnologias

- Python 3.10+
- Flask
- Flask-JWT-Extended
- Flask-Mail
- Flask-Migrate
- SQLite
- dotenv

## 📁 Estrutura de diretórios

.
├── app.py
├── instance
│   └── db.sqlite
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
├── README.md
├── requirements.txt
└── scr
    ├── controllers
    │   ├── auth.py
    │   ├── models
    │   │   ├── models.py
    │   │   └── __pycache__
    │   │       └── models.cpython-310.pyc
    │   ├── __pycache__
    │   │   ├── auth.cpython-310.pyc
    │   │   └── user.cpython-310.pyc
    │   └── user.py
    ├── db.py
    ├── __pycache__
    │   ├── db.cpython-310.pyc
    │   └── token_utils.cpython-310.pyc
    └── token_utils.py


## Implementações de segurança novas

* Controle de acesso.
* * o usuário tem apenas 3 chances de acessar o sistema, após ele ficará bloqueado.
* Foi criado uma nova rota de acesso para o login de Administradores.
* * No momento a criação de admin, deve ser feita via código direto no sistema.
* * O arquivo se chama : creat_admin.py, nele o administrador deve inserir as informações de admin.
* Todas as rotas estão protegidas com JWT.
* O sistema conta com uma atualizalção de auditoria, onde todas as ações de uso, serão registradas no banco de dados.

    
