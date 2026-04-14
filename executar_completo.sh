#!/bin/bash
# Script completo: Scraper + Deploy GitHub
# Execute diariamente via cron

echo "=========================================="
echo "  ROCHA CAR - Atualização Automática"
echo "=========================================="
echo ""

# Diretório do script
cd "$(dirname "$0")"

# Log
LOG_FILE="logs/execucao_$(date +%Y%m%d_%H%M%S).log"
mkdir -p logs

echo "📅 Início: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 1. Executa scraper
echo "🔍 Executando scraper..." | tee -a "$LOG_FILE"
python3 scraper_automatico.py 2>&1 | tee -a "$LOG_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Scraper concluído" | tee -a "$LOG_FILE"
else
    echo "❌ Erro no scraper" | tee -a "$LOG_FILE"
    exit 1
fi

echo "" | tee -a "$LOG_FILE"

# 2. Deploy no GitHub
echo "🚀 Fazendo deploy no GitHub..." | tee -a "$LOG_FILE"
python3 deploy_github.py 2>&1 | tee -a "$LOG_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Deploy concluído" | tee -a "$LOG_FILE"
else
    echo "❌ Erro no deploy" | tee -a "$LOG_FILE"
    exit 1
fi

echo "" | tee -a "$LOG_FILE"
echo "=========================================="  | tee -a "$LOG_FILE"
echo "✅ PROCESSO COMPLETO CONCLUÍDO"  | tee -a "$LOG_FILE"
echo "📅 Fim: $(date)"  | tee -a "$LOG_FILE"
echo "=========================================="  | tee -a "$LOG_FILE"

# Mantém apenas últimos 30 logs
cd logs
ls -t | tail -n +31 | xargs -r rm
cd ..

exit 0
