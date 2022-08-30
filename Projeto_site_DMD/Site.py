#-------------------------------<Configurações>--------------------------------#

# Core do aplicativo
from flask import Flask, request, redirect, url_for, render_template#, flash, abort

#Sistema de login e autenticação - Expansão flask
from flask_login import (LoginManager, UserMixin, login_user, logout_user,
current_user, login_required)

#Criptografia de senha
from werkzeug.security import generate_password_hash, check_password_hash

#Geração de código para validação de email
from random import seed, randint

#Sistema de envio de emails - Expansão flask
from flask_mail import Mail, Message

#Comunicação com o banco de dados PostgreSQL
import psycopg2

#arquivo de configuração de variáveis de ambiente e outros dados usados no programa
from config import app_config, Config_email
from Database import Banco_de_dados
import json
#Para tratamento de erros e exceções

# Ver de importar apenas exceções específicas
import werkzeug.exceptions
import jinja2.exceptions


#Importação de variáveis de ambiente e outras configurações, caso necessário
# OPTIMIZE:
is_validation = None
verify_code = ''
User_data = None
status_code = 404 #Código de teste padrão

#Criação de uma instância do Flask
app = Flask(__name__,
static_folder=app_config.static_folder,
template_folder=app_config.template_folder)

#Inicialização e configuração das extensões flask
app.secret_key = app_config.secret_key
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.__init__(app)
app.config.update(Config_email)
mail = Mail(app)
db = Banco_de_dados() # Inicialização da classe de banco de dados


# Classe usada pelo Flask Login
class User(UserMixin):
    pass



#decoradores de user_loader e request_loader, usados pelo flask_login
@login_manager.user_loader
def load_user(email):
    if(db.Auth_tokens != None):
        if email not in db.Auth_tokens:
            return
    User_token = User()
    User_token.id = email
    return User_token


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if(db.Auth_tokens != None):
        if email not in db.Auth_tokens:
            return
    User_token = User()
    User_token.id = email
    return User_token

#--------------------------------<Autenticação>--------------------------------#

#Função da página de cadastro
@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    # return 'Página não implementada ainda'
    # ver um modo mais eficiente de persistir o status da página e o código da
    # validação para a próxima etapa
    #talvez com arquivo json??
    # global is_validation
    # global verify_code
    # global User_data
    #
    # #Recupera os dados do input html
    if(request.method == 'POST'):
    #     if(is_validation == None):

            Nome = request.form['Nome']
            Email = request.form['Email']
            Senha = generate_password_hash(request.form['Senha'], method ='sha256')
            Senha_sem_hash = request.form['Senha']
            RG = request.form['RG']
            RA = request.form['RA']
            CPF = request.form['CPF']
            Curso = request.form['Curso']
            Ciclo = request.form['Ciclo']
            #email = request.form['Email']
            print(f'Nome: {Nome}')
            print(f'Email: {Email}')
            print(f'Senha: {Senha}')
            print(f'RG: {RG}')
            print(f'RA: {RA}')
            print(f'CPF: {CPF}')
            print(f'Curso: {Curso}')
            print(f'Ciclo: {Ciclo}')
            User_data = (Nome, Email, Senha, RG, RA, CPF, Curso, Ciclo)
            db.inserir_user(User_data)
            return User_data

    #         email_exists = db.verificar_user(email)
    #         if(not email_exists):
    #             for i in range(4):
    #                 verify_code+=str(randint(0, 9))
    #             # print(f'Código: {verify_code}')#DEBUG
    #
    #             msg = Message(
    #             subject= 'Verificação de email - Gamesplace',
    #             recipients=[email, "emailverify.gamesplace@gmail.com"],
    #             html= render_template('landing_pages/html/corpo_email.html', verify_code=verify_code)
    #             )
    #             mail.send(msg)
    #
    #
    #             User_data = (email, Senha)
    #
    #             is_validation = 'email_verify'
    #             return render_template('landing_pages/html/email_verify.html')
    #         else:
    #             flash('Usuário já existe! Tente outro email')
    #             return redirect(url_for('cadastro'))
    #             #return redirect(url_for('error', error='Usuário já existe! Tente outro email'))
    #
    #     elif(is_validation == 'email_verify'):
    #         try:
    #             email_code = request.form['email_code']
    #             if(request.form['verify_code'] == 'verify_code'):
    #                 print(f'is_validation2: {is_validation}')
    #                 if(email_code == verify_code):
    #                     try:
                            # db.inserir_user(User_data)
    #                         # print('inserido!')#DEBUG
    #
    #                         #inserir o valor perfil no HTML (será mostrado o usuário no canto)
    #                         flash('Cadastro concluído!')
    #                         return redirect(url_for('home'))
    #
    #                     except psycopg2.errors.UniqueViolation:
    #                         flash('Usuário já existe! Tente outro email')
    #                         return redirect(url_for('cadastro'))
    #
    #                     finally:
    #                         #encerra a comunicação com o banco de dados independente do resultado
    #
    #                         print(f'is_validation3: {is_validation}')
    #                         db.comms.close()
    #                         verify_code = ''
    #                         is_validation = None
    #
    #                 else:
    #                     print('Código inválido')
    #
    #                     flash('Código inválido!')
    #                     return redirect(url_for('cadastro'))
    #
    #                     #popup flash nessa página
    #                     flash('Código de validação inválido')
    #                     return redirect(url_for('cadastro'))
    #         except werkzeug.exceptions.BadRequestKeyError:
    #             flash('Página recarregada!')
    #             return redirect(url_for('cadastro'))
    #
    #
    #     else:
    #         return render_template('landing_pages/html/page_error.html', status_code='002',
    #         complete_status= f'002 - Erro na etapa de cadastro')
    else:
        # is_validation = None
    #     verify_code = ''
    #     User_data = None
        return render_template('cadastro.html')



