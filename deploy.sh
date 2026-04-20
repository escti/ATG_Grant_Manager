#!/bin/bash
# Script de Automação de Deploy para o OGM

REPO_DIR="/opt/ATG_Grant_Manager"
REPO_URL="https://github.com/escti/ATG_Grant_Manager.git"

echo "==============================================="
echo "   🚀 Iniciando Deploy do Oracle Grant Manager "
echo "==============================================="

# 1. Checagem e Clonagem/Atualização do Repositório
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "[+] Clonando o repositório em $REPO_DIR..."
    sudo mkdir -p "$REPO_DIR"
    sudo chown $USER:$USER "$REPO_DIR"
    git clone "$REPO_URL" "$REPO_DIR"
else
    echo "[+] Repositório encontrado. Atualizando versão mais recente do git..."
    cd "$REPO_DIR" || exit 1
    # Descarta mudanças locais (se não mapeadas) e puxa o mais atual
    git fetch origin
    git reset --hard origin/main
    git clean -fd
    git pull origin main
fi

cd "$REPO_DIR" || exit 1

# 2. Verificação de Arquivos Sensíveis
if [ ! -f "src/backend/.env" ]; then
    echo "[-] AVISO: Arquivo .env não encontrado em src/backend/.env!"
    if [ -f "src/backend/.env.example" ]; then
        echo "    Criando a partir do .env.example. POR FAVOR, edite com as senhas corretas antes de usar o sistema."
        cp src/backend/.env.example src/backend/.env
        chmod 600 src/backend/.env
    fi
fi

# 3. Build e Deploy com Docker Compose
echo "[+] Inicializando Docker Compose..."
# Remove containers orfãos e força rebuild
docker compose up -d --build

echo "==============================================="
echo "   ✅ Deploy Finalizado!"
echo "   Acesse a aplicação via http://localhost"
echo "   Logs: docker logs -f ogm-web"
echo "==============================================="
