🔐 API de Autenticação com Flask
Esta é uma API de autenticação e gerenciamento de usuários desenvolvida com Flask. É uma aplicação simplificada, mas que já cobre os principais fundamentos de segurança e boas práticas:

🚀 Funcionalidades
🔧 Criação automática do banco de dados com SQLite

Como funciona: O banco de dados SQLite é criado automaticamente e seu esquema é gerenciado através de migrações.

Bibliotecas: Flask-SQLAlchemy, Flask-Migrate.

👤 CRUD completo de usuários

Como funciona: Permite criar, ler, atualizar e deletar (Create, Read, Update, Delete) informações de usuários no sistema.

Bibliotecas: Flask-SQLAlchemy.

🔐 Autenticação com JWT

Como funciona: Utiliza JSON Web Tokens para autenticar usuários, garantindo que apenas usuários autorizados possam acessar rotas protegidas.

Bibliotecas: Flask-JWT-Extended.

📧 Validação de e-mail real com envio de link de confirmação

Como funciona: Envia um e-mail de confirmação com um link seguro para verificar a validade do endereço de e-mail do usuário.

Bibliotecas: Flask-Mail, itsdangerous.

🔒 Recuperação de senha via e-mail real

Como funciona: Permite que usuários redefinam suas senhas através de um link de recuperação enviado para seu e-mail cadastrado.

Bibliotecas: Flask-Mail, itsdangerous.

🌐 Suporte a CORS (Cross-Origin Resource Sharing)

Como funciona: Habilita a comunicação segura entre o frontend (rodando em um domínio diferente) e o backend, permitindo requisições de origem cruzada.

Bibliotecas: Flask-Cors.

🔑 Criptografia de Mensagens Ponta a Ponta (E2E):

Como funciona: As mensagens são criptografadas no dispositivo do remetente e só podem ser descriptografadas no dispositivo do destinatário. Utiliza um par de chaves assimétricas (RSA) para trocar chaves simétricas (AES), que por sua vez criptografam o conteúdo real da mensagem.

Bibliotecas: cryptography (Python, para geração de chaves no backend, se usado), jsencrypt (JavaScript, para RSA no frontend), crypto-js (JavaScript, para AES no frontend).

🔒 Gerenciamento de Chaves Públicas:

Como funciona: As chaves públicas RSA dos usuários são geradas no frontend (ou via script) e armazenadas no banco de dados. Elas são usadas por outros usuários para criptografar mensagens destinadas a eles. A chave privada correspondente é armazenada localmente no dispositivo do usuário (ex: localStorage).

Bibliotecas: Flask-SQLAlchemy, cryptography (Python), jsencrypt (JavaScript).

🧹 Sanitização de Entradas JSON:

Como funciona: Antes que os dados JSON de uma requisição cheguem à lógica da rota, eles são processados para remover tags HTML maliciosas (<script>, <iframe>) e caracteres perigosos, prevenindo ataques como Cross-Site Scripting (XSS) e injeção.

Bibliotecas: re (módulo re do Python).

💬 Gerenciamento de Salas de Chat:

Como funciona: Permite a criação de novas salas de chat, a listagem das salas existentes (às quais o usuário pertence), a obtenção de detalhes de uma sala específica, e a atualização/exclusão de salas (pelo criador).

Bibliotecas: Flask-SQLAlchemy.

🤝 Associação de Usuários a Salas:

Como funciona: Controla explicitamente quais usuários são membros de quais salas de chat através de uma tabela de associação, garantindo que apenas membros autorizados possam acessar o conteúdo da sala.

Bibliotecas: Flask-SQLAlchemy.

✉️ Envio e Listagem de Mensagens Criptografadas:

Como funciona: Rotas dedicadas para receber mensagens já criptografadas do frontend e armazená-las no banco de dados, e para recuperá-las para o frontend. O backend não descriptografa as mensagens, apenas as armazena e entrega.

Bibliotecas: Flask-SQLAlchemy.

🧱 Tecnologias
Python 3.10+

Flask

Flask-JWT-Extended

Flask-Mail

Flask-Migrate

SQLite

dotenv

cryptography (para geração de chaves RSA no backend, se usado)

Flask-Cors (para suporte a CORS)

📁 Estrutura de diretórios
.
├── app.py
├── instance
│   └── db.sqlite
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   └── versions/
│       └── <seus_arquivos_de_migracao>.py
├── README.md
├── requirements.txt
└── scr
    ├── controllers
    │   ├── admin.py       # Novo: Módulo para funcionalidades administrativas (se implementado)
    │   ├── auth.py
    │   ├── models
    │   │   ├── models.py
    │   │   └── __pycache__
    │   │       └── models.cpython-310.pyc
    │   ├── message.py     # Novo: Módulo para gerenciamento de mensagens
    │   ├── room.py        # Novo: Módulo para gerenciamento de salas
    │   ├── __pycache__
    │   │   ├── auth.cpython-310.pyc
    │   │   ├── user.cpython-310.pyc
    │   │   ├── message.cpython-310.pyc
    │   │   └── room.cpython-310.pyc
    │   └── user.py
    ├── db.py
    ├── __pycache__
    │   ├── db.cpython-310.pyc
    │   ├── token_utils.cpython-310.pyc
    │   └── utils.cpython-310.pyc
    ├── token_utils.py
    └── utils              # Novo: Pasta para utilitários
        ├── __init__.py
        └── sanitization.py # Novo: Módulo para funções de sanitização