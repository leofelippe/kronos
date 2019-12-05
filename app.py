from flask import Flask, render_template, url_for, request, flash, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import Usuario, Projeto, RegistroHoras
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kronos.db'
db = SQLAlchemy(app)

@app.route('/', methods=['GET',])
def index():
    return render_template('index.html')

@app.route('/usuarios', methods=['GET', 'POST',])
def usuarios():
    if request.method == 'POST':
        nome = request.form['nome']
        username = request.form['username']
        senha = request.form['senha']
        novo_usuario = Usuario(nome=)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect('/usuarios')
        except:
            return 'Erro ao adicionar usuário'

    if request.method == 'GET':
        usuarios = Usuario.query.order_by(Usuario.id).all()
        return render_template('usuarios.html', usuarios=usuarios)

@app.route('/add_usuario', methods=['GET', 'POST',])

@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = Usuario.query.get(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
        flash('Senha incorreta', category='error')
    else:
        flash('Usuário não encontrado', category='error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect('/')