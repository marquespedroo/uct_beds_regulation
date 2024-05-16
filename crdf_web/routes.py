from flask import render_template, redirect, url_for, flash, request, jsonify,session
from crdf_web import app, database
from unidecode import unidecode
from crdf_web.forms import FormCreateAccount, FormLogin, MyForm, FormChangePassword
from crdf_web.models import User,Post,AtualizacaoLeito
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import bcrypt
from crdf_web import bcrypt
from datetime import datetime
import string
import random




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
    'HUB': {'ADULTO': 6, 'CORONARIANO': 5, 'NEONATAL': 5}
}


hospital_beds_normalized = {
    'anchieta_ceilandia_sao_francisco': {'Adulto': 10, 'Neonatal': 5},
    'hospital_ana_nery': {'Adulto': 8},
    'hospital_da_crianca': {'Pediátrico: Estrela-do-mar': 10, 'Pediátrico: Cavalo-marinho': 20, 'Pediátrico: Peixe': 8},
    'hospital_daher': {'Adulto': 40},
    'hospital_de_base': {'Adulto Geral': 10, 'Trauma': 20, 'Coronariano': 4, 'Pediátrico': 17},
    'hospital_home': {'Adulto': 31},
    'hospital_maria_auxiliadora': {'Adulto': 10},
    'hospital_santa_maria': {'Adulto-1': 18, 'Adulto-2': 9, 'Adulto-3': 9, 'Neonatal': 20},
    'hospital_santa_marta': {'Adulto': 15, 'Pediátrico': 10, 'Neonatal': 5},
    'hospital_sao_mateus': {'Adulto': 20},
    'hub': {'Adulto': 6, 'Coronariano': 5, 'Neonatal': 5},
    'uti_domed': {'Adulto': 19} 
}

# Inicia um dicionário vazio para agrupar os leitos por tipo_leito
leitos_por_tipo = {}

def make_hospital_route(hospital, bed, leitos_por_tipo,):
    def hospital_route():
        leitos_por_tipo = {}

        # Itera sobre todos os tipos de leito e seus números para o hospital atual
        for tipo_leito, num_leitos in bed.items():
            for num_leito in range(1, num_leitos + 1):
                id_leito = f"{unidecode(hospital.replace(' ', '_'))}_{unidecode(tipo_leito.replace(' ', '_'))}_{num_leito}".lower()

                # Tenta recuperar a cama do banco de dados
                leito = Post.query.filter_by(id_leito=id_leito).order_by(Post.data_atualizacao.desc()).first()

                # Se a cama não existir no banco de dados, cria um novo registro Post para ela
                if leito is None:
                    leito = Post(id_leito=id_leito, status_leito='Vago', perfil_leito='Regular', status_paciente='Vago',
                                 idade=' ', nome_colaborador='a preencher', matricula_colaborador='a preencher',
                                 pontuario_ses=' ', user_id=current_user.id, nome_hospital=hospital,
                                 tipo_leito=tipo_leito)
                    # Adiciona essa cama ao banco de dados
                    database.session.add(leito)
                    database.session.commit()

                # Adiciona o leito ao dicionário leitos_por_tipo
                if tipo_leito not in leitos_por_tipo:
                    leitos_por_tipo[tipo_leito] = []
                leitos_por_tipo[tipo_leito].append(leito)
        if current_user.username != hospital:
                flash('Você não tem permissão para acessar esta página', 'error')
                return redirect(url_for('login'))

        
        return render_template('hospital_page.html', hospital=hospital, bed=bed, leitos_por_tipo=leitos_por_tipo)

    return hospital_route

for hospital, bed in hospital_beds_normalized.items():
    hospital_route = make_hospital_route(hospital, bed,leitos_por_tipo)
    hospital_route.__name__ = f'hospital_route_{unidecode(hospital.replace(" ", "_")).lower()}'
    app.route(f'/{unidecode(hospital.replace(" ", "_")).lower()}')(hospital_route)

