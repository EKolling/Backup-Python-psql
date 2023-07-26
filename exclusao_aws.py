import os
import boto3
from datetime import datetime, timedelta, timezone

# Carregar variáveis de ambiente do arquivo .env
from dotenv import load_dotenv

env_path = '.env'
load_dotenv(dotenv_path=env_path)

# Configuração do cliente AWS S3
bucket_name = os.getenv('BUCKET_AWS')
contract = os.getenv('PATH_IMPORT')
tipo_sistema = os.getenv('EXTRUCTURE')

bucket_without_s3 = bucket_name.replace("s3://", "")

# Obter o período de tempo do arquivo .env e convertê-lo em dias
periodo_minimo_dias = int(os.getenv('RETENTION_DATE_PERIOD_AWS'))
periodo_maximo_dias = int(os.getenv('RETENTION_DATE_MAX'))

# Inicializar o cliente AWS S3
s3_client = boto3.client('s3')

# Função para listar arquivos no bucket
def listar_arquivos_no_bucket():
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_without_s3, Prefix=f'{tipo_sistema}/{contract}')
        if 'Contents' in response:
            print(f"Arquivos no bucket {bucket_without_s3} com mais de {periodo_minimo_dias} dias de criação e menos de {periodo_maximo_dias} dias de existência:")
            data_atual = datetime.now(timezone.utc)  # Adicionando informação de fuso horário
            for obj in response['Contents']:
                # Obter a data de criação do objeto
                created_date = obj['LastModified'].replace(tzinfo=timezone.utc)  # Definindo fuso horário para a data do objeto S3
                # Calcular a diferença de dias entre a data de criação e a data atual
                dias_de_criacao = (data_atual - created_date).days
                # Verificar se o arquivo tem mais de {periodo_minimo_dias} dias de criação e menos de {periodo_maximo_dias} dias de existência
                if dias_de_criacao > periodo_minimo_dias and dias_de_criacao < periodo_maximo_dias:
                    print(obj['Key'])
                    # Remover o arquivo do bucket
                    s3_client.delete_object(Bucket=bucket_without_s3, Key=obj['Key'])
                    print(f"Arquivo {obj['Key']} removido com sucesso.")
        else:
            print(f"Nenhum arquivo encontrado no bucket {bucket_without_s3}.")
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")

if __name__ == "__main__":
    listar_arquivos_no_bucket()
