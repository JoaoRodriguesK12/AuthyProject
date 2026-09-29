# AuthyProject

Projeto de teste de **autenticação em duas etapas (MFA)** feito em Python com Flask e SQLite.

O usuário entra com login e senha e, em seguida, precisa informar o código de 6 dígitos (TOTP) gerado por um app autenticador, como Google Authenticator, Microsoft Authenticator ou Authy. Só depois disso a página "Você foi validado" é liberada.

## Fluxo do sistema

1. **Login**: usuário e senha.
2. **Validação MFA**: código de 6 dígitos do app autenticador.
3. **Página final**: "Você foi validado ✅".

## Tecnologias

- Python 3
- Flask (servidor web)
- SQLite (banco de dados de teste)
- PyOTP (geração e validação do token TOTP)
- qrcode (geração do QR Code para o app autenticador)

## Estrutura do projeto

```
AuthyProject/
├── app.py            # servidor Flask e rotas
├── init_db.py        # cria o banco, o usuário de teste e o QR Code
├── requirements.txt  # dependências
├── .gitignore
├── README.md
└── templates/
    ├── login.html
    ├── mfa.html
    └── validado.html
```

## Pré-requisitos

- [Python 3](https://www.python.org/downloads/) instalado (marque **Add python.exe to PATH** na instalação)
- [VS Code](https://code.visualstudio.com/) com a extensão **Python**
- [Git](https://git-scm.com/downloads)
- App autenticador no celular (Google Authenticator, Microsoft Authenticator ou Authy)

## Como rodar (passo a passo)

### 1. Baixe o projeto

```bash
git clone https://github.com/JoaoRodriguesK12/AuthyProject.git
cd AuthyProject
```

Depois abra a pasta no VS Code (**File → Open Folder**) e abra o terminal com `Ctrl + '`.

### 2. Crie e ative o ambiente virtual

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

No Linux/Mac use `source venv/bin/activate`.

Quando ativar, aparece **(venv)** no começo da linha do terminal.

Se der erro de execução de scripts no PowerShell, rode uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 3. Instale as dependências

```powershell
pip install -r requirements.txt
```

Ou, manualmente:

```powershell
pip install flask pyotp "qrcode[pil]"
```

### 4. Crie o banco de dados e o QR Code

```powershell
python init_db.py
```

Esse comando cria:

- `database.db`: banco SQLite com o usuário de teste
- `qrcode.png`: QR Code com a chave secreta do MFA

Mensagem esperada: **"Banco criado com sucesso!"**

### 5. Configure o app autenticador

1. No VS Code, clique em `qrcode.png` para abrir a imagem.
2. No celular, abra o app autenticador e escolha **adicionar conta / escanear QR Code**.
3. Escaneie a imagem. Vai aparecer a conta **Projeto Teste MFA (teste)** com um código de 6 dígitos que muda a cada 30 segundos.

### 6. Inicie o servidor

```powershell
python app.py
```

### 7. Acesse e teste

Abra no navegador: **http://127.0.0.1:5000**

| Campo   | Valor       |
|---------|-------------|
| Usuário | `teste`     |
| Senha   | `Senha@123` |

Depois digite o código de 6 dígitos que está no app. Se estiver correto, aparece a página **"Você foi validado"**.

## Rotas

| Rota        | Função                                          |
|-------------|-------------------------------------------------|
| `/`         | Página de login (usuário e senha)               |
| `/mfa`      | Validação do token de 6 dígitos                 |
| `/validado` | Página final, só acessível após login + MFA     |
| `/sair`     | Encerra a sessão                                |

## Banco de dados

Tabela `usuarios`:

| Coluna          | Descrição                                   |
|-----------------|---------------------------------------------|
| `id`            | Identificador                               |
| `username`      | Nome do usuário (único)                     |
| `password_hash` | Senha armazenada com hash (nunca em texto)  |
| `mfa_secret`    | Chave secreta usada para gerar o TOTP       |

Para visualizar o banco no VS Code, instale a extensão **SQLite Viewer** e clique em `database.db`.

## Problemas comuns

**"Python was not found"**: instale o Python pelo python.org marcando *Add to PATH* e reinicie o VS Code.

**"No module named 'pyotp'"**: o ambiente virtual não está ativo ou as dependências não foram instaladas. Ative o `venv` e rode `pip install -r requirements.txt`.

**Token sempre inválido**: confira se a data e a hora do computador e do celular estão em **ajuste automático**. O TOTP depende do relógio.

**Trocou de máquina ou perdeu o QR Code**: rode `python init_db.py` de novo. Ele gera uma chave nova; apague a conta antiga do app e escaneie o novo QR Code.

**`git` não reconhecido**: instale o Git e reinicie o VS Code.

## Segurança

Este é um projeto de **teste**. Para uso real, seria necessário:

- Guardar a `secret_key` do Flask em variável de ambiente
- Usar HTTPS
- Limitar tentativas de login e de token
- Criar cadastro de usuários e códigos de recuperação do MFA

Os arquivos `database.db` e `qrcode.png` **não são enviados ao GitHub** (estão no `.gitignore`), pois o QR Code contém a chave secreta do MFA. Cada pessoa que rodar o projeto gera os seus com `python init_db.py`.

## Autor

João Vitor Rodrigues ([@JoaoRodriguesK12](https://github.com/JoaoRodriguesK12))
