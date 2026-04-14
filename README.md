# 🚗 Rocha Car Veículos → Facebook Catalog (100% AUTOMÁTICO)

Sistema completo para VPS Ubuntu que extrai veículos do site Rocha Car e publica XML online gratuitamente para uso no Facebook Catalog.

## 🎯 O que o Sistema Faz

1. ✅ Acessa o site Rocha Car Veículos automaticamente
2. ✅ Clica no menu de estoque (carregamento dinâmico)
3. ✅ Faz scroll infinito para carregar todos os veículos
4. ✅ Extrai: título, descrição, preço, imagem, URL de cada veículo
5. ✅ Gera XML no formato Facebook Catalog
6. ✅ Publica XML online gratuitamente (GitHub Pages)
7. ✅ Atualiza automaticamente todo dia às 6h da manhã
8. ✅ Facebook detecta mudanças e atualiza o catálogo

## � Pré-requisitos

Antes de começar, você precisa:

- ✅ VPS Ubuntu 20.04+ (ou Debian) - Recomendado: 1GB RAM, 10GB disco
- ✅ Acesso SSH à VPS (usuário e senha ou chave SSH)
- ✅ Conta GitHub (gratuita) - https://github.com/signup
- ✅ Cliente SSH (Windows: PuTTY, PowerShell, ou WSL | Mac/Linux: Terminal)
- ✅ Cliente SFTP para upload de arquivos (FileZilla, WinSCP, ou `scp`)

## 🚀 Instalação Completa (Passo a Passo)

### PASSO 1: Preparar VPS

#### 1.1. Conectar na VPS via SSH

```bash
# Windows (PowerShell ou CMD)
ssh usuario@seu-vps-ip

# Exemplo:
ssh root@192.168.1.100
# ou
ssh ubuntu@meusite.com
```

#### 1.2. Criar diretório do projeto

```bash
# Criar pasta
mkdir -p ~/rocha-car
cd ~/rocha-car

# Verificar onde está
pwd
# Deve mostrar: /home/usuario/rocha-car
```

### PASSO 2: Upload dos Arquivos

#### Opção A: Usando SCP (Linha de comando)

```bash
# Da sua máquina local (não da VPS), execute:
scp -r * usuario@seu-vps-ip:/home/usuario/rocha-car/

# Exemplo:
scp -r * root@192.168.1.100:/root/rocha-car/
```

#### Opção B: Usando FileZilla/WinSCP (Interface gráfica)

1. Abra FileZilla ou WinSCP
2. Conecte na VPS:
   - Host: `seu-vps-ip`
   - Usuário: `seu-usuario`
   - Senha: `sua-senha`
   - Porta: `22`
3. Navegue até `/home/usuario/rocha-car/`
4. Arraste todos os arquivos do projeto para lá

#### Opção C: Usando Git (Se você tem repositório)

```bash
# Na VPS
cd ~
git clone https://github.com/SEU_USUARIO/rocha-car-scraper.git rocha-car
cd rocha-car
```

### PASSO 3: Executar Setup Automático

```bash
# Na VPS, dentro da pasta rocha-car
cd ~/rocha-car

# Tornar scripts executáveis
chmod +x *.sh

# Executar instalação (instala Python, Chrome, Git, dependências)
bash setup_vps.sh
```

**O que o setup faz:**
- Atualiza o sistema Ubuntu
- Instala Python 3 e pip
- Instala Google Chrome (para Selenium)
- Instala Git
- Instala todas as dependências Python
- Cria pasta de logs

**Tempo estimado:** 5-10 minutos

### PASSO 4: Configurar GitHub Pages (Hospedagem Gratuita)

#### 4.1. Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Preencha:
   - **Repository name:** `catalogo-rocha-car`
   - **Description:** "Catálogo XML para Facebook Ads"
   - **Visibilidade:** ✅ **Public** (obrigatório para GitHub Pages gratuito)
   - **Initialize:** Deixe DESMARCADO (não adicione README)
3. Clique em **"Create repository"**

#### 4.2. Ativar GitHub Pages

1. No repositório criado, clique em **Settings** (⚙️)
2. No menu lateral, clique em **Pages**
3. Em **Source**, selecione:
   - Branch: **main** (ou master)
   - Folder: **/ (root)**
