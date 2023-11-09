import os
from FLU import create_local_backup, verify_local_backup_content, listar_arquivos_antigos, remover_arquivos
from FAU import sync_local_to_aws, listar_arquivos_no_bucket
from datetime import datetime
import smail
from pyzabbix import ZabbixMetric, ZabbixSender


#classes

class InfoTempo:
    def __init__(self, min_dias, ret_local ):
        self.hora_atual = datetime.now().strftime('%H-%M-%S')
        self.dia_atual = datetime.now().strftime('%Y-%m-%d')
        self.min_dias = min_dias
        self.ret_local = ret_local
    
    def __str__(self):
        return f"InfoTempo(hora_atual={self.hora_atual}, dia_atual={self.dia_atual}, min_dias={self.min_dias}, ret_local={self.ret_local})"

class InfoBancodedados:
    def __init__(self, user_db, database, contract, tipo_sistema, nome_do_dump, diretorio_de_backup):
        self.user_db = user_db
        self.database = database
        self.contract = contract
        self.tipo_sistema = tipo_sistema
        self.nome_do_dump = nome_do_dump

        self.diretorio_de_backup = diretorio_de_backup

class InfoAWS:
    def __init__(self,bucket_name, bucket_without_s3, aws_s3_bucket,):
        self.bucket_name = bucket_name
        self.bucket_without_s3 = bucket_without_s3
        self.aws_s3_bucket = aws_s3_bucket

#infotempo
min_dias = int(os.getenv('RETENTION_DATE_PERIOD_AWS'))
ret_local = int(os.getenv("RETENTION_DATE_PERIOD_LOCAL"))
infotempo = InfoTempo(min_dias, ret_local)

#info banco de dados
user_db = os.getenv('USER_DB')
database = os.getenv('DATABASE')
contract = os.getenv('PATH_IMPORT')
tipo_sistema = os.getenv('EXTRUCTURE')
diretorio_de_backup = os.getenv('FOLDER_BACKUP')
nome_do_dump = f'dump_{contract}_{infotempo.dia_atual}_{infotempo.hora_atual}.pgsql'
infodb = InfoBancodedados(user_db, database, contract, tipo_sistema, nome_do_dump, diretorio_de_backup)

#info AWS

bucket_name = os.getenv('BUCKET_AWS')
bucket_without_s3 = bucket_name.replace("s3://", "")
aws_s3_bucket = f'{bucket_name}/{tipo_sistema}/{contract}'
infoaws = InfoAWS(bucket_name, bucket_without_s3, aws_s3_bucket)

#ZABBIX
zabbix_server = os.getenv('ZABBIX_SERVER')
ip_local =  os.getenv('IP_LOCAL')



def main():
## inicio do backup

    print("---------------- Backup Local Iniciado", tipo_sistema, infotempo.dia_atual, infotempo.hora_atual, "----------")
    print("Caminho completo local:", diretorio_de_backup)

    # Chamada da função para criar o backup local
    arquivo_backup = create_local_backup(infodb, infotempo)
    sucesso_backup = verify_local_backup_content(arquivo_backup)

    if sucesso_backup:
        print("Backup local realizado com sucesso")
    else:
        print("Falha ao criar backup")
        email_subject = 'Backup do ' + infodb.tipo_sistema + ' de ' + infodb.contract + ' de ' + infotempo.dia_atual
        email_body = 'Falha no Backup. Verifique o '+ infodb.tipo_sistema +' do contrato de '  + infodb.contract + ' e execute o backup manualmente.'
        smail.send(email_subject, email_body)

## informativo do zabbix
    metrics = []
    m = ZabbixMetric(ip_local, 'fail', int(sucesso_backup))
    metrics.append(m)
    zbx = ZabbixSender(zabbix_server)
    zbx.send(metrics)

#sincronizar com a AWS
    print("---------------- Sincronização AWS Iniciada ----------")
    sync_local_to_aws(infodb, infoaws)

#excluir da AWS 
    print("---------------- Exclusao da AWS Iniciada ----------")
    listar_arquivos_no_bucket(infodb, infoaws, infotempo)

## exclusao local
    print("---------------- Exclusao Local Iniciada ----------")

    # Lista os arquivos antigos
    arquivos_antigos = listar_arquivos_antigos (infotempo, infodb.diretorio_de_backup)

    # Remove os arquivos antigos without confirmation
    if arquivos_antigos:
        for arquivo in arquivos_antigos:
            print(arquivo)
        print()

        resposta_confirmacao = 's'  # Change this line to always confirm removal
        if resposta_confirmacao.lower() == 's':
            remover_arquivos(arquivos_antigos)
        else:
            print("Nenhum arquivo foi removido.")
    else:
        print("Nenhum arquivo antigo encontrado.")

if __name__ == '__main__':
    main()