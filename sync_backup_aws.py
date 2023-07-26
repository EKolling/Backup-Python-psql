import os
import subprocess
from dotenv import dotenv_values

def sync_local_to_aws(diretorio_de_backup, aws_s3_bucket):
    print(f"Iniciando sincronização para o AWS S3 {aws_s3_bucket}")
    # Comando aws s3 sync para sincronizar o diretório local com o bucket no AWS S3
    subprocess.run(f"aws s3 sync {diretorio_de_backup} {aws_s3_bucket} --delete", shell=True)
    print("Sincronização com o AWS S3 concluída")

def main():
    config = dotenv_values(".env")

    # Carregando variáveis do .env
    diretorio_de_backup = config["FOLDER_BACKUP"]
    aws_bucket = config["BUCKET_AWS"]
    contract = config["PATH_IMPORT"]
    tipo_sistema = config["EXTRUCTURE"]
    aws_s3_bucket = f'{aws_bucket}/{tipo_sistema}/{contract}'


    print("---------------- Sincronização AWS Iniciada ----------")
    sync_local_to_aws(diretorio_de_backup, aws_s3_bucket)
    print("---------------- Sincronização AWS Concluída ----------")

if __name__ == '__main__':
    main()