@app.route('/hospital/<hospital>/<tipo_leito>/<int:numero_leito>', methods=['GET'])
@login_required
def atualizar_leito(hospital, tipo_leito, numero_leito):
    form = MyForm()
    id_leito = f"{unidecode(hospital.replace(' ', '_'))}_{unidecode(tipo_leito.replace(' ', '_'))}_{numero_leito}".lower()
    if current_user.username != hospital:
        flash('Você não tem permissão para acessar esta página', 'error')
        return redirect(url_for('login'))
    return render_template('atualizar_leito.html', id_leito=id_leito, hospital=hospital, tipo_leito=tipo_leito, numero_leito=numero_leito, form=form)



@app.route('/atualizacoes_leitos/<hospital>', methods=['GET'])
@login_required
def atualizacoes_leitos_hospital(hospital):
    if current_user.username != 'admcrdf':
        flash('Você não tem permissão para acessar esta página', 'error')
        return redirect(url_for('login'))

    global leitos_por_tipo
    # Inicia um dicionário vazio para agrupar os leitos por tipo_leito
    leitos_por_tipo = {}

    # Verifica se o nome do hospital está no dicionário normalizado
    if hospital in hospital_beds_normalized:
        # Itera sobre todos os tipos de leito e seus números para o hospital atual
        for tipo_leito, num_leitos in hospital_beds_normalized[hospital].items():
            for num_leito in range(1, num_leitos + 1):
                id_leito = f"{unidecode(hospital.replace(' ', '_'))}_{unidecode(tipo_leito.replace(' ', '_'))}_{num_leito}".lower()

                # Tenta recuperar a cama do banco de dados
                leito = Post.query.filter_by(id_leito=id_leito).order_by(Post.data_atualizacao.desc()).first()

                # Se a cama não existir no banco de dados, cria um novo registro Post para ela
                if leito is None:
                    leito = Post(id_leito=id_leito, status_leito='Vago', perfil_leito='Regular', status_paciente='Vago',
                                 idade=' ', nome_colaborador='a preencher', matricula_colaborador='a preencher',
                                 pontuario_ses=' ', user_id=current_user.id, nome_hospital=hospital,
                                 tipo_leito=tipo_leito)
                    # Adiciona essa cama ao banco de dados
                    database.session.add(leito)
                    database.session.commit()
                atualizacoes_leito = AtualizacaoLeito.query.filter_by(id_leito_post=leito.id_leito).order_by(AtualizacaoLeito.timestamp.desc()).first()

                # Verifica se o tipo de leito já está no dicionário
                if tipo_leito not in leitos_por_tipo:
                    # Se não estiver, cria uma nova lista para esse tipo de leito
                    leitos_por_tipo[tipo_leito] = []

                # Adiciona o leito à lista correspondente ao tipo de leito
                leitos_por_tipo[tipo_leito].append((leito, atualizacoes_leito))

    # Renderiza o template HTML com os leitos agrupados por tipo_leito
    return render_template('atualizacoes_leitos.html', hospital=hospital, bed=hospital_beds_normalized[hospital],
                           leitos_por_tipo=leitos_por_tipo)



@app.route('/leito/<id_leito>', methods=['GET'])
@login_required
def detalhes_leito(id_leito):
    if current_user.username != 'admcrdf':
        flash('Você não tem permissão para acessar esta página', 'error')
        return redirect(url_for('login'))
    # Verifique primeiro se o leito já existe no banco de dados
    leito = Post.query.filter_by(id_leito=id_leito).order_by(Post.data_atualizacao.desc()).first()
    atualizacoes_leito = Post.query.filter_by(id_leito=id_leito).order_by(Post.data_atualizacao.desc()).all()

    # Se o leito não existe, crie-o e salve-o no banco de dados
    if not leito:
        leito = Post(id_leito=id_leito)
        database.session.add(leito)
        database.session.commit()
    
    # Renderiza o template HTML com as informações do leito
    return render_template('detalhes_leito.html', leito=leito, atualizacoes_leito=atualizacoes_leito)


@app.route('/index.html')
@login_required
def control():
    if current_user.username == 'admcrdf':
        taxas_ocupacao = taxa_ocupacao_global()  # Supondo que este é o nome da sua função que calcula a taxa de ocupação
        return render_template('index.html', taxas_ocupacao=taxas_ocupacao)
    else:
        flash('Você não tem permissão para acessar esta página', 'error')
        return redirect(url_for('login'))
    
