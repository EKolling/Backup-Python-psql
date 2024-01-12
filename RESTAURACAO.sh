#!/bin/bash
# Carregar as variáveis do arquivo .env
if [ -f .env ]; then
    source .env
else
    echo "Arquivo .env não encontrado."
    exit 1
fi

# Exibe um menu para o usuário escolher entre CCO e LPR
echo "Escolha o programa para atuar:"
echo "1. CCO"
echo "2. LPR - em manutenção" 

# Lê a escolha do usuário
read escolha

# Define as pastas com base na escolha do usuário
if [ "$escolha" = "1" ]; then
    programa="CCO"
    pasta_sistema=(
        "$HOME/projects/cco/cco-backend"
        "$HOME/projects/cco-backend"
    )
elif [ "$escolha" = "2" ]; then
    programa="LPR"
    pasta_sistema=(
        "$HOME/projects/lpr/sistema-lpr-api"
        "$HOME/projects/sistema-lpr-api"
    )
else
    echo "Escolha inválida. Saindo do script."
    exit 1
fi

# Exibe a mensagem sobre a escolha do usuário
echo "Você escolheu $programa. As seguintes pastas serão acessadas:"

# Exibe as pastas selecionadas
for pasta in "${pastas_sistema[@]}"; do
    echo "$pasta"
done


################### pasta Database

pasta_database=(
    "$HOME/projects/cco/database"
    "$HOME/projects/database"
	"/mnt/database"
)


###################### comando Docker 

executar_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        echo "Usando 'docker-compose'..."
        docker-compose "$@"
    elif command -v docker &> /dev/null && docker --version | grep -q "Docker version"; then
        echo "Usando 'docker compose'..."
        docker compose "$@"
    else
        echo "Nem 'docker-compose' nem 'docker compose' estão disponíveis."
    fi
}
##################### sistema:


