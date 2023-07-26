import subprocess

# Script de exclusão local
subprocess.run(["python3", "exclusao_local.py"])

# Script de backup
subprocess.run(["python3", "backup_local.py"])

# Script de exclusão na AWS
subprocess.run(["python3", "sync_backup_aws.py"])

# Script de exclusão na AWS
#subprocess.run(["python3", "exclusao_aws.py"])

# Script de backup
#subprocess.run(["python3", "cron.py"])
