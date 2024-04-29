from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TimeField,DateField, BooleanField, SelectField,IntegerField
from wtforms.validators import DataRequired, NumberRange, EqualTo, Length, ValidationError
from crdf_web.models import User, Post


class FormLogin(FlaskForm):
    username = StringField("Nome de usuário",validators=[DataRequired()])
    password = PasswordField("Senha:", validators=[DataRequired()])
    remember_data= BooleanField("Manter-me conectado")
    login_button = SubmitField("Entrar")



class MyForm(FlaskForm):
    id_leito = IntegerField('ID do leito', validators=[DataRequired(), NumberRange(min=0)])
    status_leito = SelectField('Status do leito', choices=[('Opção 1', 'OCUPADO'), ('opcao2', 'VAGO'), ('opcao3', 'BLOQUEADO - PACIENTE PARTICULAR'), ('opcao3','BLOQUEADO - PACIENTE PARTICULAR')], validators=[DataRequired()])
    perfil_leito = SelectField('Perfil  do leito', choices=[('opcaoA', 'HEMODIÁLISE'), ('opcaoB', 'ISOLAMENTO'),('opcaoC', 'REGULAR')], validators=[DataRequired()])
    status_paciente = SelectField('Status do paciente', choices=[('opcaoA', 'PERMANCE NO LEITO'), ('opcaoB', 'ALTA ADM'), ('opcaoC', 'TRANSFERIDO PARA OUTRA UNIDADE'), ('opcaoD', 'SAIU DE ALTA'), ('opcaoE', 'EM LISTA PARA SER TRANSFERIDO'), ('opcaoF', 'OCUPADO COM PACIENTE PARTICULAR'), ('opcaoG', 'VAGO')], validators=[DataRequired()])
    nome_paciente = StringField('Id paciente', validators=[DataRequired()])
    data_nascimento = DateField('Data de nascimento', format='%d/%m/%Y', validators=[DataRequired()])
    idade = IntegerField('Idade', validators=[DataRequired(), NumberRange(min=0)])
    pontuario_ses = IntegerField('Prontuário SES', validators=[DataRequired(), NumberRange(min=0)])
    data_admissao = DateField('Data de admissão', format='%d/%m/%Y', validators=[DataRequired()])
    hora_admissao = StringField('Hora da admissão', validators=[DataRequired()])
    data_obito = DateField('Data do óbito', format='%d/%m/%Y', validators=[DataRequired()])
    hora_obito = StringField('Hora do óbito', validators=[DataRequired()])
    data_transferencia = DateField('Data da transferência', format='%d/%m/%Y', validators=[DataRequired()])
    hora_transferencia = StringField('Hora do óbito', validators=[DataRequired()])
    data_alta = DateField('Data da alta', format='%d/%m/%Y', validators=[DataRequired()])
    hora_alta = StringField('Hora do óbito', validators=[DataRequired()])
    nome_colaborador= StringField('Nome do colaborador', validators=[DataRequired()])
    matricula_colaborador= StringField('Matrícula do colaborador', validators=[DataRequired()])
    submit = SubmitField('Enviar')


class FormCreateAccount(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6,20)])
    password_confirmation =PasswordField("Repeat your password", validators=[DataRequired(),EqualTo("password")])
    confirmation_button = SubmitField("Create account")

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Esse usuário já existe')