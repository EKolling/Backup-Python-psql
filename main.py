import os
from dotenv import load_dotenv
import subprocess

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtenha o valor de PROJECTS_DIR do arquivo .env
projects_dir = os.getenv("PROJECTS_DIR")

# Use a variável projects_dir para construir caminhos absolutos
exclusao_local_path = os.path.join(projects_dir, "local-backup", "exclusao_local.py")
backup_local_path = os.path.join(projects_dir, "local-backup", "backup_local.py")
sync_backup_aws_path = os.path.join(projects_dir, "local-backup", "sync_backup_aws.py")
exclusao_aws_path = os.path.join(projects_dir, "local-backup", "exclusao_aws.py")

# Agora você pode usar os caminhos absolutos nos subprocessos
subprocess.run(["python3", backup_local_path])
subprocess.run(["python3", sync_backup_aws_path])
subprocess.run(["python3", exclusao_aws_path])
subprocess.run(["python3", exclusao_local_path])
