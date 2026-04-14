#!/bin/bash
# Setup automático para VPS Ubuntu
# Execute: bash setup_vps.sh

echo "=========================================="
echo "  ROCHA CAR - Setup VPS Ubuntu"
echo "=========================================="
echo ""

# Atualiza sistema
echo "📦 Atualizando sistema..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Instala Python e pip
echo "🐍 Instalando Python..."
sudo apt-get install -y python3 python3-pip

# Instala Chrome
echo "🌐 Instalando Google Chrome..."
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update -y
sudo apt-get install -y google-chrome-stable

# Instala dependências do Chrome
echo "📚 Instalando dependências..."
sudo apt-get install -y xvfb libxi6 libgconf-2-4 libnss3 libxss1 libappindicator1 libindicator7

# Instala Git
echo "📂 Instalando Git..."
sudo apt-get install -y git

# Instala dependências Python
echo "🔧 Instalando dependências Python..."
pip3 install -r requirements.txt

# Cria diretório para logs
mkdir -p logs

echo ""
echo "=========================================="
echo "✅ Setup concluído!"
echo "=========================================="
echo ""
echo "Próximos passos:"
echo "1. Configure o GitHub (veja DEPLOY_GITHUB.md)"
echo "2. Execute: python3 scraper_automatico.py"
echo "3. Configure cron: bash configurar_cron.sh"
echo ""
