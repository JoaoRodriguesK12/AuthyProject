import sqlite3
import pyotp
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "troque-esta-chave-em-producao"


def get_user(username):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    user = conn.execute("SELECT * FROM usuarios WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user


@app.route("/", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        user = get_user(request.form["username"])
        if user and check_password_hash(user["password_hash"], request.form["password"]):
            session.clear()
            session["pre_mfa_user"] = user["username"]
            return redirect(url_for("mfa"))
        erro = "Usuário ou senha inválidos."
    return render_template("login.html", erro=erro)


@app.route("/mfa", methods=["GET", "POST"])
def mfa():
    username = session.get("pre_mfa_user")
    if not username:
        return redirect(url_for("login"))

    erro = None
    if request.method == "POST":
        user = get_user(username)
        token = request.form["token"].strip()
        if pyotp.TOTP(user["mfa_secret"]).verify(token, valid_window=1):
            session.clear()
            session["autenticado"] = username
            return redirect(url_for("validado"))
        erro = "Token inválido ou expirado."
    return render_template("mfa.html", erro=erro)


@app.route("/validado")
def validado():
    if "autenticado" not in session:
        return redirect(url_for("login"))
    return render_template("validado.html")


@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)