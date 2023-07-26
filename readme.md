Realizar Git clone em projects/




##necessario instalar

sudo apt install python3-pip

pip3 install python-dotenv 

pip3 install python-dateutil

pip3 install boto3

pip3 install --upgrade awscli

Conteudo .env

#Sistema

PATH_IMPORT="Nome do cliente"
FOLDER_BACKUP="pasta local do linux, caminho completo"
#FOLDER_BACKUP="/home/Evandro/projects/backups"
BUCKET_AWS="s3://NOME_DO_BUCKET"



#Sistema LPR ou CCO?
EXTRUCTURE="cco"
DATABASE="nome_do_database"
USER_DB="nome_do_usuario_da_database"

##########sistema de backup
RETENTION_DATE_PERIOD_AWS=5
RETENTION_DATE_PERIOD_LOCAL=12
RETENTION_DATE_MAX=30


##########sistema de email
#destinatario
RECIPIENT="seu@mail.aqui"
#remetente
SMTP_EMAIL="seu@mail.da.amazon.aqui"

#cron
HORARIOS_BACKUP=00 5,14,19 * * *
CAMINHO_INDEX=/home/evandro/projects/local-backup/index.py
LOGS=/home/evandro/projects/LOCAL-BACKUP/output_aws.txt
