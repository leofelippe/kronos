from flask_frozen import Freezer
from kronos import app
from kronos.models import Usuario, Projeto, RegistroHoras

freezer = Freezer(app)

@freezer.register_generator 
def editar_projeto():
    for projeto in Projeto.query.all():
        yield { 'projeto_id': projeto.id }

@freezer.register_generator 
def deletar_projeto():
    for projeto in Projeto.query.all():
        yield { 'projeto_id': projeto.id }

@freezer.register_generator 
def deletar_usuario():
    for usuario in Usuario.query.all():
        yield { 'usuario_id': usuario.id }

@freezer.register_generator 
def editar_usuario():
    for usuario in Usuario.query.all():
        yield { 'usuario_id': usuario.id }

@freezer.register_generator 
def usuario_registros():
    for usuario in Usuario.query.all():
        yield { 'usuario_id': usuario.id }

@freezer.register_generator 
def relatorio():
    for usuario in Usuario.query.all():
        yield { 'usuario_id': usuario.id }

@freezer.register_generator 
def aprovar():
    for registro in RegistroHoras.query.all():
        yield { 'registro_id': registro.id }

@freezer.register_generator 
def reprovar():
    for registro in RegistroHoras.query.all():
        yield { 'registro_id': registro.id }

if __name__ == '__main__':
    freezer.run(debug=True)