4. Clique em **Save**
5. Aguarde 1-2 minutos
6. A URL será exibida: `https://SEU_USUARIO.github.io/catalogo-rocha-car/`

#### 4.3. Configurar Autenticação Git

**Opção A: Token HTTPS (Mais fácil)**

1. GitHub → Clique na sua foto → **Settings**
2. No menu lateral, role até **Developer settings**
3. Clique em **Personal access tokens** → **Tokens (classic)**
4. Clique em **Generate new token (classic)**
5. Preencha:
   - **Note:** `Rocha Car Deploy`
   - **Expiration:** `No expiration` (ou 1 ano)
   - **Scopes:** Marque ✅ **repo** (todas as opções dentro de repo)
6. Clique em **Generate token**
7. **COPIE O TOKEN** (ghp_xxxxxxxxxxxx) - você não verá novamente!

**Opção B: SSH (Mais seguro)**

```bash
# Na VPS, gerar chave SSH
ssh-keygen -t ed25519 -C "seu@email.com"
# Pressione Enter 3 vezes (sem senha)

# Copiar chave pública
cat ~/.ssh/id_ed25519.pub
# Copie todo o texto que aparecer
```

Adicione no GitHub:
1. GitHub → Settings → SSH and GPG keys
2. Clique em **New SSH key**
3. Title: `VPS Rocha Car`
4. Key: Cole a chave pública
5. Clique em **Add SSH key**

#### 4.4. Clonar Repositório na VPS

```bash
# Na VPS, volte para a pasta do projeto
cd ~/rocha-car

# Opção A: Clone com HTTPS (se usou token)
git clone https://github.com/SEU_USUARIO/catalogo-rocha-car.git catalogo-repo

# Opção B: Clone com SSH (se configurou SSH)
git clone git@github.com:SEU_USUARIO/catalogo-rocha-car.git catalogo-repo
```

#### 4.5. Configurar Git

```bash
cd catalogo-repo

# Configure seu nome e email
git config user.name "Seu Nome"
git config user.email "seu@email.com"

# Se usou token HTTPS, configure credenciais
git config credential.helper store

# Configure URL com token (substitua SEU_TOKEN e SEU_USUARIO)
git remote set-url origin https://SEU_TOKEN@github.com/SEU_USUARIO/catalogo-rocha-car.git

# Volte para pasta principal
cd ..
```

### PASSO 5: Testar o Sistema

```bash
# Na VPS, dentro de ~/rocha-car
cd ~/rocha-car

# Executar teste completo
bash executar_completo.sh
```

**O que vai acontecer:**
1. Scraper abre o site (modo headless - invisível)
2. Clica no menu de estoque
3. Faz scroll para carregar todos os veículos
4. Extrai dados de cada veículo
5. Gera `catalogo_facebook.xml`
6. Faz deploy no GitHub
7. Mostra resultado

**Tempo estimado:** 2-5 minutos

**Resultado esperado:**
```
==========================================
✅ PROCESSO COMPLETO CONCLUÍDO
📅 Fim: Tue Jan 14 10:30:45 UTC 2025
==========================================
```

#### 5.1. Verificar se funcionou

```bash
# Ver se o XML foi gerado
ls -lh catalogo_facebook.xml

# Ver conteúdo (primeiras linhas)
head -20 catalogo_facebook.xml

# Ver quantos veículos foram extraídos
grep -c "<item>" catalogo_facebook.xml
```

#### 5.2. Verificar URL pública

Acesse no navegador:
```
https://SEU_USUARIO.github.io/catalogo-rocha-car/catalogo_facebook.xml
```

Deve mostrar o XML com os veículos!

### PASSO 6: Configurar Execução Automática

```bash
# Na VPS
cd ~/rocha-car

# Configurar cron (agendador)
bash configurar_cron.sh
```

**O que isso faz:**
- Configura o sistema para executar automaticamente todo dia às 6h
- Você pode desconectar da VPS
- O sistema roda sozinho em background
- Logs são salvos automaticamente

#### 6.1. Verificar se o cron foi configurado

```bash
# Ver tarefas agendadas
crontab -l

# Deve mostrar algo como:
# 0 6 * * * cd /home/usuario/rocha-car && bash /home/usuario/rocha-car/executar_completo.sh >> /home/usuario/rocha-car/logs/cron.log 2>&1
```

