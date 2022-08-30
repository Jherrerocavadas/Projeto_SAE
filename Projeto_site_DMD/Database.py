from config import db_config
import psycopg2

# Classe para manipulação do banco de dados
class Banco_de_dados():
    def __init__(self):
        #Não colocar None pois senão a primeira carregada da página indica como
        #como se houvesse um usuário logado já (Não entra como anônimo).
        self.Auth_tokens = []

    #Conexão com o banco de dados
    def conectar_banco(self, platform="PostgreSQL"):

        #Para PostgreSQL
        if(platform == 'PostgreSQL'):
            comms = psycopg2.connect(
                host = db_config.host,
                user = db_config.user,
                password = db_config.password,
                database = db_config.database,
            )
            return comms

    def verificar_user(self, login):
        #melhorar essa atribuição depois
        self.comms = self.conectar_banco()
        #comms = self.comms
        cursor = self.comms.cursor()
        get_user = f"""SELECT * FROM SAE_account_data
        WHERE (Email = '{login}' or CPF = '{login}')"""
        try:
            cursor.execute(get_user)
            print('Executou')
            self.Auth_tokens = cursor.fetchone()
            # print(f'CURSOR: {cursor[1]}')
            print(f'AUTH: {self.Auth_tokens}')
            print(f'Type: {type(self.Auth_tokens)}')
            return self.Auth_tokens
        except TypeError:
            print('levantou a exceção interna')
            return None


    def inserir_user(self, User_data):

        #melhorar essa atribuição depois
        #conexão do banco de dados
        self.comms = self.conectar_banco()
        cursor = self.comms.cursor()
        #Insere os dados no PostgreSQL por meio dos comandos
        add_User = '''INSERT INTO SAE_account_data
        (Nome, Email, Senha, RG, RA, CPF, Curso, Ciclo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(add_User, User_data)
        self.comms.commit()


                #-------------------<Contas>-------------------#

    def alterar_user(self, **config_args):
        #por algum motivo aqui dá erro se o self for chamado sem os parênteses
        self.comms = self().conectar_banco()
        cursor = self.comms.cursor()
        callback_status = {'mensagem':None, 'redirecionamento':None}

        novo_email = config_args["email"]
        senha_input = config_args["senha"]
        senha = None

        Senha_hash = check_password_hash(self().verificar_user(current_user.id)[1], senha)
        if(Senha_hash):
            if(novo_email != ''):
                alterar_dados = f"""UPDATE logins
                SET Email='{novo_email}'
                Where Email='{current_user.id}' """
            elif(senha_input != ''):
                senha_nova = generate_password_hash(senha_input, method ='sha256')
                alterar_dados = f"""UPDATE logins
                SET Senha='{senha_nova}'
                Where Email='{current_user.id}' """

            #Só pra fazer um envio ao servidor ao invés de envios de cada argumento separadamente
            elif(novo_email != '' and senha_input != ''):
                alterar_dados = f"""UPDATE logins
                SET Email='{novo_email}', Senha='{senha_nova}'
                Where Email='{current_user.id}' """

            else:
                callback_status['mensagem'] ='Algum valor de alteração precisa ser inserida!'
                callback_status['redirecionamento'] = redirect(url_for('conta'))
                self.comms.close()
                return callback_status


            cursor.execute(alterar_dados)
            self.comms.commit()
            callback_status['mensagem'] ='Dados alterados com sucesso!'
        else:
            callback_status['mensagem'] ='A senha de autenticação é inválida!'

        callback_status['redirecionamento'] = redirect(url_for('conta_feature', recurso = 'change_data'))
        self.comms.close()
        return callback_status




    def deletar_user(self, **config_args):
        self.comms = self.conectar_banco(self, platform="PostgreSQL")
        cursor = self.comms.cursor()
        callback_status = {'mensagem':None, 'redirecionamento':None}

        email = 'None' #current_user.id
        senha = config_args["senha"]

        #Senha_hash = check_password_hash(self.verificar_user(email)[1], senha)
        Senha_hash = True
        if(Senha_hash):
            # deletar = f"DELETE FROM logins WHERE Email = {email}"
            # cursor.execute(deletar)
            # self.comms.close()
            print(email)
            callback_status['mensagem'] = 'Dados excluídos com sucesso!'
            callback_status['redirecionamento'] = redirect(url_for('home'))

            #Conferir isso aqui posteriormente
            callback_status['is_target_top'] = True
        else:
            callback_status['mensagem'] ='Não foi possível deletar os dados. A senha de autenticação é inválida!'
            callback_status['redirecionamento'] = redirect(url_for('conta_feature', recurso = 'delete_user'))
            callback_status['is_target_top'] = False

        self.comms.close()
        return callback_status


    #Operação para verificar todos os logins
    #NÂO UTILIZAR EM AMBIENTE DE PRODUÇÂO
    def get_all_users(self):
        self.comms = self.conectar_banco()
        cursor = self.comms.cursor()
        email_list = []
        senhas_list = []
        get_all_user = "SELECT Email FROM logins"
        cursor.execute(get_all_user)
        for(Email) in cursor:
            email_list.append(Email)
        self.comms.commit()
        return email_list


    #Operação para deletar todos os logins
    #NÂO UTILIZAR EM AMBIENTE DE PRODUÇÂO
    def deletar_dados(self):
        self.comms = self.conectar_banco()
        cursor = self.comms.cursor()
        email_list = []
        senhas_list = []
        lista_banco = {'Emails: ' : email_list, 'Senhas:' : senhas_list}
        deletar = "DELETE FROM logins"
        cursor.execute(deletar)

        get_user = "SELECT Email, Senha, id FROM logins"
        cursor.execute(get_user)
        for(Email, Senha) in cursor:
            email_list.append(Email)
            senhas_list.append(Senha)
        self.comms.commit()
        return lista_banco
