#!/bin/bash
# Configura cron para executar automaticamente todo dia às 6h

echo "=========================================="
echo "  Configurando Execução Automática"
echo "=========================================="
echo ""

# Caminho completo do script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/executar_completo.sh"

# Torna executável
chmod +x "$SCRIPT_PATH"
chmod +x "$SCRIPT_DIR/scraper_automatico.py"
chmod +x "$SCRIPT_DIR/deploy_github.py"

echo "📂 Diretório: $SCRIPT_DIR"
echo "📄 Script: $SCRIPT_PATH"
echo ""

# Cria entrada do cron
CRON_JOB="0 6 * * * cd $SCRIPT_DIR && bash $SCRIPT_PATH >> $SCRIPT_DIR/logs/cron.log 2>&1"

# Verifica se já existe
if crontab -l 2>/dev/null | grep -q "executar_completo.sh"; then
    echo "⚠️  Cron já configurado. Removendo entrada antiga..."
    crontab -l | grep -v "executar_completo.sh" | crontab -
fi

# Adiciona ao cron
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron configurado com sucesso!"
echo ""
echo "=========================================="
echo "  Configuração"
echo "=========================================="
echo "Horário: Todos os dias às 6:00 AM"
echo "Script: $SCRIPT_PATH"
echo "Logs: $SCRIPT_DIR/logs/"
echo ""
echo "=========================================="
echo "  Comandos Úteis"
echo "=========================================="
echo ""
echo "Ver cron configurado:"
echo "  crontab -l"
echo ""
echo "Executar agora (teste):"
echo "  bash $SCRIPT_PATH"
echo ""
echo "Ver logs:"
echo "  tail -f $SCRIPT_DIR/logs/cron.log"
echo ""
echo "Remover cron:"
echo "  crontab -l | grep -v 'executar_completo.sh' | crontab -"
echo ""
echo "Alterar horário (editar cron):"
echo "  crontab -e"
echo "  Formato: MIN HORA DIA MÊS DIA_SEMANA"
echo "  Exemplo 8h: 0 8 * * *"
echo ""
