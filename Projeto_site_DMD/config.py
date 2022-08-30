#Arquivo de configurações do programa

class app_config():
    secret_key = 'f@tec.site_DMD.Alunos'
    static_folder = 'static'
    template_folder = 'templates'

#Banco de dados
class db_config():
    #Variável que indica a plataforma padrão de configuração do banco de dados
    platform="PostgreSQL"
    #Inserir o host de hospedagem do seu banco de dados
    host="localhost"
     #Inserir o usuário de acesso ao seu banco de dados
    user="postgres"
    #Inserir a senha de acesso ao seu banco de dados:
    password="Pi3!4159"
    #Inserir o banco de dados.
    database="SAE"

Config_email = {
"MAIL_SERVER": 'smtp.gmail.com',
"MAIL_PORT": 465,
"MAIL_USE_TLS": False,
"MAIL_USE_SSL": True,
"MAIL_USERNAME": ' <INSERIR DADOS> ',
"MAIL_PASSWORD": ' <INSERIR DADOS> ',
"MAIL_DEFAULT_SENDER": ' <INSERIR DADOS> '
}