def detalhar_leito(id_leito):
    # Aqui você recupera as informações do leito do banco de dados com base no ID do leito
    leito = Post.query.filter_by(id_leito=id_leito).first()

    if not leito:
        flash('Leito não encontrado.', 'error')
        return redirect(url_for('atualizacoes_leitos'))

    # Renderiza o template HTML com as informações do leito
    return render_template('detalhes_leito.html', leito=leito)


@app.route('/salvar_leito', methods=['POST'])
@login_required
def salvar_leito():
    if request.method == 'POST':
        form = request.form
        tipo_leito = form['tipo_leito']
        hospital = form['hospital']
        data_nascimento = datetime.strptime(form['data_nascimento'], "%Y-%m-%d") if form['data_nascimento'] else None
        if 'data_nascimento_nsa' in form:
            data_nascimento = None
        
        data_admissao = datetime.strptime(form['data_admissao'], "%Y-%m-%d") if form['data_admissao'] else None
        if 'data_admissao_nsa' in form:
            data_admissao = None
        
        data_obito = datetime.strptime(form['data_obito'], "%Y-%m-%d") if form['data_obito'] else None
        if 'data_obito_nsa' in form:
            data_obito = None
        
        data_transferencia = datetime.strptime(form['data_transferencia'], "%Y-%m-%d") if form['data_transferencia'] else None
        if 'data_transferencia_nsa' in form:
            data_transferencia = None
        
        data_alta = datetime.strptime(form['data_alta'], "%Y-%m-%d") if form['data_alta'] else None
        if 'data_alta_nsa' in form:
            data_alta = None
        
        hora_admissao = datetime.strptime(form['hora_admissao'], "%H:%M").time() if form['hora_admissao'] else None
        if 'hora_admissao_nsa' in form:
            hora_admissao = None
        
        hora_obito = datetime.strptime(form['hora_obito'], "%H:%M").time() if form['hora_obito'] else None
        if 'hora_obito_nsa' in form:
            hora_obito = None
        
        hora_transferencia = datetime.strptime(form['hora_transferencia'], "%H:%M").time() if form['hora_transferencia'] else None
        if 'hora_transferencia_nsa' in form:
            hora_transferencia = None
        
        hora_alta = datetime.strptime(form['hora_alta'], "%H:%M").time() if form['hora_alta'] else None
        if 'hora_alta_nsa' in form:
            hora_alta = None
        print(request.form)
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
            user_id=current_user.id,
            nome_hospital=hospital,
            tipo_leito=tipo_leito
        )
        print(novo_leito)
        database.session.add(novo_leito)
        database.session.commit()
        app.logger.info("Novo leito adicionado com sucesso.")
        flash('Leito atualizado com sucesso!', 'sucesss')
        return redirect(url_for(f'hospital_route_{unidecode(hospital.replace(" ", "_")).lower()}'))




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
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'login_button' in request.form:
        user = User.query.filter_by(username=form_login.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember_data.data)
            flash(f'Login in {form_login.username.data} successful', 'alert-success')
            if user.username == 'admcrdf':
                return redirect('index.html') # redirecionar para index.html se o usuário for 'admcrdf'
            else:    
                hospital_route = f'/{unidecode(form_login.username.data.replace(" ", "_")).lower()}'
                return redirect(f'{hospital_route}?next={hospital_route}')
        else:
            flash(f'Log in falhou: usuário ou senha errados', 'alert-danger')
    return render_template('home.html', form_login=form_login)
            
    



@app.route('/createaccount', methods=['GET', 'POST'])
@login_required
def create_account():
    if current_user.username != 'admcrdf':
        flash('Você não tem permissão para acessar esta página', 'error')
        return redirect(url_for('login'))
    form_create_account = FormCreateAccount()
    form_change_password = FormChangePassword()  # Adicionando o formulário FormChangePassword


    if form_create_account.validate_on_submit() and 'confirmation_button' in request.form:
        pdw_cript = bcrypt.generate_password_hash(form_create_account.password.data)
        pdw_cript = pdw_cript.decode('utf-8')
        user = User(username=form_create_account.username.data, password=pdw_cript)
        database.session.add(user)
        database.session.commit()
        flash(f'Account created for: {form_create_account.username.data}', 'alert-success')
    
    return render_template('createaccount.html', form_create_account=form_create_account, form_change_password=form_change_password)  # Passando ambos os formulários para o contexto do template

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    
    if current_user.username != 'admcrdf':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('index'))
    
    form_change_password = FormChangePassword()
    if form_change_password.validate_on_submit():
        username = form_change_password.username.data
        user = User.query.filter_by(username=username).first()
        if user:
            new_password = generate_password()  # Função para gerar uma nova senha aleatória
            user.set_password(new_password)
            database.session.commit()
            flash(f'A senha do usuário {username} foi alterada para: {new_password}', 'success')
        else:
            flash('Usuário não encontrado.', 'danger')
    return redirect(url_for('create_account'))  # Redirecionando de volta para a página de criação de conta