#### 6.2. Entender o formato do cron

```
0 6 * * *
│ │ │ │ │
│ │ │ │ └─── Dia da semana (0-7, 0=Domingo)
│ │ │ └───── Mês (1-12)
│ │ └─────── Dia do mês (1-31)
│ └───────── Hora (0-23)
└─────────── Minuto (0-59)

Exemplos:
0 6 * * *     → Todo dia às 6:00
0 8 * * *     → Todo dia às 8:00
0 6 * * 1     → Toda segunda às 6:00
0 */6 * * *   → A cada 6 horas
30 6 * * *    → Todo dia às 6:30
```

### PASSO 7: Configurar Facebook Catalog

#### 7.1. Acessar Facebook Business Manager

1. Acesse: https://business.facebook.com/
2. Faça login com sua conta Facebook
3. Selecione sua conta de negócios (ou crie uma)

#### 7.2. Criar ou Acessar Catálogo

**Se já tem catálogo:**
1. No menu lateral, clique em **Catálogos**
2. Selecione seu catálogo de veículos

**Se não tem catálogo:**
1. Clique em **Catálogos** → **Criar catálogo**
2. Escolha: **Comércio eletrônico** ou **Veículos**
3. Nome: `Rocha Car Veículos`
4. Clique em **Criar**

#### 7.3. Adicionar Feed de Dados

1. Dentro do catálogo, clique em **Fontes de dados**
2. Clique em **Adicionar itens** → **Usar feeds de dados**
3. Escolha: **URL agendada**
4. Preencha:
   - **Nome do feed:** `Estoque Rocha Car`
   - **URL:** `https://SEU_USUARIO.github.io/catalogo-rocha-car/catalogo_facebook.xml`
   - **Formato:** XML
   - **Frequência de atualização:** Diária
   - **Horário:** 07:00 (1h após a atualização do XML)
   - **Fuso horário:** Seu fuso horário
5. Clique em **Adicionar feed**

#### 7.4. Verificar Importação

1. Aguarde 5-10 minutos
2. Vá em **Fontes de dados** → Seu feed
3. Clique em **Ver detalhes**
4. Verifique:
   - ✅ Status: Ativo
   - ✅ Itens importados: Número de veículos
   - ✅ Erros: 0 (ou resolva os erros mostrados)

#### 7.5. Configurar Atualização Automática

O Facebook vai:
- ✅ Buscar o XML todo dia às 7h
- ✅ Detectar veículos novos → Adiciona automaticamente
- ✅ Detectar veículos removidos → Remove dos anúncios
- ✅ Detectar preços alterados → Atualiza anúncios

## 📊 Monitoramento e Manutenção

### Ver Logs de Execução

```bash
# Conectar na VPS
ssh usuario@seu-vps-ip
cd ~/rocha-car

# Ver log do cron (execuções automáticas)
tail -f logs/cron.log

# Ver últimas execuções
ls -lht logs/

# Ver log específico
cat logs/execucao_20250114_060001.log

# Ver últimas 50 linhas do log
tail -50 logs/cron.log
```

### Verificar se o Cron está Rodando

```bash
# Ver tarefas agendadas
crontab -l

# Ver status do serviço cron
sudo systemctl status cron

# Ver logs do sistema sobre cron
grep CRON /var/log/syslog | tail -20
```

### Executar Manualmente (Teste)

```bash
# Executar agora (não precisa esperar 6h)
cd ~/rocha-car
bash executar_completo.sh

# Ver resultado
cat catalogo_facebook.xml | head -50
```

### Verificar Última Atualização

```bash
# Ver quando o XML foi atualizado pela última vez
ls -lh catalogo_facebook.xml

# Ver data/hora da última modificação
stat catalogo_facebook.xml | grep Modify
```

### Ver Quantos Veículos Estão no Catálogo

```bash
# Contar itens no XML
grep -c "<item>" catalogo_facebook.xml

# Ver títulos dos veículos
grep "<g:title>" catalogo_facebook.xml
```

## 🔧 Comandos Úteis

### Alterar Horário de Execução

