# 🚀 Deploy Automático no GitHub Pages (GRATUITO)

GitHub Pages hospeda seu XML gratuitamente e fornece uma URL pública para o Facebook Catalog.

## 📋 Configuração Inicial (Fazer 1 vez)

### 1. Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Nome do repositório: `catalogo-rocha-car` (ou outro nome)
3. Marque: **Public**
4. Clique em **"Create repository"**

### 2. Ativar GitHub Pages

1. No repositório, vá em **Settings** → **Pages**
2. Em **Source**, selecione: **main** branch
3. Clique em **Save**
4. Aguarde 1-2 minutos
5. Sua URL será: `https://SEU_USUARIO.github.io/catalogo-rocha-car/`

### 3. Configurar na VPS

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/catalogo-rocha-car.git catalogo-repo

# Configure Git
cd catalogo-repo
git config user.name "Seu Nome"
git config user.email "seu@email.com"

# Volte para o diretório principal
cd ..
```

### 4. Configurar Token de Acesso (Para push automático)

1. GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Clique em **Generate new token (classic)**
3. Nome: `Rocha Car Deploy`
4. Marque: **repo** (todas as opções)
5. Clique em **Generate token**
6. **COPIE O TOKEN** (você não verá novamente!)

### 5. Configurar Credenciais na VPS

```bash
# Configure para usar o token
cd catalogo-repo
git remote set-url origin https://SEU_TOKEN@github.com/SEU_USUARIO/catalogo-rocha-car.git
cd ..
```

Ou use SSH (mais seguro):

```bash
# Gere chave SSH
ssh-keygen -t ed25519 -C "seu@email.com"

# Copie a chave pública
cat ~/.ssh/id_ed25519.pub

# Adicione no GitHub: Settings → SSH and GPG keys → New SSH key

# Configure o repositório para usar SSH
cd catalogo-repo
git remote set-url origin git@github.com:SEU_USUARIO/catalogo-rocha-car.git
cd ..
```

## ▶️ Testar Deploy

```bash
# Execute o scraper
python3 scraper_automatico.py

# Faça deploy
python3 deploy_github.py
```

Se tudo funcionar, você verá:
```
✅ DEPLOY CONCLUÍDO!
📍 URL do catálogo:
   https://SEU_USUARIO.github.io/catalogo-rocha-car/catalogo_facebook.xml
```

## 🔄 Automatizar Tudo

```bash
# Configura execução automática diária às 6h
bash configurar_cron.sh
```

Isso vai:
1. ✅ Executar scraper todo dia às 6h
2. ✅ Fazer deploy automático no GitHub
3. ✅ Atualizar o XML online
4. ✅ Facebook detecta e atualiza o catálogo

## 📍 URL Final

Sua URL pública será:
```
https://SEU_USUARIO.github.io/catalogo-rocha-car/catalogo_facebook.xml
```

Use essa URL no Facebook Business Manager!

## 🆓 Alternativas Gratuitas ao GitHub Pages

### 1. Netlify Drop

1. Acesse: https://app.netlify.com/drop
2. Arraste o arquivo `catalogo_facebook.xml`
3. Receba URL: `https://RANDOM.netlify.app/catalogo_facebook.xml`

Para automatizar:
```bash
# Instale Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod --dir=. --site=SEU_SITE_ID
```

### 2. Vercel

```bash
# Instale Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

### 3. Cloudflare Pages

1. Acesse: https://pages.cloudflare.com/
2. Conecte seu repositório GitHub
3. Deploy automático a cada push

### 4. GitLab Pages

Similar ao GitHub Pages, mas no GitLab:
```bash
git clone https://gitlab.com/SEU_USUARIO/catalogo-rocha-car.git catalogo-repo
```

## 🔧 Solução de Problemas

### Erro: "Permission denied (publickey)"
Configure SSH ou use token HTTPS

### Erro: "fatal: could not read Username"
Configure credenciais:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### GitHub Pages não atualiza
- Aguarde 1-2 minutos após o push
- Limpe cache do navegador
- Verifique se o repositório é público

### Token expirou
Gere novo token no GitHub e atualize:
```bash
cd catalogo-repo
git remote set-url origin https://NOVO_TOKEN@github.com/SEU_USUARIO/catalogo-rocha-car.git
```

## 📊 Monitorar

Ver logs:
```bash
tail -f logs/cron.log
```

Ver últimas execuções:
```bash
ls -lht logs/
```

Testar manualmente:
```bash
bash executar_completo.sh
```
