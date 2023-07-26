import os
import subprocess
from dotenv import dotenv_values
from datetime import datetime
import smail

def create_local_backup(diretorio_de_backup, nome_do_dump):
    print("Iniciando backup local")
    # Criar o backup do dump
    arquivo_novo = os.path.join(diretorio_de_backup, nome_do_dump)
    subprocess.run(f"docker exec -t pg pg_dump -n public -U {user_db} {database} > {arquivo_novo}", shell=True)
    print("Geração de dump concluído")
    return arquivo_novo

def verify_local_backup_content(arquivo_backup):
    with open(arquivo_backup, 'r') as file:
        content = file.read()
        if 'PostgreSQL database dump complete' in content:
            print(arquivo_backup, "VIÁVEL PARA RESTAURAÇÃO")
            return True
        else:
            print(arquivo_backup, "NÃO VIÁVEL PARA RESTAURAÇÃO")
            os.remove(arquivo_backup)
            return False

def main():
    # Programa principal
    config = dotenv_values(".env")

    # Carregando variáveis do .env
    global user_db, database
    user_db = config["USER_DB"]
    database = config["DATABASE"]

    # Outras variáveis
    contract = config["PATH_IMPORT"]
    tipo_sistema = config["EXTRUCTURE"]
    diretorio_de_backup = config["FOLDER_BACKUP"]
    hora_atual = datetime.now().strftime('%H-%M-%S')
    dia_atual = datetime.now().strftime('%Y-%m-%d')

    # Otimização
    nome_do_dump = f'dump_{contract}_{dia_atual}_{hora_atual}.pgsql'

    print("---------------- Backup Local Iniciado", tipo_sistema, dia_atual, hora_atual, "----------")

    # Criar pasta no sistema local, se já existir a pasta, não criar
    if not os.path.exists(diretorio_de_backup):
        os.makedirs(diretorio_de_backup, 0o775)  # Definir permissões para 0775

    print("Caminho completo local:", diretorio_de_backup)

    # Chamada da função para criar o backup local
    arquivo_backup = create_local_backup(diretorio_de_backup, nome_do_dump)
    if verify_local_backup_content(arquivo_backup):
        print("Backup local realizado com sucesso")
    else:
        print("Falha ao criar backup")
        email_subject = 'Backup do ' + tipo_sistema + ' de ' + contract + ' de ' + dia_atual
        email_body = 'Falha no Backup. Verifique o '+ tipo_sistema +' do contrato de '  + contract + ' e execute o backup manualmente.'
        smail.send(email_subject, email_body)
        

if __name__ == '__main__':
    main()