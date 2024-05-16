from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TimeField,DateField, BooleanField, SelectField,IntegerField
from wtforms.validators import DataRequired, NumberRange, EqualTo, Length, ValidationError
from crdf_web.models import User, Post


class FormLogin(FlaskForm):
    username = StringField("Nome de usuário",validators=[DataRequired()])
    password = PasswordField("Senha:", validators=[DataRequired()])
    remember_data= BooleanField("Manter-me conectado")
    login_button = SubmitField("Entrar")

class FormChangePassword(FlaskForm):
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    change_password_button = SubmitField("Trocar Senha")

    

class MyForm(FlaskForm):
    id_leito = StringField('Id do leito', validators=[DataRequired()])
    status_leito = SelectField('Status do leito', choices=[('ocupado', 'OCUPADO'), ('vago', 'VAGO'), ('B_PP', 'BLOQUEADO - PACIENTE PARTICULAR'), ('B_MAN','BLOQUEADO - MANUTENÇÃO')], validators=[DataRequired()])
    perfil_leito = SelectField('Perfil  do leito', choices=[('hemodialise', 'HEMODIÁLISE'), ('isolamento', 'ISOLAMENTO'),('regular', 'REGULAR')], validators=[DataRequired()])
    status_paciente = SelectField('Status do paciente', choices=[('PNLE', 'PERMANCE NO LEITO'), ('ALTAA', 'ALTA ADM'), ('TPOU', 'TRANSFERIDO PARA OUTRA UNIDADE'), ('SDAL', 'SAIU DE ALTA'), ('LPST', 'EM LISTA PARA SER TRANSFERIDO'), ('OCPP', 'OCUPADO COM PACIENTE PARTICULAR'), ('vago', 'VAGO')], validators=[DataRequired()])
    nome_paciente_nsa = BooleanField('Não se aplica')
    nome_paciente = StringField('Id paciente', validators=[DataRequired()])
    data_nascimento_nsa = BooleanField('Não se aplica')
    data_nascimento = DateField('Data de nascimento', format='%d/%m/%Y', validators=[DataRequired()])
    idade = IntegerField('Idade', validators=[DataRequired(), NumberRange(min=0)])
    pontuario_ses_nsa = BooleanField('Não se aplica')
    pontuario_ses = IntegerField('Prontuário SES', validators=[DataRequired()])
    data_admissao_nsa = BooleanField('Não se aplica')
    data_admissao = DateField('Data de admissão', format='%d/%m/%Y', validators=[DataRequired()])
    hora_admissao_nsa = BooleanField('Não se aplica')
    hora_admissao = StringField('Hora da admissão', validators=[DataRequired()])
    data_obito_nsa = BooleanField('Não se aplica')
    data_obito = DateField('Data do óbito', format='%d/%m/%Y', validators=[DataRequired()])
    hora_obito_nsa = BooleanField('Não se aplica')
    hora_obito = StringField('Hora do óbito', validators=[DataRequired()])
    data_transferencia_nsa = BooleanField('Não se aplica')
    data_transferencia = DateField('Data da transferência', format='%d/%m/%Y', validators=[DataRequired()])
    hora_transferencia_nsa = BooleanField('Não se aplica')
    hora_transferencia = StringField('Hora do óbito', validators=[DataRequired()])
    data_alta_nsa = BooleanField('Não se aplica')
    data_alta = DateField('Data da alta', format='%d/%m/%Y', validators=[DataRequired()])
    hora_alta_nsa = BooleanField('Não se aplica')
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