# Verifica a escolha e executa o programa correspondente
case $escolha in
  1)

  #arquivo mais recente:
  

	# Confirmação para prosseguir
	read -p "Deseja iniciar restauração do sistema?? (Digite 'y' para confirmar): " confirmacao
	if [ "$confirmacao" != "y" ]; then
	    echo "Operação cancelada."
	    exit 1
	fi
	
	# Insira os comandos específicos do CCO aqui
	
	# Desliga os contêineres Docker associados ao CCO
	read -p "Deseja desligar os contêineres do CCO? (Digite 'y' para confirmar): " confirmacao
	if [ "$confirmacao" = "y" ]; then
		echo "Entrando na pasta do sistema: $pasta_sistema "
		cd $pasta_sistema && executar_docker_compose down
	fi
	
	# Confirmação para prosseguir	
	read -p "Deseja remover as pastas do banco de dados? (Digite 'y' para confirmar): " 	confirmacao
	if [ "$confirmacao" = "y" ]; then
	    sudo rm -rf $pasta_database
	fi
	
	# Confirmação para prosseguir	
	read -p "Deseja reconstruir os contêineres Docker? (Digite 'y' para confirmar): " 	confirmacao
	if [ "$confirmacao" = "y" ]; then
	    executar_docker_compose up --build pg -d
	fi
	
	#restauração do banco de dados.
	echo "Arquivos de backup disponíveis:"
	backups_disponiveis=($(ls -t $HOME/projects/backups/dump* 2>/dev/null))
	num_backups=${#backups_disponiveis[@]}

	if [ "$num_backups" -eq 0 ]; then
		echo "Nenhum backup disponível para restauração."
		exit 0
	fi

	for ((i=0; i<num_backups; i++)); do
		echo "$((i+1)). ${backups_disponiveis[i]}"
	done

	# Restauração do banco de dados.
	read -p "Digite o número do arquivo de backup que deseja restaurar (1 a $num_backups): " numero_escolhido

	# Verificar se a entrada é um número válido
	re='^[0-9]+$'
	if ! [[ $numero_escolhido =~ $re ]]; then
		echo "Entrada inválida. A restauração não será realizada."
		exit 1
	fi

	# Verificar se o número está dentro da faixa válida
		if ((numero_escolhido >= 1 && numero_escolhido <= num_backups)); then
			arquivo_escolhido=${backups_disponiveis[$((numero_escolhido-1))]}
			echo "Iniciando restauração do arquivo escolhido: $arquivo_escolhido..."
			cat "$arquivo_escolhido" | docker exec -i pg psql -U $USER_DB $DATABASE
			echo "Restauração concluída."
		else
			echo "Número fora da faixa válida. A restauração não será realizada."
	fi

	# Confirmação para prosseguir	
	read -p "Deseja reconstruir os contêineres Docker? (Digite 'y' para confirmar): " 	confirmacao
	if [ "$confirmacao" = "y" ]; then
		executar_docker_compose down -d
		time 10 seconds
	    executar_docker_compose up --build -d
	fi

    ;;
	
##############################################################
##############################################################
##############################################################
  2)
    echo "Você escolheu LPR."

    if ! dpkg -s postgresql-contrib &> /dev/null; then
        echo "O pacote 'postgresql-contrib' não está instalado. Instalando..."
        
        # Instala o pacote postgresql-contrib
        sudo apt-get install postgresql-contrib

        # Verifica se a instalação foi bem-sucedida
        if [ $? -eq 0 ]; then
            echo "Instalação concluída com sucesso."
        else
            echo "Falha na instalação. Certifique-se de ter os privilégios necessários."
            exit 1
        fi
    else
        echo "O pacote 'postgresql-contrib' já está instalado. Continuando..."
    fi

    # Confirmação para prosseguir
    read -p "Deseja iniciar restauração do sistema?? (Digite 'y' para confirmar): " confirmacao
    if [ "$confirmacao" != "y" ]; then
        echo "Operação cancelada."
        exit 1
    fi

    # Desliga os contêineres Docker associados ao LPR
    read -p "Deseja desligar os contêineres do LPR? (Digite 'y' para confirmar): " confirmacao
    if [ "$confirmacao" = "y" ]; then
        echo "Entrando na pasta do sistema: $pasta_sistema "
        cd "${pasta_sistema[0]}" && executar_docker_compose down
    fi

    # Confirmação para prosseguir    
    read -p "Deseja desmontar e remover a pasta do banco de dados? (Digite 'y' para confirmar):  " confirmacao
    if [ "$confirmacao" = "y" ]; then
        echo "Removendo a pasta do banco de dados..."
        sudo rm -rf /mnt/database
        echo "Recriando a pasta do banco de dados..."
        sudo mkdir /mnt/database
    fi

    # Desliga os contêineres Docker associados ao LPR
    read -p "Deseja reconstruir os contêineres Docker? (Digite 'y' para confirmar): " confirmacao
    if [ "$confirmacao" = "y" ]; then
        executar_docker_compose up --build pg -d
    fi

    # Restauração do banco de dados.
    echo "Arquivos de backup disponíveis:"
    backups_disponiveis=($(ls -t $HOME/projects/backups/dump* 2>/dev/null))
    num_backups=${#backups_disponiveis[@]}

    if [ "$num_backups" -eq 0 ]; then
        echo "Nenhum backup disponível para restauração."
        exit 0
    fi

    for ((i=0; i<num_backups; i++)); do
        echo "$((i+1)). ${backups_disponiveis[i]}"
    done

    # Restauração do banco de dados.
    read -p "Digite o número do arquivo de backup que deseja restaurar (1 a $num_backups): " numero_escolhido

    # Verificar se a entrada é um número válido
    re='^[0-9]+$'
    if ! [[ $numero_escolhido =~ $re ]]; then
        echo "Entrada inválida. A restauração não será realizada."
        exit 1
    fi

    # Verificar se o número está dentro da faixa válida
    if ((numero_escolhido >= 1 && numero_escolhido <= num_backups)); then
        arquivo_escolhido=${backups_disponiveis[$((numero_escolhido-1))]}
        echo "Iniciando restauração do arquivo escolhido: $arquivo_escolhido"
        psql -U $USER_DB -d $DATABASE -f "$arquivo_escolhido"
        echo "Restauração concluída."
    else
        echo "Número fora da faixa válida. A restauração não será realizada."
    fi

    # Confirmação para prosseguir    
    read -p "Reconstrua os Viewers materializados. (Digite 'y' para confirmar): " confirmacao
    if [ "$confirmacao" = "y" ]; then
        echo "Levantando API"
        executar_docker_compose up --build api -d
        echo "Executando migração"
        executar_docker_compose exec api adonis migration:run --force
        echo "Levantando o restante dos containers"
        executar_docker_compose up --build -d
    fi

    echo "Você restaurou com sucesso. Parabéns."

    ;;

  # ...

esac