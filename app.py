from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'sua_senha'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Armazenamento temporário para perfis e vagas
perfis = []
vagas = [
    {"titulo": "Desenvolvedor Python", "habilidades": ["Python", "Django"]},
    {"titulo": "Analista de Dados", "habilidades": ["SQL", "Python"]},
    {"titulo": "Desenvolvedor Frontend",
        "habilidades": ["JavaScript", "React"]},
]

# Página inicial


@app.route('/')
def index():
    return render_template('perfil.html')

# Criação de perfil


@app.route('/criar_perfil', methods=['POST'])
def criar_perfil():
    nome = request.form['nome']
    habilidades = request.form['habilidades'].split(',')
    perfil = {"nome": nome, "habilidades": [
        habilidade.strip() for habilidade in habilidades]}
    perfis.append(perfil)
    return redirect(url_for('buscar_vagas', nome=nome))

# Busca de vagas


@app.route('/buscar_vagas')
def buscar_vagas():
    nome = request.args.get('nome')
    perfil = next((p for p in perfis if p['nome'] == nome), None)
    if perfil:
        vagas_recomendadas = [vaga for vaga in vagas if set(
            perfil['habilidades']).intersection(vaga['habilidades'])]
        return render_template('vagas.html', perfil=perfil, vagas=vagas_recomendadas)
    return redirect(url_for('index'))

# Função para enviar notification por e-mail


def enviar_notificacao_vagas(email):
    msg = Message('Vagas Recomendadas',
                  sender='seu_email@gmail.com', recipients=[email])
    msg.body = 'Obrigado por criar seu perfil! Vamos procurar vagas para você em breve.'
    mail.send(msg)


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=True)