```bash
# Editar cron
crontab -e

# Exemplos de horários:
# 0 8 * * *     → 8h da manhã
# 0 20 * * *    → 8h da noite
# 0 */6 * * *   → A cada 6 horas
# 0 6,18 * * *  → 6h e 18h
# 30 6 * * *    → 6h30 da manhã

# Salvar: Ctrl+X, depois Y, depois Enter
```

### Pausar Execução Automática

```bash
# Remover do cron (pausar)
crontab -l | grep -v 'executar_completo.sh' | crontab -

# Verificar se foi removido
crontab -l
```

### Reativar Execução Automática

```bash
# Reconfigurar
cd ~/rocha-car
bash configurar_cron.sh
```

### Forçar Execução Imediata

```bash
# Executar agora
cd ~/rocha-car
bash executar_completo.sh

# Ou via cron (se estiver configurado)
# Isso adiciona à fila de execução
echo "cd ~/rocha-car && bash executar_completo.sh" | at now
```

### Limpar Logs Antigos

```bash
# Manter apenas últimos 10 logs
cd ~/rocha-car/logs
ls -t execucao_*.log | tail -n +11 | xargs rm -f

# Ver espaço usado pelos logs
du -sh logs/
```

### Atualizar o Script

```bash
# Se você fez alterações no código
cd ~/rocha-car

# Fazer backup
cp scraper_automatico.py scraper_automatico.py.backup

# Editar
nano scraper_automatico.py

# Testar
python3 scraper_automatico.py

# Se funcionar, está pronto para o cron
```

## 🐛 Solução de Problemas

### Problema: Scraper não encontra veículos

```bash
# Executar manualmente para ver erros
cd ~/rocha-car
python3 scraper_automatico.py

# Verificar se o Chrome está instalado
google-chrome --version

# Reinstalar Chrome
bash setup_vps.sh
```

### Problema: Deploy falha (erro de Git)

```bash
# Verificar configuração Git
cd ~/rocha-car/catalogo-repo
git config --list

# Testar push manual
git add .
git commit -m "teste"
git push

# Se pedir senha, reconfigure o token
git remote set-url origin https://SEU_TOKEN@github.com/SEU_USUARIO/catalogo-rocha-car.git
```

### Problema: Cron não executa

```bash
# Verificar se o cron está ativo
sudo systemctl status cron

# Se não estiver, ativar
sudo systemctl start cron
sudo systemctl enable cron

# Ver logs do cron
grep CRON /var/log/syslog | tail -20

# Verificar permissões
chmod +x ~/rocha-car/executar_completo.sh
```

### Problema: Erro "Chrome not found"

```bash
# Instalar Chrome manualmente
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f -y

# Verificar instalação
which google-chrome
google-chrome --version
```

### Problema: Erro de memória (VPS pequena)

```bash
# Adicionar swap (memória virtual)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Tornar permanente
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verificar
free -h
```

### Problema: GitHub Pages não atualiza

```bash
# Verificar se o push foi feito
cd ~/rocha-car/catalogo-repo
git log -1

# Forçar atualização
git add .
git commit -m "Forçar atualização"
git push -f

# Aguardar 2-3 minutos e verificar URL
curl https://SEU_USUARIO.github.io/catalogo-rocha-car/catalogo_facebook.xml
```

### Problema: Facebook não importa o feed

1. Verifique se a URL está acessível publicamente
2. Teste no navegador: `https://SEU_USUARIO.github.io/catalogo-rocha-car/catalogo_facebook.xml`
3. Valide o XML: https://validator.w3.org/feed/
4. No Facebook, vá em Fontes de dados → Ver detalhes → Ver erros
5. Corrija os erros mostrados

## 📱 Notificações (Opcional)

### Receber Email quando Executar

Adicione ao final do `executar_completo.sh`:

```bash
# Instalar mailutils
sudo apt-get install -y mailutils

# Adicionar ao script
echo "Catálogo atualizado em $(date)" | mail -s "Rocha Car - Atualização" seu@email.com
```

### Receber Notificação no Telegram

```bash
# Criar bot no Telegram (@BotFather)
# Obter TOKEN e CHAT_ID

# Adicionar ao executar_completo.sh
TOKEN="seu_token_aqui"
CHAT_ID="seu_chat_id"
curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
  -d chat_id=$CHAT_ID \
  -d text="✅ Catálogo Rocha Car atualizado!"
```

