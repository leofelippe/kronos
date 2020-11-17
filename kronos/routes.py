# -*- coding: utf-8 -*-
from flask import render_template, url_for, request, flash, redirect
from kronos import app, db, bcrypt
from kronos.forms import FormRegistrar, FormLogin, FormEditarUsuario, FormProjeto, FormEditarProjeto, FormRegistro
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
     
@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', titulo='Perfil')

@app.route('/relatorio/<int:usuario_id>')
@login_required
def relatorio(usuario_id):
    projetos = Projeto.query.all()
    registros = RegistroHoras.query.filter_by(usuario_id=usuario_id)
    return render_template('relatorio.html', titulo='Relatório Horas/Projeto', registros=registros, projetos=projetos)

#REGISTROS
@app.route('/userpage')
@login_required
def userpage():
    registros = RegistroHoras.query.filter_by(usuario_id=current_user.id)
    return render_template('userpage.html', titulo='Página Inicial', registros=registros)

@app.route('/novo_registro', methods=['GET', 'POST'])
@login_required
def novo_registro():
    projetos = Projeto.query.all()
    form = FormRegistro()
    form.projeto.choices = [(projeto.id, projeto.nome) for projeto in Projeto.query.all()]
    if form.is_submitted():
        projeto = Projeto.query.filter_by(id=form.projeto.data).first()
        registro = RegistroHoras(data=form.data.data, total_horas=form.total_horas.data, 
        usuario_id=current_user.id, projeto_id=projeto.id)
        projeto.total_horas += registro.total_horas
        db.session.add(registro)
        db.session.commit()
        flash('Esforço registrado!', 'success')
        return redirect(url_for('userpage'))
    return render_template('novo_registro.html', titulo='Novo Registro', form=form)

@app.route('/usuario_registros/<int:usuario_id>')
def usuario_registros(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    registros = RegistroHoras.query.filter_by(usuario_id=usuario.id)
    titulo = 'Registros - ' + usuario.nome
    return render_template('usuario_registros.html', titulo =' Registros -' + usuario.nome, registros=registros, usuario=usuario)

@app.route('/aprovar/<int:registro_id>')
def aprovar(registro_id):
    registro = RegistroHoras.query.get_or_404(registro_id)
    registro.aprovacao = True
    db.session.commit()
    flash('Registro aprovado!', 'success')
    return redirect(url_for('usuario_registros', usuario_id=registro.autor.id))

@app.route('/reprovar/<int:registro_id>')
def reprovar(registro_id):
    registro = RegistroHoras.query.get_or_404(registro_id)
    registro.aprovacao = False
    db.session.commit()
    flash('Registro não aprovado!', 'danger')
    return redirect(url_for('usuario_registros', usuario_id=registro.autor.id))

#USUARIOS
@app.route('/usuarios')
@login_required
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', titulo='Usuários Cadastrados', usuarios=usuarios)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = FormRegistrar()
    if form.validate_on_submit():
        senha_encriptada = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(username=form.usuario.data, senha=senha_encriptada, nome=form.nome.data)
        db.session.add(usuario)
        db.session.commit()
        flash(f'Uma conta para '{form.nome.data}' foi criada!', 'success')
        return redirect(url_for('login'))
    return render_template('registrar.html', titulo='Registrar', form=form)

@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    form = FormEditarUsuario()
    if form.validate_on_submit():
        usuario.username = form.usuario.data
        usuario.nome = form.nome.data
        usuario.admin = form.admin.data
        db.session.commit()
        flash(f'Usuário '{usuario.username}' atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios'))
    elif request.method == 'GET':
        form.usuario.data = usuario.username
        form.nome.data = usuario.nome
        form.admin.data = usuario.admin
    return render_template('editar_usuario.html', titulo='Editar Usuário', form=form)

@app.route('/deletar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def deletar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash(f'Usuário '{usuario.username}' removido com sucesso!', 'success')
    return redirect(url_for('usuarios'))   

#PROJETOS
@app.route('/projetos')
@login_required
def projetos():
    projetos = Projeto.query.all()
    return render_template('projetos.html', titulo='Projetos', projetos=projetos)

@app.route('/novo_projeto', methods=['GET', 'POST'])
@login_required
def novo_projeto():
    form = FormProjeto()
    if form.validate_on_submit():
        projeto = Projeto(nome=form.nome.data, descricao=form.descricao.data, 
        data_inicio=form.data_inicio.data, data_entrega=form.data_entrega.data)
        db.session.add(projeto)
        db.session.commit()
        flash(f''{form.nome.data}' foi criado!', 'success')
        return redirect(url_for('projetos'))
    return render_template('novo_projeto.html', titulo='Novo Projeto', form=form)
    
@app.route('/editar_projeto/<int:projeto_id>', methods=['GET', 'POST'])
@login_required
def editar_projeto(projeto_id):
    projeto = Projeto.query.get_or_404(projeto_id)
    form = FormEditarProjeto()
    if form.validate_on_submit():
        projeto.nome = form.nome.data
        projeto.descricao = form.descricao.data
        projeto.data_entrega = form.data_entrega.data
        db.session.commit()
        flash(f'Projeto '{projeto.nome}' atualizado com sucesso!', 'success')
        return redirect(url_for('projetos'))
    elif request.method == 'GET':
        form.nome.data = projeto.nome
        form.descricao.data = projeto.descricao
        form.data_entrega.data = projeto.data_entrega
    return render_template('editar_projeto.html', titulo='Editar Projeto', form=form)

@app.route('/deletar_projeto/<int:projeto_id>', methods=['GET', 'POST'])
@login_required
def deletar_projeto(projeto_id):
    projeto = projeto.query.get_or_404(projeto_id)
    db.session.delete(projeto)
    db.session.commit()
    flash(f'Projeto '{projeto.nome}' removido com sucesso!', 'success')
    return redirect(url_for('projetos'))   

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))