#Ler dados de usuário no banco de dados
@app.route('/login', methods = ['GET', 'POST'])
def login():
    # return 'Página não implementada ainda'
    # #lembra_user = False
    if(request.method == 'POST'):
        Login = request.form['login_field']
        Senha = request.form['password_field']

        print(f'Login: {Login}')
        print(f'Senha: {Senha}')
        User_data = ('id','Nome', 'Email', 'Senha', 'RG', 'RA', 'CPF', 'Curso', 'Ciclo')
        Auth_tokens = db.verificar_user(Login)

        return dict(zip(User_data, Auth_tokens))
    #
    #     try:
    #         #se os valores existirem, são retornados
    #         if(Auth_tokens != None):
    #             Senha_hash = check_password_hash(Auth_tokens[1], Senha)
    #
    #             if(Senha_hash == True):
    #                 User_token = User()
    #                 User_token.id = email
    #                 login_user(User_token)#, remember=lembra_user)
    #
    #                 flash('Login concluído!')
    #                 #popup flash nessa página
    #                 return redirect(url_for('home'))
    #
    #             else:
    #                 flash('Senha incorreta!')
    #                 #popup flash nessa página
    #                 return redirect(url_for('login'))
    #
    #         #se Auth_tokens == []
    #         else:
    #
    #         #enviar um popup
    #             flash('Usuário não encontrado!')
    #             #popup flash nessa página
    #             return redirect(url_for('login'))
    #     except TypeError:
    #             #enviar um popup
    #                 flash('Usuário não encontrado!')
    #                 #popup flash nessa página
    #                 return redirect(url_for('login'))
    #
    #     #encerra a comunicação com o banco de dados independente do resultado
    #     finally:
    #         db.comms.close()
    #
    else:
        return render_template('login.html')

@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    db.Auth_tokens = []
    #enviar um popup
    flash('Conta desconectada com sucesso!')
    #popup flash nessa página
    return redirect(url_for('home'))

@login_manager.unauthorized_handler
def not_logged():
    flash('Você precisa estar logado para acessar essa página!')
    return redirect(url_for('home'))


#-----------------------------------<Erros>------------------------------------#

