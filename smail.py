import os
import boto3
from dotenv import load_dotenv


# Carrega as variáveis de ambiente do arquivo .env do CCO backend
path_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

load_dotenv(path_env)

# Parâmetros do e-mail
sender = os.getenv('SMTP_EMAIL')
recipient = os.getenv('RECIPIENT') 


def send(subject, body):
    # Configuração do cliente SES
    ses_client = boto3.client(
        'ses',
        region_name='us-east-1',
    )
    
    # Formatação dos parâmetros do e-mail
    email_subject = {
        'Data': subject,
        'Charset': 'UTF-8'
    }
    
    email_body = {
        'Data': body,
        'Charset': 'UTF-8'
    }
    
    
    # Envio do e-mail
    response = ses_client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [
                recipient
            ]
        },
        Message={
            'Subject': email_subject,
            'Body': {
                'Text': email_body
            }
        }
    )
    
    print('E-mail enviado com sucesso!')
    print('ID da mensagem: ' + response['MessageId'])

