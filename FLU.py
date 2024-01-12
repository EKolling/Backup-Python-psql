import os
import subprocess
from tqdm import tqdm
import shutil
import zipfile
import glob
import time

class InfoTempo:
    def __init__(self, hora_atual, dia_atual, min_dias, ret_local):
        self.hora_atual = hora_atual
        self.dia_atual = dia_atual
        self.min_dias = min_dias
        self.ret_local = ret_local

class InfoBancodedados:
    def __init__(self, user_db, database, contract, tipo_sistema, nome_do_dump, diretorio_de_backup, diretorio_de_projeto):
        self.user_db = user_db
        self.database = database
        self.contract = contract
        self.tipo_sistema = tipo_sistema
        self.nome_do_dump = nome_do_dump
        self.diretorio_de_projeto = diretorio_de_projeto
        self.diretorio_de_backup = diretorio_de_backup

class InfoAWS:
    def __init__(self, bucket_name, bucket_without_s3, aws_s3_bucket):
        self.bucket_name = bucket_name
        self.bucket_without_s3 = bucket_without_s3
        self.aws_s3_bucket = aws_s3_bucket



def backup_env_files(infotempo, infodb, source_dir, backup_dir):
    # Cria o diretório de backups se ainda não existir
    os.makedirs(backup_dir, exist_ok=True)

    # Pasta ENVS dentro da pasta Backups
    envs_dir = os.path.join(backup_dir, 'ENVS')
    os.makedirs(envs_dir, exist_ok=True)
    
    # Lista para armazenar os nomes dos arquivos .env encontrados
    env_files = find_env_files(source_dir, envs_dir, infotempo.dia_atual)

    # Imprime os nomes dos arquivos .env encontrados
    print("Arquivos .env encontrados:")
    for env_file in env_files:
        print(env_file)

    # Criar o nome do arquivo zip usando a data atual
    zip_file_name = f'envs_{infodb.contract}_{infotempo.dia_atual}.zip'
    zip_file_path = os.path.join(backup_dir, zip_file_name)

    # Criar um arquivo zip e adicionar os arquivos de backup
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, _, files in os.walk(envs_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, envs_dir)
                zipf.write(file_path, arcname=arcname)
    
    # Remover os arquivos .env após a criação do arquivo ZIP
    for root, _, files in os.walk(envs_dir):
        for file in files:
            if file.startswith('.env'):
                file_path = os.path.join(root, file)
                os.remove(file_path)

def find_env_files(source_dir, envs_dir, dia_atual):
    env_files = []

    # Percorre os arquivos .env no diretório de origem
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file == '.env':
                source_file_path = os.path.join(root, file)
                backup_file_name = generate_backup_file_name(source_file_path, dia_atual)
                backup_file_path = os.path.join(envs_dir, backup_file_name)
                copy_env_file(source_file_path, backup_file_path)
                env_files.append(backup_file_name)

    return env_files

def generate_backup_file_name(source_file_path, dia_atual):
    return f'.env_{os.path.basename(os.path.dirname(source_file_path))}_backup_{dia_atual}'

def copy_env_file(source_file_path, backup_file_path):
    shutil.copy(source_file_path, backup_file_path)

def create_local_backup(infodb):
    print("Iniciando backup local")
    arquivo_novo = os.path.join(infodb.diretorio_de_backup, infodb.nome_do_dump)
    tamanho_total = 0

    # Crie uma barra de progresso
    with tqdm(total=tamanho_total, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        # Execute o comando de backup
        comando_backup = f"docker exec -t pg pg_dump -n public -U {infodb.user_db} {infodb.database}"
        processo_backup = subprocess.Popen(comando_backup, shell=True, stdout=subprocess.PIPE)

        with open(arquivo_novo, 'wb') as arquivo_destino:
            for chunk in iter(lambda: processo_backup.stdout.read(1024), b''):
                arquivo_destino.write(chunk)
                pbar.update(len(chunk))

    print("Geração de dump concluído")
    return arquivo_novo

def verify_local_backup_content(arquivo_backup):
    linhas_verificadas = 10

    try:
        with open(arquivo_backup, 'r') as file:
            # Obtém o tamanho total do arquivo
            tamanho_total = os.fstat(file.fileno()).st_size
            
            # Move o cursor para trás, começando pelas últimas linhas
            for _ in range(linhas_verificadas + 1):
                tamanho_total -= 1
                while tamanho_total > 0 and file.read(1) != '\n':
                    tamanho_total -= 1

            # Volta para o início da última linha
            file.seek(tamanho_total)

            # Lê as últimas linhas
            ultimas_linhas = file.readlines()

        for linha in reversed(ultimas_linhas):
            if 'PostgreSQL database dump complete' in linha:
                print(arquivo_backup, "VIÁVEL PARA RESTAURAÇÃO")
                return True

    except Exception as e:
        print(f"Erro ao verificar conteúdo do backup: {str(e)}")

    print(arquivo_backup, "NÃO VIÁVEL PARA RESTAURAÇÃO")
    os.remove(arquivo_backup)
    return False

def listar_arquivos_antigos(infotempo, diretorio_de_backup):
    padrao_arquivos = [f"{diretorio_de_backup}/dump_*", f"{diretorio_de_backup}/envs_*"]
    arquivos = []

    for padrao in padrao_arquivos:
        arquivos.extend(glob.glob(padrao))

    arquivos_antigos = []
    for arquivo in arquivos:
        tempo_criacao = os.path.getctime(arquivo)
        dias_desde_criacao = (time.time() - tempo_criacao) / (24 * 3600)
        if dias_desde_criacao > infotempo.ret_local and dias_desde_criacao < 180:
            arquivos_antigos.append(arquivo)

    return arquivos_antigos

def remover_arquivos(arquivos):
    for arquivo in arquivos:
        print(f"Arquivo encontrado: {arquivo}")
        os.remove(arquivo)
        print(f"Arquivo removido: {arquivo}")