def alter_code(e):
    global status_code
    status_code = e.code
    return page_error(e)

@app.errorhandler(status_code)
def page_error(e):
    try:
        return render_template('page_error.html', status_code=e.code,
        complete_status= f'{e.code} - {e.name}'),status_code
        # return f'{e.code} - {e.name}'
    except:
        return f'??? - Erro desconhecido'
        # return render_template('landing_pages/html/page_error.html', status_code='???',
        # complete_status= f'??? - Erro desconhecido')

#Alguns status de erro a serem exibidos na página de erro
#Erros de cliente
app.register_error_handler(400, alter_code)
app.register_error_handler(401, alter_code)
app.register_error_handler(403, alter_code)
app.register_error_handler(404, alter_code)
app.register_error_handler(405, alter_code)
app.register_error_handler(406, alter_code)
app.register_error_handler(410, alter_code)

#Erros de servidor
app.register_error_handler(500, alter_code)
app.register_error_handler(501, alter_code)
app.register_error_handler(502, alter_code)
app.register_error_handler(503, alter_code)
app.register_error_handler(504, alter_code)
app.register_error_handler(505, alter_code)

#------------------------------------<Home>------------------------------------#
@app.route('/', methods = ['GET', 'POST'])
def home():
    # Exibir os botões de redirecionamento para as outras guias, ou informações
    # relevantes como tarefas com vencimento próximo, provas com data próxima,
    # atividades extracurriculares, etc.
    #Testes
    print(db.Auth_tokens)
    print(f'current_user: {current_user}')
    try:
        print(f'Id: {current_user.id}')
    except AttributeError:
        pass
    print(f'Ativo?: {current_user.is_active}')
    print(f'Autenticado?: {current_user.is_authenticated}')
    print(f'Anônimo?: {current_user.is_anonymous}')

    return render_template('home.html', curso= 'Design de Mídias Digitais')
    # return 'Página não implementada ainda'

#-----------------------------------<Aulas>------------------------------------#

@app.route('/horario_curso/<path:curso>', methods = ['GET', 'POST'])
def horario_curso(curso):
    #Exibir a grade horária do curso do aluno.
    # if(request.method == 'POST'):
    #     curso = request.form[]
    with open('static\cursos_disciplinas.json', 'r', encoding = 'utf-8') as disciplinas:
        cursos_disciplinas = json.load(disciplinas)
        print(cursos_disciplinas)
    if(current_user.is_anonymous):
        return render_template('disciplinas.html', curso = curso, cursos_disciplinas=cursos_disciplinas)
    return render_template('disciplinas.html', curso = 'Design de Mídias Digitais', cursos_disciplinas=cursos_disciplinas)

@app.route('/horario_curso', methods = ['GET', 'POST'])
def horario_curso_anon():
    #Exibir a grade horária do curso do aluno.
    with open('static\cursos_disciplinas.json', 'r', encoding = 'utf-8') as disciplinas:
        cursos = json.load(disciplinas).keys()
        print(cursos)
    if(current_user.is_anonymous):
        return render_template('cursos.html', cursos = cursos)


#Horários de Aula
@app.route('/horario_grade', methods = ['GET', 'POST'])
#Exibir a grade horária do aluno, e as matérias que está matriculada
def horario_grade():
    with open('static\horarios.json', 'r', encoding = 'utf-8') as horarios_aula:
        horarios = json.load(horarios_aula)
        print(cursos)
    return render_template('horario_grade.html', horarios=horarios['horarios_matutino'])
    return 'Página não implementada ainda'

#Verificação de professores na matéria
@app.route('/professores', methods = ['GET', 'POST'])
#Verificar o status dos professores das matérias (licença, online, sem professor, etc)
def professores():
    # return render_template('landing_pages/html/home.html', sugestions=sugestions)
    return 'Página não implementada ainda'

#Sugestões de matéria para matrículas
@app.route('/materia_suggest', methods = ['GET', 'POST'])
#Sugerir atribuições de matérias na matrícula
def materia_suggest():
    # return render_template('landing_pages/html/home.html', sugestions=sugestions)
    return 'Página não implementada ainda'

