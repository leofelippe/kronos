# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, EqualTo
from kronos.models import Usuario, Projeto

class FormRegistrar(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    registrar = SubmitField('Registrar')

    def validar_usuario(self, usuario):
        usuario = Usuario.query.filter_by(username=usuario.data).first()
        if usuario:
            raise ValidationError('Usuário já existe')

class FormLogin(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    sessao = BooleanField('Continuar Conectado')
    entrar = SubmitField('Entrar')

class FormEditarUsuario(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    admin = BooleanField('Admin')
    registrar = SubmitField('Atualizar')

    def validar_usuario(self, usuario):
        if usuario.data != current_user.username:
            usuario = Usuario.query.filter_by(username=usuario.data).first()
            if usuario:
                raise ValidationError('Usuário já existe')  

class FormProjeto(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    descricao = TextAreaField('Descrição')
    data_inicio = DateField('Data Início', format='%Y-%m-%d')
    data_entrega = DateField('Data Entrega', validators=[DataRequired()], format='%Y-%m-%d')
    registrar = SubmitField('Criar Projeto')

    def validar_projeto(self, projeto):
            projeto = Projeto.query.filter_by(nome=nome.data).first()
            if projeto:
                raise ValidationError('Projeto já existe')  

class FormEditarProjeto(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=50)])
    descricao = TextAreaField('Descrição')
    data_entrega = DateField('Data Entrega', validators=[DataRequired()], format='%Y-%m-%d')
    registrar = SubmitField('Alterar Projeto')

    def validar_projeto(self, projeto):
            projeto = Projeto.query.filter_by(nome=nome.data).first()
            if projeto:
                raise ValidationError('Projeto já existe')  

class FormRegistro(FlaskForm):
    data = DateField('Data', validators=[DataRequired()], format='%Y-%m-%d')
    total_horas = IntegerField('Horas Trabalhadas', validators=[DataRequired()])
    projeto = SelectField('Projeto', validators=[DataRequired()])
    registrar = SubmitField('Criar Registro')

    def pre_validate(self, form):
        pass