## 📊 Estatísticas

### Ver Histórico de Veículos

```bash
# Criar script para salvar histórico
cat > ~/rocha-car/salvar_historico.sh << 'EOF'
#!/bin/bash
DATA=$(date +%Y%m%d)
TOTAL=$(grep -c "<item>" catalogo_facebook.xml)
echo "$DATA,$TOTAL" >> historico_veiculos.csv
EOF

chmod +x ~/rocha-car/salvar_historico.sh

# Adicionar ao executar_completo.sh
bash salvar_historico.sh

# Ver histórico
cat historico_veiculos.csv
```

## 🔒 Segurança

### Proteger Token do GitHub

```bash
# Usar variável de ambiente
echo 'export GITHUB_TOKEN="seu_token_aqui"' >> ~/.bashrc
source ~/.bashrc

# Modificar deploy_github.py para usar a variável
# Em vez de hardcoded no código
```

### Atualizar Sistema Regularmente

```bash
# Atualizar Ubuntu
sudo apt-get update && sudo apt-get upgrade -y

# Atualizar dependências Python
pip3 install --upgrade -r requirements.txt
```

## 📈 Otimizações

### Reduzir Tempo de Execução

No `scraper_automatico.py`, ajuste:

```python
# Linha do scroll_infinito
def scroll_infinito(self, max_scrolls=20):  # Reduzir para 10 se o site tem poucos veículos
```

### Aumentar Timeout

Se o site está lento:

```python
# Linha do time.sleep
time.sleep(3)  # Aumentar para 5 se necessário
```

## 🆓 Alternativas ao GitHub Pages

### Netlify (Mais fácil)

```bash
# Instalar Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd ~/rocha-car
netlify deploy --prod --dir=catalogo-repo

# URL gerada: https://RANDOM.netlify.app/catalogo_facebook.xml
```

### Cloudflare Pages

1. Acesse: https://pages.cloudflare.com/
2. Conecte seu repositório GitHub
3. Deploy automático a cada push
4. URL: https://catalogo-rocha-car.pages.dev/catalogo_facebook.xml

### Vercel

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd ~/rocha-car/catalogo-repo
vercel --prod

# URL gerada automaticamente
```

## 📞 Suporte

Para mais detalhes sobre GitHub Pages, veja: `DEPLOY_GITHUB.md`

## 📝 Checklist Final

Antes de considerar concluído, verifique:

- [ ] VPS Ubuntu configurada e acessível via SSH
- [ ] Todos os arquivos enviados para `/home/usuario/rocha-car/`
- [ ] Setup executado: `bash setup_vps.sh`
- [ ] Repositório GitHub criado e público
- [ ] GitHub Pages ativado
- [ ] Repositório clonado na VPS: `catalogo-repo/`
- [ ] Git configurado com nome, email e token
- [ ] Teste manual funcionou: `bash executar_completo.sh`
- [ ] XML gerado: `catalogo_facebook.xml` existe
- [ ] URL pública acessível no navegador
- [ ] Cron configurado: `crontab -l` mostra a tarefa
- [ ] Facebook Catalog configurado com a URL
- [ ] Feed importado com sucesso no Facebook

Se todos os itens estão ✅, o sistema está 100% automático!

## 🎓 Recursos Adicionais

- Documentação Selenium: https://selenium-python.readthedocs.io/
- GitHub Pages: https://pages.github.com/
- Facebook Catalog: https://www.facebook.com/business/help/125074381480892
- Cron: https://crontab.guru/ (gerador de expressões cron)

---

**Desenvolvido para Rocha Car Veículos**  
Sistema de atualização automática de catálogo para Facebook Ads

## 📤 Configurar no Facebook Catalog

1. Acesse [Facebook Business Manager](https://business.facebook.com/)
2. Vá em **Catálogos** → Seu catálogo
3. Clique em **"Fontes de dados"** → **"Adicionar itens"**
4. Escolha **"Feed de dados"**
5. Configure:
   - **Tipo**: URL agendada
   - **URL**: `https://SEU_USUARIO.github.io/catalogo-rocha-car/catalogo_facebook.xml`
   - **Formato**: XML
   - **Frequência**: Diária
   - **Horário**: 7:00 (1h após a atualização)
