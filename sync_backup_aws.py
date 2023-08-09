import os
import subprocess
from dotenv import dotenv_values, load_dotenv

def sync_local_to_aws(diretorio_de_backup, aws_s3_bucket):
    print(f"Iniciando sincronização para o AWS S3 {aws_s3_bucket}")
    # Comando aws s3 sync para sincronizar o diretório local com o bucket no AWS S3
    subprocess.run(f"aws s3 sync {diretorio_de_backup} {aws_s3_bucket}", shell=True)
    print("Sincronização com o AWS S3 concluída")

def main():
    env_path = '.env'
    load_dotenv(dotenv_path=env_path)

    # Carregando variáveis do .env
    diretorio_de_backup  = os.getenv('FOLDER_BACKUP')
    aws_bucket  = os.getenv('BUCKET_AWS')
    contract  = os.getenv('PATH_IMPORT')
    tipo_sistema  = os.getenv('EXTRUCTURE')
    aws_s3_bucket = f'{aws_bucket}/{tipo_sistema}/{contract}'


    print("---------------- Sincronização AWS Iniciada ----------")
    sync_local_to_aws(diretorio_de_backup, aws_s3_bucket)

if __name__ == '__main__':
    main()
