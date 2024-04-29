from crdf_web import database, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import Date, Time



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    password = database.Column(database.String, nullable=False)
    posts = database.relationship('Post', backref='author', lazy=True)
    languages = database.Column(database.String, nullable=False, default ='not informed')

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_leito = database.Column(database.String, nullable=False)
    status_leito = database.Column(database.String, nullable=False)
    perfil_leito = database.Column(database.String, nullable=False)
    status_paciente = database.Column(database.String, nullable=False)
    nome_paciente = database.Column(database.String, nullable=False)
    data_nascimento = database.Column(Date, nullable=False)
    idade = database.Column(database.Integer, nullable=False)
    pontuario_ses = database.Column(database.Integer, nullable=False)
    data_admissao = database.Column(Date, nullable=False)
    hora_admissao = database.Column(Time, nullable=False)
    data_obito = database.Column(Date, nullable=False)
    hora_obito = database.Column(Time, nullable=False)
    data_transferencia = database.Column(Date, nullable=False)
    hora_transferencia = database.Column(Time, nullable=False)
    data_alta = database.Column(Date, nullable=False)
    hora_alta = database.Column(Time, nullable=False)
    nome_colaborador = database.Column(database.String, nullable=False)
    matricula_colaborador = database.Column(database.String, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)