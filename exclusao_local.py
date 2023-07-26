import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

def listar_arquivos_antigos(diretorio, periodo_ret_local, periodo_ret_max):
    comando_listagem = f"find {diretorio}/dump_* -ctime +{periodo_ret_local} -ctime -{periodo_ret_max}"
    resultado_listagem = subprocess.run(comando_listagem, shell=True, capture_output=True, text=True)

    arquivos = resultado_listagem.stdout.strip().split('\n')
    return arquivos

def remover_arquivos(arquivos):
    for arquivo in arquivos:
        print(f"Arquivo encontrado: {arquivo}")
        subprocess.run(f"rm -f {arquivo}", shell=True)
        print(f"Arquivo removido: {arquivo}")

def main():
    diretorio_de_backup = os.getenv("FOLDER_BACKUP")
    periodo_ret_local = int(os.getenv("RETENTION_DATE_PERIOD_LOCAL"))
    periodo_ret_max = int(os.getenv("RETENTION_DATE_MAX"))



    # Lista os arquivos antigos
    arquivos_antigos = listar_arquivos_antigos(diretorio_de_backup, periodo_ret_local, periodo_ret_max)

    # Remove os arquivos antigos without confirmation
    if arquivos_antigos:
        print("Arquivos antigos encontrados:")
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