def generate_password(length=6):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(alphabet) for _ in range(length))
    return password


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Logout successful', 'alert-success')
    return redirect(url_for('login'))




@app.route('/atualizacoes_leitos.html')
@login_required
def atualizacoes_leitos():
    if current_user.username != 'admcrdf':
        flash('Você não tem permissão para acessar esta página', 'error')
        return redirect(url_for('login'))
    return render_template('atualizacoes_leitos.html')

def taxa_ocupacao_global():
    # Recupere todos os leitos
    leitos = Post.query.all()

    # Contadores de status
    total_leitos = len(leitos)
    status_ocupado = 0
    status_vago = 0
    status_bloq_paciente_particular = 0
    status_bloq_manutencao = 0

    # Iterar sobre os leitos para contar os status
    for leito in leitos:
        if leito.status_leito == 'Ocupado':
            status_ocupado += 1
        elif leito.status_leito == 'Vago':
            status_vago += 1
        elif leito.status_leito == 'Bloq: paciente particular':
            status_bloq_paciente_particular += 1
        elif leito.status_leito == 'Bloq: manutenção':
            status_bloq_manutencao += 1

    # Cálculo da taxa de ocupação
    taxa_vago = (status_vago / total_leitos) * 100
    taxa_ocupado = (status_ocupado / total_leitos) * 100
    taxa_bloq_paciente_particular = (status_bloq_paciente_particular / total_leitos) * 100
    taxa_bloq_manutencao = (status_bloq_manutencao / total_leitos) * 100

    # Organize os dados de acordo com a ordem desejada
    taxas = {
        "Vago": taxa_vago,
        "Ocupado": taxa_ocupado,
        "Bloq: paciente particular": taxa_bloq_paciente_particular,
        "Bloq: manutenção": taxa_bloq_manutencao
    }

    return taxas

@app.route('/api/v1/taxa_ocupacao')
def api_taxa_ocupacao():
    # Chame a função para calcular as taxas de ocupação global
    taxas_ocupacao = taxa_ocupacao_global()
    # Retorne os dados de taxa de ocupação em formato JSON
    return jsonify(taxas_ocupacao)

def taxa_ocupacao_por_hospital(hospital_name):
    hospital_bed = hospital_beds_normalized[hospital_name]
    
    total_leitos = sum(hospital_bed.values())
    status_ocupado = 0
    status_vago = 0
    status_bloq_paciente_particular = 0
    status_bloq_manutencao = 0

    # Iterar sobre os leitos do hospital atual
    for tipo_leito, num_leitos in hospital_bed.items():
        for num_leito in range(1, num_leitos + 1):
            id_leito = f"{unidecode(hospital_name.replace(' ', '_'))}_{unidecode(tipo_leito.replace(' ', '_'))}_{num_leito}".lower()
            leito = Post.query.filter_by(id_leito=id_leito).order_by(Post.data_atualizacao.desc()).first()

            if leito is not None:
                if leito.status_leito == 'Ocupado':
                    status_ocupado += 1
                elif leito.status_leito == 'Vago':
                    status_vago += 1
                elif leito.status_leito == 'Bloq:Paciente particular':
                    status_bloq_paciente_particular += 1
                elif leito.status_leito == 'Bloq:manuten':
                    status_bloq_manutencao += 1

    # Calcular as taxas de ocupação para o hospital atual
    taxa_vago = (status_vago / total_leitos) * 100 if total_leitos > 0 else 0
    taxa_ocupado = (status_ocupado / total_leitos) * 100 if total_leitos > 0 else 0
    taxa_bloq_paciente_particular = (status_bloq_paciente_particular / total_leitos) * 100 if total_leitos > 0 else 0
    taxa_bloq_manutencao = (status_bloq_manutencao / total_leitos) * 100 if total_leitos > 0 else 0

    taxa_por_hospital = {
        "Vago": taxa_vago,
        "Ocupado": taxa_ocupado,
        "Bloq: paciente particular": taxa_bloq_paciente_particular,
        "Bloq: manutenção": taxa_bloq_manutencao
    }

    return taxa_por_hospital


