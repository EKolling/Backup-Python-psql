import os
from crontab import CronTab
from dotenv import load_dotenv
import subprocess

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Acesse as variáveis de ambiente definidas no arquivo .env
horarios_backup = os.getenv("HORARIOS_BACKUP")
local_backup = os.getenv("LOCAL_BACKUP")
output_file = os.getenv("OUTPUT_FILE")

# Monta o comando para o cronjob
cron_command = f"cd {local_backup} && python3 main.py > {output_file}"

# Função para visualizar o cron atual
def mostrar_cron_atual():
    cron = CronTab(user=True)
    print("Cronjobs atuais:")
    for job in cron:
        print(job)

# Função para remover o cron atual
def remover_cron_atual():
    cron = CronTab(user=True)
    cron.remove_all()
    cron.write()
    print("Cronjobs removidos com sucesso!")

# Função para adicionar o novo cronjob
def adicionar_novo_cron():
    cron = CronTab(user=True)
    job = cron.new(command=cron_command)
    job.setall(horarios_backup)  # Define o horário do cronjob
    cron.write()
    print("Novo cronjob configurado com sucesso!")

def restart_cron_service():
    try:
        subprocess.run(["sudo", "service", "cron", "restart"], check=True)
        print("Serviço do cron reiniciado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Ocorreu um erro ao reiniciar o serviço do cron: {e}")

# Mostra o cron atual antes de perguntar se deseja remover
mostrar_cron_atual()

# Pergunta ao usuário se ele deseja remover o cron atual antes de adicionar o novo
resposta = input("Deseja remover o cronjob atual antes de adicionar o novo? (S/N): ").strip().lower()
if resposta == "s":
    remover_cron_atual()

# Adiciona o novo cronjob
adicionar_novo_cron()

# Reinicia o serviço do cron
restart_cron_service()