# -*- coding: utf-8 -*-
from datetime import datetime
from kronos import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))

class Data(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.strptime(value, '%d/%m/%Y')
        return value

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    senha = db.Column(db.String(60), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    registros = db.relationship('RegistroHoras', backref='autor', lazy=True)

    def __repr__(self):
        return f"<Usuario: '{self.id}', '{self.username}', '{self.nome}'>"

class RegistroHoras(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(Data, nullable=False)
    aprovacao = db.Column(db.Boolean, default=False)
    total_horas = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)

    def __repr__(self):
        return f"<Registro de Horas: '{self.id}', '{self.autor.nome}', '{self.projeto.nome}','{self.data}'>"

class Projeto(db.Model):
    __tablename__ = 'projetos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text)
    data_inicio = db.Column(Data, nullable=False, default=datetime.utcnow)
    data_entrega = db.Column(Data, nullable=False)
    total_horas = db.Column(db.Integer, nullable=False, default=0)
    registros = db.relationship('RegistroHoras', backref='projeto', lazy=True)

    def __repr__(self):
        return f"<Projeto: '{self.id}', '{self.nome}', '{self.data_entrega}'>"