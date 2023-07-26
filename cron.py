import os

def configurar_agendamento_cron():
    # Remover todos os agendamentos anteriores
    os.system("crontab -r")
    print("Todos os agendamentos anteriores foram removidos.")

    # Obter a estrutura de horários do arquivo .env
    horarios = os.getenv("HORARIOS_BACKUP")
    local_index = os.getenv("CAMINHO_INDEX")
    local_logs = os.getenv("LOGS")


    # Adicionar o agendamento ao crontab
    comando_agendamento = f"echo '{horarios} /usr/bin/python3 {local_index} > {local_logs}' | crontab -"
    os.system(comando_agendamento)
    print("Novo agendamento do backup realizado.")

    # Reiniciar o serviço cron
    os.system("sudo service cron restart")
    print("Serviço cron reiniciado.")

# Configurações
caminho_env = ".env"

# Carregar variáveis de ambiente do arquivo .env
with open(caminho_env, "r") as env_file:
    env_vars = env_file.readlines()

for env_var in env_vars:
    env_var = env_var.strip()
    if "=" in env_var:
        key, value = env_var.split("=", 1)
        os.environ[key] = value


# Configurar o agendamento do cron e reiniciar o serviço
configurar_agendamento_cron()
