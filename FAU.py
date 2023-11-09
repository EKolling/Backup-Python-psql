import subprocess
import boto3
from datetime import datetime, timezone

#sincronizar com a AWS
def sync_local_to_aws(infodb, infoaws):
    print(f"Iniciando sincronização para o AWS S3 {infoaws.aws_s3_bucket}")
    # Comando aws s3 sync para sincronizar o diretório local com o bucket no AWS S3
    subprocess.run(f"aws s3 sync {infodb.diretorio_de_backup} {infoaws.aws_s3_bucket}", shell=True)
    print("Sincronização com o AWS S3 concluída")

#listagem e exclusao da aws.

s3_client = boto3.client(
    's3',
    )

def listar_arquivos_no_bucket(infodb, infoaws, infotempo):
    try:
        response = s3_client.list_objects_v2(Bucket=infoaws.bucket_without_s3, Prefix=f'{infodb.tipo_sistema}/{infodb.contract}')
        if 'Contents' in response:
            print(f"Arquivos no bucket {infoaws.bucket_without_s3} com mais de {infotempo.min_dias} dias de criação e menos de 180 dias de existência:")  # Período padrão de 180 dias
            data_atual = datetime.now(timezone.utc)  # Adicionando informação de fuso horário
            for obj in response['Contents']:
                # Obter a data de criação do objeto
                created_date = obj['LastModified'].replace(tzinfo=timezone.utc)  # Definindo fuso horário para a data do objeto S3
                # Calcular a diferença de dias entre a data de criação e a data atual
                dias_de_criacao = (data_atual - created_date).days
                # Verificar se o arquivo tem mais de {periodo_minimo_dias} dias de criação e menos de {periodo_maximo_dias} dias de existência
                if dias_de_criacao > infotempo.min_dias and dias_de_criacao < 180:  # Período padrão de 180 dias
                    # Remover o arquivo do bucket
                    s3_client.delete_object(Bucket=infoaws.bucket_without_s3, Key=obj['Key'])
                    print(f"Arquivo {obj['Key']} removido com sucesso.")
        else:
            print(f"Nenhum arquivo encontrado no bucket {infoaws.bucket_without_s3}.")
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")