6. Salvar

O Facebook vai buscar o XML automaticamente todo dia!

## 🔄 Como Funciona (Fluxo Completo)

```
┌─────────────────────────────────────────────┐
│  VPS Ubuntu (Sempre ligada)                 │
├─────────────────────────────────────────────┤
│                                             │
│  06:00 - Cron dispara automaticamente      │
│    ↓                                        │
│  1. scraper_automatico.py                   │
│     • Abre site Rocha Car                  │
│     • Clica no menu estoque                │
│     • Scroll infinito                      │
│     • Extrai todos os veículos             │
│     • Gera catalogo_facebook.xml           │
│    ↓                                        │
│  2. deploy_github.py                        │
│     • Copia XML para catalogo-repo/        │
│     • git add, commit, push                │
│     • Envia para GitHub                    │
│    ↓                                        │
│  3. GitHub Pages (Automático)               │
│     • Detecta novo commit                  │
│     • Publica XML online                   │
│     • URL atualizada em 1-2 min            │
│    ↓                                        │
│  4. Facebook Catalog (07:00)                │
│     • Busca XML da URL                     │
│     • Compara com catálogo anterior        │
│     • Adiciona veículos novos              │
│     • Remove veículos vendidos             │
│     • Atualiza preços                      │
│     • Anúncios atualizados!                │
│                                             │
│  Logs salvos em: logs/                     │
│  Você pode estar desconectado ✓            │
└─────────────────────────────────────────────┘
```

## 📊 Monitoramento

```bash
# Ver logs em tempo real
tail -f logs/cron.log

# Ver últimas execuções
ls -lht logs/

# Ver cron configurado
crontab -l

# Executar manualmente (teste)
bash executar_completo.sh
```

## 🔧 Comandos Úteis

```bash
# Alterar horário (exemplo: 8h)
crontab -e
# Mude: 0 6 * * * para 0 8 * * *

# Remover automação
crontab -l | grep -v 'executar_completo.sh' | crontab -

# Ver status do último deploy
cat logs/cron.log | tail -50

# Testar apenas scraper
python3 scraper_automatico.py

# Testar apenas deploy
python3 deploy_github.py
```

## 🆓 Alternativas Gratuitas

Se não quiser usar GitHub Pages:

### Netlify (Mais fácil)
```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod
```

### Vercel
```bash
npm install -g vercel
vercel login
vercel --prod
```

### Cloudflare Pages
Conecte seu repositório GitHub em: https://pages.cloudflare.com/

Veja detalhes em `DEPLOY_GITHUB.md`

## 📋 Estrutura de Arquivos

```
rocha-car-scraper/
├── scraper_automatico.py      # Extrai veículos
├── deploy_github.py            # Publica no GitHub
├── executar_completo.sh        # Script principal
├── configurar_cron.sh          # Configura automação
├── setup_vps.sh                # Setup inicial VPS
├── requirements.txt            # Dependências Python
├── DEPLOY_GITHUB.md            # Guia detalhado
├── README.md                   # Este arquivo
├── logs/                       # Logs de execução
└── catalogo-repo/              # Repositório GitHub
    ├── catalogo_facebook.xml   # XML publicado
    └── index.html              # Página de redirect
```

## 🐛 Solução de Problemas

### Scraper não encontra veículos
```bash
# Execute manualmente para ver erros
python3 scraper_automatico.py
```

### Deploy falha
```bash
# Verifique credenciais Git
cd catalogo-repo
git config --list
```

### Cron não executa
```bash
# Verifique se está configurado
crontab -l

# Veja logs
tail -f logs/cron.log
```

### Chrome não funciona no VPS
```bash
# Reinstale Chrome
bash setup_vps.sh
```

## 📝 Requisitos

- VPS Ubuntu 20.04+ (ou Debian)
- Python 3.7+
- Git
- Conta GitHub (gratuita)
- 512MB RAM mínimo
- 1GB espaço em disco

## 💰 Custos

- ✅ GitHub Pages: GRATUITO
- ✅ Script: GRATUITO
- ✅ VPS: A partir de $3-5/mês (DigitalOcean, Vultr, Contabo)

## 🎓 Suporte

Veja documentação completa em `DEPLOY_GITHUB.md`
