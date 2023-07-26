#!/bin/bash

# Defina o caminho do diretório do projeto
PROJETO_DIRETORIO="$HOME/projects/local_backup_python/local-backup"

# Navegue para o diretório do projeto
cd "$PROJETO_DIRETORIO" || exit 1

# Desligue os contêineres do Docker Compose, se estiverem em execução
docker-compose down

# Certifique-se de estar no branch master
git checkout master

# Atualize o repositório com as últimas mudanças
git pull

# Use sed para adicionar a linha "TZ=3" abaixo de "#Sistema LPR ou CCO?" no arquivo .env
sed -i '/#Sistema LPR ou CCO?/a TZ=3' .env

# Abra o arquivo .env para edição usando o editor "nano"
nano .env
