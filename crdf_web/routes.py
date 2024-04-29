from flask import render_template, redirect, url_for, flash, request,get_flashed_messages
from crdf_web import app, database
from unidecode import unidecode
from crdf_web.forms import FormCreateAccount, FormLogin, MyForm
from crdf_web.models import User,Post
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import bcrypt
from crdf_web import bcrypt
from datetime import datetime


hospital_beds = {
    'ANCHIETA CEILÂNDIA (SÃO FRANCISCO)': {'ADULTO': 10, 'NEONATAL': 5},
    'HOSPITAL ANA NERY': {'ADULTO': 8},
    'HOSPITAL SÃO MATEUS': {'ADULTO': 20},
    'UTI DOMED': {'ADULTO': 19},
    'HOSPITAL SANTA MARTA': {'ADULTO': 15, 'PEDIÁTRICO': 10, 'NEONATAL': 5},
    'HOSPITAL HOME': {'ADULTO': 31},
    'HOSPITAL DAHER': {'ADULTO': 40},
    'HOSPITAL MARIA AUXILIADORA': {'ADULTO': 10},
    'HOSPITAL DE BASE': {'ADULTO GERAL': 10, 'TRAUMA': 20, 'CORONARIANO': 4, 'PEDIATRICO': 17},
    'HOSPITAL SANTA MARIA': {'ADULTO-1': 18, 'ADULTO-2': 9, 'ADULTO-3': 9, 'NEONATAL': 20},
    'HOSPITAL DA CRIANÇA': {'PEDIÁTRICO- ESTRELA DO MAR': 10, 'PEDIÁTRICO- CAVALO MARINHO': 20, 'PEDIÁTRICO- PEIXE': 8},
    'HUB': {'ADULTO': 6, 'CORONARIANA': 5, 'NEONATAL': 5}
}

def make_hospital_route(hospital, bed):
    def hospital_route():
        return render_template('hospital_page.html', hospital=hospital, bed=bed)
    return hospital_route 

for hospital, bed in hospital_beds.items():
    hospital_route = make_hospital_route(hospital, bed)
    hospital_route.__name__ = f'hospital_route_{unidecode(hospital.replace(" ", "_")).lower()}'
    app.route(f'/{unidecode(hospital.replace(" ", "_")).lower()}')(hospital_route)

@app.route('/hospital/<hospital>/<tipo_leito>/<int:numero_leito>', methods=['GET'])
def atualizar_leito(hospital, tipo_leito, numero_leito):
    form = MyForm()
    # Aqui você pode adicionar a lógica para obter informações sobre o leito específico
    # Por exemplo, você pode consultar um banco de dados para obter detalhes sobre o leito com base no hospital, tipo de leito e número do leito
    # Por enquanto, vamos passar apenas essas informações para o modelo
    return render_template('atualizar_leito.html', hospital=hospital, tipo_leito=tipo_leito, numero_leito=numero_leito, form=form)

@app.route('/atualizacoes_leitos/<hospital>')
def atualizacoes_leitos_hospital(hospital):
    # Recupere os dados dos leitos para o hospital especificado do banco de dados
    dados_leitos = Post.query.filter_by(nome_hospital=hospital).all()
    return render_template('atualizacoes_leitos.html', hospital=hospital, dados_leitos=dados_leitos)

@app.route('/index.html')
@login_required
def control():
    if current_user.username == 'admcrdf':
        return render_template('index.html')
    else:
        flash('Você não tem permissão para acessar esta página', 'error')
        return redirect(url_for('home'))
    
def detalhar_leito(id_leito):
    # Aqui você recupera as informações do leito do banco de dados com base no ID do leito
    leito = Post.query.filter_by(id_leito=id_leito).first()

    if not leito:
        flash('Leito não encontrado.', 'error')
        return redirect(url_for('atualizacoes_leitos'))

    # Renderiza o template HTML com as informações do leito
    return render_template('detalhes_leito.html', leito=leito)

@app.route('/sucesso')
@login_required
def sucesso():
    return render_template('sucesso.html')

