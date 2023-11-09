#!/bin/bash

# Verifica se o script está sendo executado como root (sudo)
if [ "$EUID" -ne 0 ]; then
  echo "Por favor, execute este script com privilégios de superusuário (sudo)."
  exit 1
fi

# Atualiza a lista de pacotes disponíveis e instala o pip3, caso ainda não esteja instalado
apt update
apt install -y python3-pip

# Instala as dependências
pip3 install python-dotenv python-dateutil boto3 python-crontab tqdm py-zabbix

# Atualiza o AWS CLI, caso já esteja instalado
pip3 install --upgrade awscli

echo "Instalação concluída!"