#Sugestões de matéria para matrículas
@app.route('/cursos', methods = ['GET', 'POST'])
#Sugerir atribuições de matérias na matrícula
def cursos():
    with open('static\cursos_disciplinas.json', 'r', encoding = 'utf-8') as disciplinas:
        cursos = json.load(disciplinas).keys()
        # print(cursos)
    return render_template('cursos.html', cursos=cursos, curso= 'Design de Mídias Digitais')
    # return 'Página não implementada ainda'
#---------------------------------<Atividades>---------------------------------#
#Atividades
@app.route('/atividades', methods = ['GET', 'POST'])
# Exibir as atividades de cada professor
def atividades():

    return 'Página não implementada ainda'

#---------------------------------<Documentos>---------------------------------#
#Atividades
@app.route('/documentos', methods = ['GET', 'POST'])
# Carteirinha de estudante, passe de transporte, etc.
def documentos():

    return 'Página não implementada ainda'
#-------------------------------<Estágios e TG>--------------------------------#

#Estágios -> Falar com as meninas de Gestão de projetos
@app.route('/estagios', methods = ['GET', 'POST'])
def estagios():
    #Exibir sugestões de estágios

    # return render_template('landing_pages/html/forum.html', sugestions=sugestions, threads=threads)
    return 'Página não implementada ainda'
# TG
@app.route('/tg', methods =['GET','POST'])
def tg():
    #Exibir dados relevantes ao TG (Cronograma, upload de arquivos, etc)

    return 'Página não implementada ainda'

#---------------------------------<Professores>--------------------------------#
#Publicação de atividades, provas, link de material didático, etc.
#Exibição das faltas





#------------------------------------<Conta>-----------------------------------#

# Sua conta
@app.route('/conta', methods = ['POST', 'GET'])
# @login_required
def sua_conta():
    #Editar dados da sua conta
    if (request.method == 'POST'):
        pass


    # return render_template(f'landing_pages/html/conta.html')
    return 'Página não implementada ainda'

#
@app.route('/conta/<string:recurso>', methods = ['POST', 'GET'])
# @login_required
def conta_feature(recurso):

    return 'Página não implementada ainda'



#------------------------------<Testes e devtools>-----------------------------#

#Operação para deletar todos os logins
#NÂO UTILIZAR EM AMBIENTE DE PRODUÇÂO
#Descomentar a linha abaixo para habilitar a rota de delete(/delete)
# @app.route('/delete', methods = ['POST', 'GET'])
def delete():
    lista_db = db.deletar_dados()
    return render_template('landing_pages/html/page_error.html', status_code='000',
    complete_status= lista_db)

# @app.route('/view_signatures', methods = ['POST', 'GET'])
def view_signatures():
    lista_db = db.get_all_users()
    return render_template('landing_pages/html/page_error.html', status_code='001',
    complete_status= lista_db)



#fins de teste

#Descomentar a linha abaixo para habilitar a rota de testes(/teste)
# @app.route('/teste', methods = ['POST', 'GET'])
# @login_required #Para fazer teste com página protegida, descomente essa também
# @app.route('/solicitar_post_apenas', methods = ['POST'])
def teste():

        #Teste para envio de emails

    # msg = Message(
    # subject= 'Verificação de email - Gamesplace (Teste2)',
    # recipients=[],
    # html= render_template('landing_pages/html/corpo_email.html', verify_code='1111')
    # )
    # mail.send(msg)
    # return render_template('landing_pages/html/page_error.html', status_code='???',
    # complete_status= f'??? - Só solicitações post')
    # return render_template('landing_pages/html/corpo_email.html', verify_code= '1234')
    return 'Página não implementada ainda'

#Processo para que todo o backend e estrutura do site sejam executados ao
#rodar esse arquivo python

if (__name__ == '__main__'):
    app.run(debug= True, host = "0.0.0.0")