@app.route('/taxa_ocupacao_por_hospital/<hospital_name>')
@login_required
def show_taxa_ocupacao_por_hospital(hospital_name):
    return render_template('hospital_page.html')

@app.route('/api/taxa_ocupacao_por_hospital/<hospital_name>', methods=['GET'])
@login_required
def api_taxa_ocupacao_por_hospital(hospital_name):
    taxas_ocupacao = taxa_ocupacao_por_hospital(hospital_name)
    return jsonify(taxas_ocupacao)



def contagem_leitos_pediatricos(hospital_beds_normalized):
    contagem_pediatricos = {'Vago': 0, 'Ocupado': 0, 'Bloq: paciente particular': 0, 'Bloq: manutenção': 0}
    for hospital, leitos in hospital_beds_normalized.items():
        for tipo_leito, num_leitos in leitos.items():
            if 'Pediátrico' in tipo_leito:
                for num_leito in range(1, num_leitos + 1):
                    id_leito = f"{unidecode(hospital.replace(' ', '_'))}_{unidecode(tipo_leito.replace(' ', '_'))}_{num_leito}".lower()
                    leito = Post.query.filter_by(id_leito=id_leito).order_by(Post.data_atualizacao.desc()).first()
                    if leito:
                        status = leito.status_leito
                        if status in contagem_pediatricos:
                            contagem_pediatricos[status] += 1


    return contagem_pediatricos


def contagem_leitos_por_status(hospital_beds_normalized):
    contagens = {
        'Adulto': {'Vago': 0, 'Ocupado': 0, 'Bloq: paciente particular': 0, 'Bloq: manutenção': 0},
        'Pediátrico': contagem_leitos_pediatricos(hospital_beds_normalized),
        'Neonatal': {'Vago': 0, 'Ocupado': 0, 'Bloq: paciente particular': 0, 'Bloq: manutenção': 0},
        'Coronariano': {'Vago': 0, 'Ocupado': 0, 'Bloq: paciente particular': 0, 'Bloq: manutenção': 0},
        'Trauma': {'Vago': 0, 'Ocupado': 0, 'Bloq: paciente particular': 0, 'Bloq: manutenção': 0},
    }

    for hospital, leitos in hospital_beds_normalized.items():
        for grupo, num_leitos in leitos.items():
            for num_leito in range(1, num_leitos + 1):
                id_leito = f"{hospital}_{grupo}_{num_leito}".lower().replace(' ', '_')
                leito = Post.query.filter_by(id_leito=id_leito).order_by(Post.data_atualizacao.desc()).first()

                if leito:
                    status = leito.status_leito

                    if 'Adulto' in grupo:
                        if status in contagens['Adulto']:
                            contagens['Adulto'][status] += 1
                    elif grupo in contagens:  # Verificar se o grupo ainda existe em contagens - Neonatal, Coronariano, Trauma
                        if status in contagens[grupo]:
                            contagens[grupo][status] += 1

    return contagens



@app.route('/api/v1/contagem_leitos', methods=['GET'])
@login_required
def api_contagem_leitos():
    contagens = contagem_leitos_por_status(hospital_beds_normalized)
    return jsonify(contagens)



def ocupacao_por_hospital_numeros(hospital_name):
    hospital_bed = hospital_beds_normalized[hospital_name]
    tipos_leitos = {}  # Dicionário para armazenar a ocupação por tipo de leito
    
    # Iterar sobre os leitos do hospital atual
    for tipo_leito, num_leitos in hospital_bed.items():
        status_leitos = {}  # Dicionário para armazenar a ocupação por status de leito para este tipo de leito
        
        # Inicializar contadores para cada status de leito
        for status in ['Vago', 'Ocupado', 'Bloq:Paciente particular', 'Bloq:manuten']:
            status_leitos[status] = 0

        # Iterar sobre os leitos deste tipo de leito
        for num_leito in range(1, num_leitos + 1):
            id_leito = f"{unidecode(hospital_name.replace(' ', '_'))}_{unidecode(tipo_leito.replace(' ', '_'))}_{num_leito}".lower()
            leito = Post.query.filter_by(id_leito=id_leito).order_by(Post.data_atualizacao.desc()).first()

            if leito is not None:
                # Incrementar o contador para o status do leito atual
                status_leitos[leito.status_leito] += 1
        
        # Adicionar os contadores de status deste tipo de leito ao dicionário de tipos de leitos
        tipos_leitos[tipo_leito] = status_leitos

    return tipos_leitos

