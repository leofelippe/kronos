from flask import render_template, url_for, request, flash, redirect
from kronos import app, db, bcrypt
from kronos.forms import FormRegistrar, FormLogin
from kronos.models import Usuario, Projeto, RegistroHoras
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST',])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('userpage'))
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.usuario.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=form.sessao.data)
            proxima_pagina = request.args.get('next')
            return redirect(proxima_pagina) if proxima_pagina else redirect(url_for('userpage'))
        else:
            flash('Não foi possível logar. Por favor, cheque os dados e tente novamente!', 'danger')
    return render_template('login.html', titulo='Login', form=form)
     
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = FormRegistrar()
    if form.validate_on_submit():
        senha_encriptada = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(username=form.usuario.data, senha=senha_encriptada, nome=form.nome.data)
        db.session.add(usuario)
        db.session.commit()
        flash(f'Uma conta para {form.nome.data} foi criada! Efetue o login para continuar', 'success')
        return redirect(url_for('login'))
    return render_template('registrar.html', titulo='Registrar', form=form)

@app.route('/userpage')
@login_required
def userpage():
    return render_template('userpage.html', titulo='Página Inicial')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/relatorio')
@login_required
def relatorio():
    return render_template('relatorio.html', title='Relatório Horas/Projeto')

@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', title='Usuários Cadastrados')

@app.route('/projetos')
@login_required
def projetos():
    return render_template('projetos.html', title='Projetos')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', title='Perfil')