@app.route('/salvar_leito', methods=['POST'])
@login_required
def salvar_leito():
    if request.method == 'POST':
        form = request.form
    if form.validate():
        print(request.form)  # Verificar os dados enviados pelo formulário
        print(f"Hospital: {form['hospital']}, Tipo de Leito: {form['tipo_leito']}, Número do Leito: {form['numero_leito']}")
        data_nascimento = datetime.strptime(form['data_nascimento'], "%Y-%m-%d")
        data_admissao = datetime.strptime(form['data_admissao'], "%Y-%m-%d")
        data_obito = datetime.strptime(form['data_obito'], "%Y-%m-%d")
        data_transferencia = datetime.strptime(form['data_transferencia'], "%Y-%m-%d")
        data_alta = datetime.strptime(form['data_alta'], "%Y-%m-%d")
        hora_admissao = datetime.strptime(form['hora_admissao'], "%H:%M").time()
        hora_obito = datetime.strptime(form['hora_obito'], "%H:%M").time()
        hora_transferencia = datetime.strptime(form['hora_transferencia'], "%H:%M").time()
        hora_alta = datetime.strptime(form['hora_alta'], "%H:%M").time()
        novo_leito = Post(
            id_leito=form['id_leito'],
            status_leito=form['status_leito'],
            perfil_leito=form['perfil_leito'],
            status_paciente=form['status_paciente'],
            nome_paciente=form['nome_paciente'],
            data_nascimento=data_nascimento,
            idade=form['idade'],
            pontuario_ses=form['pontuario_ses'],
            data_admissao=data_admissao,
            hora_admissao=hora_admissao,
            data_obito=data_obito,
            hora_obito=hora_obito,
            data_transferencia=data_transferencia,
            hora_transferencia=hora_transferencia,
            data_alta=data_alta,
            hora_alta=hora_alta,
            nome_colaborador=form['nome_colaborador'],
            matricula_colaborador=form['matricula_colaborador'],
            author=current_user  # Assuming you have a variable current_user defined
        )
        print(novo_leito)
        database.session.add(novo_leito)
        database.session.commit()
        # flash('Leito atualizado com sucesso!', 'success')
        return redirect(url_for('hospital_route_' + unidecode(form['hospital'].replace(" ", "_")).lower()))


        # else:
        #     for field, errors in form.errors.items():
        #      for error in errors:
        #         flash(f"Erro no campo {getattr(form, field).label.text}: {error}", 'error')
        #         return redirect(request.referrer)
        #     # Redirecione para a página de confirmação ou qualquer outra página desejada
        #     return render_template('salvar_leito.html', form=form)
    else:
            flash('Erro ao salvar o leito. Por favor, tente novamente.', 'error')
            return redirect(request.referrer)  # Redireciona para a página anterior
        

@app.route('/', methods=['GET', 'POST'])
def login():
    form_login= FormLogin()
    if form_login.validate_on_submit() and 'login_button' in request.form:
        user = User.query.filter_by(username=form_login.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember_data.data)
            flash(f'Login in {form_login.username.data} successful', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('control'))
        else:
            flash(f'Log in falhou: usuário ou senha errados', 'alert-danger')
    return render_template('home.html', form_login=form_login)
            
    


@app.route('/createaccount', methods=['GET', 'POST'])
def create_account():
    form_create_account= FormCreateAccount()
    if form_create_account.validate_on_submit() and 'confirmation_button' in request.form:
        pdw_cript = bcrypt.generate_password_hash(form_create_account.password.data)
        pdw_cript = pdw_cript.decode('utf-8')
        user = User(username=form_create_account.username.data, password=pdw_cript)
        database.session.add(user)
        database.session.commit()
        flash(f'Account created for: {form_create_account.username.data}', 'alert-success')
        return redirect(url_for('login'))
    return render_template('createaccount.html',form_create_account=form_create_account)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Logout successful', 'alert-success')
    return redirect(url_for('login'))


@app.route('/pages.html')
@login_required
def pages():
    return render_template('pages.html')


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = MyForm()
#     if form.validate_on_submit():
       
#         entry1_dropdown_value = form.entry1_dropdown.data
#         entry2_dropdown_value = form.entry2_dropdown.data
#         entry1_text_value = form.entry1_text.data
#         entry2_text_value = form.entry2_text.data
#         return f'Dropdown 1: {entry1_dropdown_value}, Texto 1: {entry1_text_value}<br>Dropdown 2: {entry2_dropdown_value}, Texto 2: {entry2_text_value}'
#     return render_template('home.html', form=form)