@app.route('/ocupacao_por_hospital_numeros/<hospital_name>')
@login_required
def show_ocupacao_por_hospital_numeros(hospital_name):
    return render_template('hospital_page.html')


@app.route('/api/ocupacao_por_hospital_numeros/<hospital_name>', methods=['GET'])
@login_required
def api_ocupacao_por_hospital_numeros(hospital_name):
    ocupacao_tipos_leitos = ocupacao_por_hospital_numeros(hospital_name)
    return jsonify(ocupacao_tipos_leitos)





@app.route('/api/v1/buscar_ultimas_atualizacoes_por_hospital')
@login_required
def buscar_ultimas_atualizacoes_por_hospital():
    with app.app_context():
        limite = 7
        ultimas_atualizacoes = Post.query.order_by(Post.data_atualizacao.desc()).limit(limite).all()
        
        # Converter os objetos Post em um formato serializável
        ultimas_atualizacoes_serializadas = []
        for post in ultimas_atualizacoes:
            post_serializado = {
                'data_atualizacao': post.data_atualizacao.strftime('%Y-%m-%d %H:%M:%S'),  # Data e hora
                'hospital': post.nome_hospital
            }
            ultimas_atualizacoes_serializadas.append(post_serializado)
        
        return jsonify(ultimas_atualizacoes_serializadas)
    

@app.route('/atualizacoes', methods=['GET'])
@login_required
def atualizacoes():
    if current_user.username != 'admcrdf':
        flash('Você não tem permissão para acessar esta página', 'error')
        return redirect(url_for('login'))
    with app.app_context():
        limite = 150
        atualizacoes_leitos = Post.query.order_by(Post.data_atualizacao.desc()).limit(limite).all()

    # Renderiza o template HTML com as informações de todas as atualizações de leitos
    return render_template('atualizacoes.html', atualizacoes_leitos=atualizacoes_leitos)




def leitos_vagos_por_hospital():
    hospitais_com_leitos_vagos = {}  # Dicionário para armazenar os hospitais com leitos vagos e a contagem por tipo de leito
    
    # Iterar sobre todos os hospitais
    for hospital_name, hospital_bed in hospital_beds_normalized.items():
        leitos_vagos = {}  # Dicionário para armazenar a contagem de leitos vagos por tipo de leito para este hospital
        
        # Iterar sobre os leitos do hospital atual
        for tipo_leito, num_leitos in hospital_bed.items():
            leitos_vagos[tipo_leito] = 0  # Inicializar contador de leitos vagos para este tipo de leito
            
            # Iterar sobre os leitos deste tipo de leito
            for num_leito in range(1, num_leitos + 1):
                id_leito = f"{unidecode(hospital_name.replace(' ', '_'))}_{unidecode(tipo_leito.replace(' ', '_'))}_{num_leito}".lower()
                leito = Post.query.filter_by(id_leito=id_leito).order_by(Post.data_atualizacao.desc()).first()
    
                if leito is None or leito.status_leito == 'Vago':
                    # Se o leito não for encontrado ou estiver vago, incrementar o contador de leitos vagos
                    leitos_vagos[tipo_leito] += 1
        
        # Verificar se o hospital tem leitos vagos e adicionar ao resultado
        if any(leitos_vagos.values()):
            hospitais_com_leitos_vagos[hospital_name] = leitos_vagos

    return hospitais_com_leitos_vagos

@app.route('/leitos_vagos_por_hospital', methods=['GET'])
@login_required
def api_leitos_vagos_por_hospital():
    hospitais_com_leitos_vagos = leitos_vagos_por_hospital()
    return jsonify(hospitais_com_leitos_vagos)



