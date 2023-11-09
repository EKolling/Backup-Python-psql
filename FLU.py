import os
import subprocess
from tqdm import tqdm



## gerar backup

def create_local_backup(infodb, infotempo):
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

#verificar conteudo se OK.
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


#listagem de arquivos antigos 
def listar_arquivos_antigos(infotempo, diretorio_de_backup):
    comando_listagem = f"find {diretorio_de_backup}/dump_* -ctime +{infotempo.ret_local} -ctime -180"
    resultado_listagem = subprocess.run(comando_listagem, shell=True, capture_output=True, text=True)

    arquivos = resultado_listagem.stdout.strip().split('\n')
    return arquivos

#remoção de arquivos antigos.
def remover_arquivos(arquivos):
    for arquivo in arquivos:
        print(f"Arquivo encontrado: {arquivo}")
        subprocess.run(f"rm -f {arquivo}", shell=True)
        print(f"Arquivo removido: {arquivo}")