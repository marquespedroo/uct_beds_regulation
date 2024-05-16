from crdf_web import database, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy import Date, Time, func
from pytz import timezone
from flask_bcrypt import bcrypt



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    password = database.Column(database.String, nullable=False)
    posts = database.relationship('Post', backref='author', lazy=True)

    def set_password(self, new_password):
        salt = bcrypt.gensalt() 
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')  

class AtualizacaoLeito(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_leito = database.Column(database.String, nullable=False)
    atualizacao = database.Column(database.String, nullable=False)
    timestamp = database.Column(database.DateTime, nullable=False, default=func.now())

    # Chave estrangeira para o id_leito na tabela de Post
    id_leito_post = database.Column(database.String, database.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"AtualizacaoLeito('{self.id_leito}', '{self.atualizacao}', '{self.timestamp}')"
    
def current_datetime():
    br_tz = timezone('America/Sao_Paulo')
    return datetime.now(br_tz)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_leito = database.Column(database.String, nullable=False)
    status_leito = database.Column(database.String, nullable=False)
    perfil_leito = database.Column(database.String, nullable=False)
    status_paciente = database.Column(database.String, nullable=False)
    nome_paciente = database.Column(database.String)
    data_nascimento = database.Column(Date)
    idade = database.Column(database.String, nullable=False)
    pontuario_ses = database.Column(database.String, nullable=False)
    data_admissao = database.Column(Date)
    hora_admissao = database.Column(Time)
    data_obito = database.Column(Date)
    hora_obito = database.Column(Time)
    data_transferencia = database.Column(Date)
    hora_transferencia = database.Column(Time)
    data_alta = database.Column(Date)
    hora_alta = database.Column(Time)
    nome_colaborador = database.Column(database.String, nullable=False)
    matricula_colaborador = database.Column(database.String, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    br_tz = timezone('America/Sao_Paulo')
    data_atualizacao = database.Column(database.DateTime, nullable=False, default=current_datetime)
    atualizacoes = database.relationship('AtualizacaoLeito', backref='leito', lazy=True)
    nome_hospital = database.Column(database.String, nullable=False)
    tipo_leito = database.Column(database.String, nullable=False)
