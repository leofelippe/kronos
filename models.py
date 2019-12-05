class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    senha = db.Column(db.String(60), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    registros = db.relationship('RegistroHoras', backref='usuario', lazy=True)

    def __repr__(self):
        return "<Usuario: '{self.id}', '{self.username}', '{self.nome}'>"

class RegistroHoras(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    nome_projeto = db.Column(db.String(50), db.ForeignKey('projeto.nome'), nullable=False, unique=True)
    aprovacao = db.Column(db.Boolean, default=False)
    total_horas = db.Column(db.Integer, nullable=False, default=0)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'), nullable=False)

    def __repr__(self):
        return "<Registro de Horas: '{self.id}', '{self.username}', '{self.nome}'>"

class Projeto(db.Model):
    __tablename__ = 'projetos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_entrega = db.Column(db.DateTime, nullable=False)
    total_horas = db.Column(db.Integer, nullable=False, default=0)
    registros = db.relationship('RegistroHoras', backref='projeto', lazy=True)

    def __repr__(self):
        return "<Projeto: '{self.id}', '{self.projeto}', '{self.data_entrega}'>"