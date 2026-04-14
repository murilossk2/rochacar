#!/usr/bin/env python3
"""
Scraper Automático Rocha Car Veículos → Facebook Catalog XML
Extrai veículos clicando no menu e fazendo scroll infinito
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import re
import time
import sys

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

class RochaCarScraper:
    def __init__(self):
        self.base_url = "https://rochacarveiculos.com.br"
        self.driver = None
    
    def iniciar_driver(self):
        """Inicializa Chrome em modo headless"""
        print("🚀 Iniciando navegador...")
        
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            if USE_WEBDRIVER_MANAGER:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.implicitly_wait(10)
            print("✓ Navegador iniciado")
            
        except Exception as e:
            print(f"\n❌ ERRO: Não foi possível iniciar o Chrome")
            print(f"Detalhes: {e}")
            print("\n📋 Solução:")
            print("1. Instale: pip install webdriver-manager")
            print("2. Ou baixe ChromeDriver: https://chromedriver.chromium.org/")
            sys.exit(1)
    
    def acessar_estoque(self):
        """Acessa a página de estoque clicando no menu"""
        print(f"\n🌐 Acessando {self.base_url}...")
        self.driver.get(self.base_url)
        time.sleep(3)
        
        print("🖱️  Procurando link do estoque no menu...")
        
        # Tenta encontrar e clicar no link de estoque
        try:
            # Procura por diferentes seletores possíveis
            seletores = [
                "//a[contains(@href, '/estoque')]",
                "//a[contains(text(), 'Estoque')]",
                "//a[contains(text(), 'estoque')]",
                "//a[contains(text(), 'ESTOQUE')]",
                "//a[contains(text(), 'Veículos')]",
                "//a[contains(text(), 'Ver estoque')]",
            ]
            
            link_estoque = None
            for seletor in seletores:
                try:
                    elementos = self.driver.find_elements(By.XPATH, seletor)
                    for elem in elementos:
                        if elem.is_displayed():
                            link_estoque = elem
                            break
                    if link_estoque:
                        break
                except:
                    continue
            
            if link_estoque:
                print(f"✓ Link encontrado: {link_estoque.text}")
                link_estoque.click()
                time.sleep(3)
                print("✓ Página de estoque carregada")
            else:
                print("⚠️  Link não encontrado, tentando URL direta...")
                self.driver.get(f"{self.base_url}/estoque")
                time.sleep(3)
                
        except Exception as e:
            print(f"⚠️  Erro ao clicar: {e}")
            print("Tentando URL direta...")
            self.driver.get(f"{self.base_url}/estoque")
            time.sleep(3)
    
    def scroll_infinito(self, max_scrolls=20):
        """Faz scroll até carregar todos os veículos"""
        print("\n📜 Carregando veículos com scroll infinito...")
        
        ultima_altura = self.driver.execute_script("return document.body.scrollHeight")
        scrolls_sem_mudanca = 0
        total_scrolls = 0
        
        while total_scrolls < max_scrolls:
            # Scroll suave até o final
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Verifica quantos veículos já foram carregados
            veiculos_visiveis = len(self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="detalhes-veiculo"]'))
            print(f"   Scroll {total_scrolls + 1}: {veiculos_visiveis} veículos carregados", end='\r')
            
            nova_altura = self.driver.execute_script("return document.body.scrollHeight")
            
            if nova_altura == ultima_altura:
                scrolls_sem_mudanca += 1
                if scrolls_sem_mudanca >= 3:
                    print(f"\n✓ Todos os veículos carregados ({veiculos_visiveis} encontrados)")
                    break
            else:
                scrolls_sem_mudanca = 0
            
            ultima_altura = nova_altura
            total_scrolls += 1
        
        if total_scrolls >= max_scrolls:
            print(f"\n✓ Limite de scrolls atingido ({veiculos_visiveis} veículos)")
    
    def extrair_veiculos(self):
        """Extrai todos os veículos da página"""
        print("\n🔍 Extraindo dados dos veículos...")
        
        links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="detalhes-veiculo"]')
        print(f"✓ {len(links)} links encontrados")
        
        veiculos = []
        veiculos_ids = set()
        
        for idx, link in enumerate(links, 1):
            try:
                href = link.get_attribute('href')
                if not href:
                    continue
                
                # Extrai ID
                id_match = re.search(r'id=(\d+)', href)
                if not id_match:
                    continue
                
                veiculo_id = id_match.group(1)
                
                # Evita duplicatas
                if veiculo_id in veiculos_ids:
                    continue
                veiculos_ids.add(veiculo_id)
                
                # Extrai texto
                texto = link.text.strip()
                if not texto or len(texto) < 5:
                    continue
                
                # Processa dados
                veiculo = self._processar_veiculo(veiculo_id, texto, href, link)
                if veiculo:
                    veiculos.append(veiculo)
                    print(f"   [{len(veiculos)}] {veiculo['titulo'][:50]} - {veiculo['preco']}")
                
            except Exception as e:
                continue
        
        return veiculos
    
    def _processar_veiculo(self, veiculo_id, texto, href, elemento):
        """Processa dados de um veículo"""
        # Título
        linhas = [l.strip() for l in texto.split('\n') if l.strip()]
        titulo = linhas[0] if linhas else "Veículo"
        titulo = re.sub(r'^Veículo\s+', '', titulo)
        titulo = re.sub(r'\s*R\$.*$', '', titulo).strip()
        
        if not titulo or len(titulo) < 3:
            return None
        
        # Preço
        preco_match = re.search(r'R\$\s*([\d.,]+)', texto)
        preco = preco_match.group(0) if preco_match else "Consulte"
        
        # Descrição
        descricao_parts = []
        
        ano_match = re.search(r'(\d{4}/\d{4})', texto)
        if ano_match:
            descricao_parts.append(ano_match.group(1))
        
        km_match = re.search(r'([\d.]+)\s*km', texto, re.IGNORECASE)
        if km_match:
            descricao_parts.append(f"{km_match.group(1)} km")
        
        cambio_match = re.search(r'(Automático|Mecânico|Automatizado)', texto, re.IGNORECASE)
        if cambio_match:
            descricao_parts.append(cambio_match.group(1))
        
        combustivel_match = re.search(r'(Gasolina|Flex|Diesel|Híbrido|Elétrico)', texto, re.IGNORECASE)
        if combustivel_match:
            descricao_parts.append(combustivel_match.group(1))
        
        descricao = " - ".join(descricao_parts) if descricao_parts else titulo
        
        # Imagem
        imagem = ""
        try:
            img = elemento.find_element(By.TAG_NAME, 'img')
            imagem = img.get_attribute('src') or ""
        except:
            pass
        
        # Marca
        marca = titulo.split()[0] if titulo else "Veículo"
        
        return {
            'id': veiculo_id,
            'titulo': titulo[:150],
            'descricao': descricao[:5000],
            'preco': preco,
            'url': href,
            'imagem': imagem,
            'marca': marca
        }
    
    def gerar_xml_facebook(self, veiculos, arquivo='catalogo_facebook.xml'):
        """Gera XML no formato Facebook Catalog para Veículos"""
        print(f"\n📝 Gerando XML com {len(veiculos)} veículos...")
        
        # Cria RSS com namespace correto
        rss = ET.Element('rss', {
            'version': '2.0',
            'xmlns:g': 'http://base.google.com/ns/1.0'
        })
        
        channel = ET.SubElement(rss, 'channel')
        ET.SubElement(channel, 'title').text = 'Rocha Car Veículos - Estoque'
        ET.SubElement(channel, 'link').text = self.base_url
        ET.SubElement(channel, 'description').text = 'Catálogo de veículos usados'
        
        for veiculo in veiculos:
            item = ET.SubElement(channel, 'item')
            
            # Campos obrigatórios
            ET.SubElement(item, 'g:id').text = str(veiculo['id'])
            ET.SubElement(item, 'g:title').text = veiculo['titulo'][:150]
            ET.SubElement(item, 'g:description').text = veiculo['descricao'][:5000]
            ET.SubElement(item, 'g:link').text = veiculo['url']
            
            # Imagem
            if veiculo['imagem']:
                ET.SubElement(item, 'g:image_link').text = veiculo['imagem']
            
            # Preço formatado corretamente (PONTO, não vírgula)
            preco_limpo = re.sub(r'[^\d,]', '', veiculo['preco'])
            if preco_limpo:
                # Converte vírgula para ponto: 16900,00 → 16900.00
                preco_formatado = preco_limpo.replace('.', '').replace(',', '.')
                ET.SubElement(item, 'g:price').text = f"{preco_formatado} BRL"
            
            # Condição e disponibilidade
            ET.SubElement(item, 'g:condition').text = 'used'
            ET.SubElement(item, 'g:availability').text = 'in stock'
            
            # Marca
            ET.SubElement(item, 'g:brand').text = veiculo['marca']
            
            # Google Product Category (OBRIGATÓRIO para veículos)
            # 916 = Veículos e Peças > Veículos > Veículos Motorizados
            ET.SubElement(item, 'g:google_product_category').text = '916'
            
            # Campos adicionais recomendados
            # Ano do veículo
            ano_match = re.search(r'(\d{4})/(\d{4})', veiculo['descricao'])
            if ano_match:
                ET.SubElement(item, 'g:year').text = ano_match.group(2)
            
            # Quilometragem
            km_match = re.search(r'([\d.]+)\s*km', veiculo['descricao'], re.IGNORECASE)
            if km_match:
                km_limpo = km_match.group(1).replace('.', '')
                ET.SubElement(item, 'g:mileage').text = f"{km_limpo} km"
            
            # Tipo de combustível
            combustivel_match = re.search(r'(Gasolina|Flex|Diesel|Híbrido|Elétrico)', veiculo['descricao'], re.IGNORECASE)
            if combustivel_match:
                ET.SubElement(item, 'g:fuel_type').text = combustivel_match.group(1)
        
        # Gera XML formatado
        xml_string = ET.tostring(rss, encoding='utf-8', method='xml')
        dom = minidom.parseString(xml_string)
        xml_pretty = dom.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
        
        # Remove linhas vazias
        xml_lines = [line for line in xml_pretty.split('\n') if line.strip()]
        xml_final = '\n'.join(xml_lines)
        
        # Salva arquivo
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(xml_final)
        
        print(f"✓ Arquivo salvo: {arquivo}")
        print(f"✓ Formato: RSS 2.0 XML (Facebook Catalog)")
        print(f"✓ Categoria: 916 (Veículos)")
        return arquivo
    
    def executar(self):
        """Executa o processo completo"""
        try:
            self.iniciar_driver()
            self.acessar_estoque()
            self.scroll_infinito()
            veiculos = self.extrair_veiculos()
            
            if not veiculos:
                print("\n❌ Nenhum veículo encontrado!")
                return False
            
            self.gerar_xml_facebook(veiculos)
            return True
            
        finally:
            if self.driver:
                self.driver.quit()

def main():
    print("=" * 70)
    print("  ROCHA CAR VEÍCULOS → FACEBOOK CATALOG")
    print("  Extração Automática de Estoque")
    print("=" * 70)
    
    inicio = datetime.now()
    scraper = RochaCarScraper()
    
    try:
        sucesso = scraper.executar()
        
        duracao = (datetime.now() - inicio).total_seconds()
        
        print("\n" + "=" * 70)
        if sucesso:
            print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
            print(f"⏱️  Tempo: {duracao:.1f} segundos")
            print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"📄 Arquivo: catalogo_facebook.xml")
            print("\n💡 Próximo passo: Faça upload no Facebook Business Manager")
        else:
            print("❌ PROCESSO FALHOU")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Processo cancelado pelo usuário")
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
