import sqlite3
from passlib.context import CryptContext

# Configuração do SQLite
DATABASE_NAME = "users.db"

# Criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dados em texto puro
plain_passwords = {
    "admin": {"password": "JKSipm0YH", "role": "admin"},
    "user": {"password": "L0XuwPOdS5U", "role": "user"},
}

# Função para criar o banco e a tabela
def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Cria a tabela de usuários, se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Banco de dados inicializado.")

# Função para inserir usuários no banco
def create_users():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    for username, data in plain_passwords.items():
        # Verifica se o usuário já existe
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            print(f"Usuário '{username}' já existe. Pulando...")
            continue

        # Insere o usuário no banco
        hashed_password = pwd_context.hash(data["password"])
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, data["role"])
        )
        print(f"Usuário '{username}' criado com sucesso.")

    conn.commit()
    conn.close()

# Função para autenticar um usuário
def authenticate_user(username, password):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Busca o usuário no banco
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False
    # Verifica a senha
    return pwd_context.verify(password, user[0])

# Inicializa o banco e cria usuários
if __name__ == "__main__":
    init_db()  # Garante que o banco e a tabela existem
    create_users()  # Adiciona os usuários ao banco
