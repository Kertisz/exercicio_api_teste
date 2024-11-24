
# FastAPI com autenticação JWT e SQLite

## Descrição do Projeto

Esta é uma API simples desenvolvida com **FastAPI** para autenticação de usuários usando tokens **JWT**. O banco de dados **SQLite** armazena as informações de usuários, incluindo nomes, senhas criptografadas e roles (funções). A API inclui rotas protegidas que só podem ser acessadas por usuários autenticados.

Desafio proposto pela 200dev para TIVIT
---
## Deixo também a collection do Postman utilizada para o desenvolvimento do teste.
---

## Funcionalidades

1. **Autenticação com JWT:**
   - Geração de tokens JWT para usuários autenticados.
   - Validação de tokens em rotas protegidas.

2. **Rotas Protegidas:**
   - `/user`: Acessível apenas para usuários com o papel `"user"`.
   - `/admin`: Acessível apenas para usuários com o papel `"admin"`.

3. **Banco de Dados SQLite:**
   - Armazenamento de usuários com senhas criptografadas usando **bcrypt**.

---

## Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- SQLite (integrado com Python)

### Configuração do Ambiente

1. **Clone o Repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd <pasta-do-projeto>
   ```

2. **Crie um Ambiente Virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate       # Linux/MacOS
   venv\Scripts\activate          # Windows
   ```

3. **Instale as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o Banco de Dados:**
   O arquivo `generate_data.py` é responsável por criar o banco de dados SQLite (`users.db`), a tabela `users` e popular o banco com os usuários padrão. Execute o seguinte comando para garantir que o banco esteja configurado corretamente:

   ```bash
   python generate_data.py
   ```

---

## Endpoints da API

### **1. `/token` (POST)**
Gera um token JWT para usuários autenticados.

- **Headers:** Nenhum.
- **Body (x-www-form-urlencoded):**
  - `username`: Nome de usuário.
  - `password`: Senha.

- **Exemplo de Resposta (Token Válido):**
  ```json
  {
    "access_token": "<JWT_TOKEN>",
    "token_type": "bearer"
  }
  ```

- **Exemplo de Resposta (Credenciais Inválidas):**
  ```json
  {
    "detail": "Invalid credentials"
  }
  ```

---

### **2. `/user` (GET)**
Retorna uma mensagem personalizada para usuários com o papel `"user"`.

- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`

- **Body:** (enviar no formato `x-www-form-urlencoded` para obter o token JWT antes de acessar as rotas protegidas)
  - `username`: Nome de usuário.
  - `password`: Senha.

- **Exemplo de Resposta (Acesso Permitido):**
  ```json
  {
    "status": "200 OK",
    "message": "Hello, <username>!"
  }
  ```

- **Exemplo de Resposta (Acesso Negado):**
  ```json
  {
    "detail": "Not authorized"
  }
  ```

---

### **3. `/admin` (GET)**
Retorna uma mensagem personalizada para usuários com o papel `"admin"`.

- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`

- **Body:** (enviar no formato `x-www-form-urlencoded` para obter o token JWT antes de acessar as rotas protegidas)
  - `username`: Nome de usuário.
  - `password`: Senha.

- **Exemplo de Resposta (Acesso Permitido):**
  ```json
  {
    "status": "200 OK",
    "message": "Hello, <username>!"
  }
  ```

- **Exemplo de Resposta (Acesso Negado):**
  ```json
  {
    "detail": "Not authorized"
  }
  ```

---

## Estrutura do Banco de Dados

- **Tabela:** `users`
  - `id`: Identificador único do usuário.
  - `username`: Nome de usuário (único).
  - `password`: Senha criptografada.
  - `role`: Papel do usuário (`"user"` ou `"admin"`).

---

## Exemplo de Uso

### Gerar Token:
Use um cliente como **Postman** ou `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/token" -d "username=admin&password=JKSipm0YH"
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
```

### Acessar Rotas Protegidas:

1. Para `/user`:
   ```bash
   curl -H "Authorization: Bearer <JWT_TOKEN>" http://127.0.0.1:8000/user
   ```

2. Para `/admin`:
   ```bash
   curl -H "Authorization: Bearer <JWT_TOKEN>" http://127.0.0.1:8000/admin
   ```


---

Desenvolvido por Gustavo Kertisz Maciel
