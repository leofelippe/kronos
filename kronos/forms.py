from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from kronos.models import Usuario

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
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=50)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    sessao = BooleanField('Continuar Conectado')
    entrar = SubmitField('Entrar')