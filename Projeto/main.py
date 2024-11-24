from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import sqlite3

# Criptografia e JWT
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_NAME = 'users.db'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI()
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user: 
            return None
        
        if not pwd_context.verify(password, user[1]):
            return None
        
        return {"username": user[0], "role": user[2]}
    
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return None

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Rota para gerar o token
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT username, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user: 
            raise credentials_exception
        return {"username": user[0], "role": user[1]}

    except (JWTError, sqlite3.Error) as e:
        print(f"Erro ao validar o token ou acessar o banco: {e}")
        raise credentials_exception

@app.get("/user")
def read_user_data(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "user":  # Verifica o papel do usuário
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"status":"OK", "message": f"Hello, {current_user['username']}!"}

@app.get("/admin")
def read_admin_data(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":  # Verifica o papel do administrador
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"status":"OK", "message": f"Hello, {current_user['username']}!"}

