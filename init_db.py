import sqlite3
import pyotp
import qrcode
from werkzeug.security import generate_password_hash

USERNAME = "teste"
PASSWORD = "Senha@123"

conn = sqlite3.connect("database.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    mfa_secret TEXT NOT NULL
)
""")

secret = pyotp.random_base32()
conn.execute(
    "INSERT OR REPLACE INTO usuarios (username, password_hash, mfa_secret) VALUES (?, ?, ?)",
    (USERNAME, generate_password_hash(PASSWORD), secret),
)
conn.commit()
conn.close()

uri = pyotp.TOTP(secret).provisioning_uri(name=USERNAME, issuer_name="Projeto Teste MFA")
qrcode.make(uri).save("qrcode.png")

print("Banco criado com sucesso!")
print("Usuário: {USERNAME} | Senha: {PASSWORD}")
print("Escaneie o arquivo qrcode.png no app autenticador.")