#!/usr/bin/env python3
"""
Deploy automático do XML para GitHub Pages
Atualiza o repositório com o novo catálogo
"""

import os
import subprocess
from datetime import datetime
import sys

class GitHubDeployer:
    def __init__(self, repo_path='catalogo-repo'):
        self.repo_path = repo_path
        self.xml_file = 'catalogo_facebook.xml'
    
    def verificar_git(self):
        """Verifica se Git está instalado"""
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True)
            return True
        except:
            print("❌ Git não está instalado!")
            print("Instale: sudo apt-get install git")
            return False
    
    def verificar_repo(self):
        """Verifica se o repositório existe"""
        if not os.path.exists(self.repo_path):
            print(f"❌ Repositório não encontrado: {self.repo_path}")
            print("\n📋 Configure primeiro:")
            print("1. Crie um repositório no GitHub (ex: catalogo-rocha-car)")
            print("2. Clone: git clone https://github.com/SEU_USUARIO/catalogo-rocha-car.git catalogo-repo")
            print("3. Configure: cd catalogo-repo && git config user.name 'Seu Nome'")
            print("4. Configure: git config user.email 'seu@email.com'")
            return False
        return True
    
    def copiar_xml(self):
        """Copia XML para o repositório"""
        if not os.path.exists(self.xml_file):
            print(f"❌ Arquivo não encontrado: {self.xml_file}")
            return False
        
        destino = os.path.join(self.repo_path, self.xml_file)
        
        try:
            import shutil
            shutil.copy2(self.xml_file, destino)
            print(f"✓ XML copiado para {destino}")
            return True
        except Exception as e:
            print(f"❌ Erro ao copiar: {e}")
            return False
    
    def criar_index_html(self):
        """Cria página index.html com redirect"""
        index_path = os.path.join(self.repo_path, 'index.html')
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={self.xml_file}">
    <title>Rocha Car Catálogo</title>
</head>
<body>
    <h1>Rocha Car Veículos - Catálogo Facebook</h1>
    <p>Redirecionando para o catálogo XML...</p>
    <p>Ou <a href="{self.xml_file}">clique aqui</a></p>
    <p>Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
</body>
</html>"""
        
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"✓ index.html criado")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar index.html: {e}")
            return False
    
    def commit_push(self):
        """Faz commit e push das alterações"""
        try:
            os.chdir(self.repo_path)
            
            # Pull primeiro para sincronizar
            print("📥 Sincronizando com GitHub...")
            try:
                subprocess.run(['git', 'pull', '--rebase'], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                # Se falhar, tentar pull normal
                subprocess.run(['git', 'pull'], check=True, capture_output=True)
            
            # Add
            subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
            
            # Commit
            mensagem = f"Atualização automática - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            result = subprocess.run(['git', 'commit', '-m', mensagem], capture_output=True, text=True)
            
            # Se não há nada para commitar, tudo bem
            if 'nothing to commit' in result.stdout or 'nothing to commit' in result.stderr:
                print("ℹ️  Nenhuma alteração para commitar")
                return True
            
            # Push
            print("� Enviando para GitHub...")
            result = subprocess.run(['git', 'push'], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Erro no push: {result.stderr}")
                return False
            
            print(f"✓ Commit e push realizados")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro no git: {e}")
            if hasattr(e, 'stderr') and e.stderr:
                stderr_text = e.stderr.decode() if isinstance(e.stderr, bytes) else e.stderr
                print(f"   Detalhes: {stderr_text}")
            return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
        finally:
            os.chdir('..')
    
    def deploy(self):
        """Executa deploy completo"""
        print("\n" + "=" * 60)
        print("  DEPLOY GITHUB PAGES")
        print("=" * 60)
        print()
        
        if not self.verificar_git():
            return False
        
        if not self.verificar_repo():
            return False
        
        if not self.copiar_xml():
            return False
        
        self.criar_index_html()
        
        if not self.commit_push():
            return False
        
        print("\n" + "=" * 60)
        print("✅ DEPLOY CONCLUÍDO!")
        print("=" * 60)
        print()
        print("📍 URL do catálogo:")
        print("   https://SEU_USUARIO.github.io/catalogo-rocha-car/catalogo_facebook.xml")
        print()
        print("💡 Use essa URL no Facebook Catalog")
        print()
        
        return True

def main():
    deployer = GitHubDeployer()
    
    try:
        sucesso = deployer.deploy()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Deploy cancelado")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
