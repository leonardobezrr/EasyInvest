import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def iniciar_driver():
    # 1. Configurações (Options)
    chrome_options = Options()
    
    # Argumentos para estabilidade e "blindagem" básica
    chrome_options.add_argument("--start-maximized")  # Começa maximizado para ver todos os elementos
    chrome_options.add_argument("--disable-extensions") # Evita interferência de plugins
    chrome_options.add_argument("--no-sandbox") # Necessário em alguns ambientes Linux/Docker
    
    # 2. O TRUQUE DO ESPECIALISTA: Forçar Download de PDF
    # Isso impede que o navegador abra o PDF numa aba nova, obrigando o download.
    diretorio_atual = os.getcwd() # Ou defina um caminho fixo: r"C:\Downloads"
    
    prefs = {
        "download.default_directory": diretorio_atual, # Onde o arquivo vai cair
        "download.prompt_for_download": False,         # Não perguntar onde salvar
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True     # O PULO DO GATO: Não abre o visualizador interno do Chrome
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # 3. Inicialização do Driver
    # O ChromeDriverManager baixa a versão correta do driver automaticamente (evita dor de cabeça de versão)
    service = Service(ChromeDriverManager().install())
    
    # Cria a instância (o tal do 'driver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

# --- COMO USAR ---

# Aqui nasce o 'driver'
driver = iniciar_driver()

# Agora você pode navegar
driver.get("https://ri.raizen.com.br/divulgacoes-e-documentos/avisos-comunicados-e-fatos-relevantes/")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Supondo que 'driver' já esteja instanciado

try:
    # 1. Aguarda a lista estar visível (assumindo que já expandiu os painéis)
    # Ajuste o seletor '.list-item' ou similar conforme o HTML real da página (inspecione com F12)
    wait = WebDriverWait(driver, 15)
    
    # Estratégia: Encontrar todos os containers de documentos
    # Dica: Procure pela classe que engloba a data, o texto e os ícones
    documentos = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'list-item') or contains(@class, 'row')]")))

    print(f"🔍 Encontrados {len(documentos)} documentos potenciais.")

    from selenium.webdriver.common.by import By

    # ... (seu código anterior) ...

    # 1. Seletor do Container (Refinado para evitar lixo)
    # Tente ser mais específico para pegar apenas as linhas da tabela/lista
    # Se puder, inspecione a classe exata da LINHA (ex: 'list-item', 'feed-item')
    xpath_container = "//div[contains(@class, 'list-item') or contains(@class, 'row')]" 
    documentos = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_container)))

    print(f"🔍 Encontrados {len(documentos)} elementos. Iniciando filtragem...")

    for i, doc in enumerate(documentos):
        try:
            # 2. Correção do erro de digitação: @class (apenas um L)
            # Usamos '.' no início para indicar que a busca é DENTRO do elemento atual (doc)
            titulo_elemento = doc.find_element(By.XPATH, ".//p | .//span[contains(@class, 'title')]")
            
            titulo_texto = titulo_elemento.text.strip()
            
            # Ignora linhas vazias (comum em layouts de grid)
            if not titulo_texto:
                continue

            print(f"📄 Item {i}: {titulo_texto}")

            # ... (Lógica de clique/download aqui) ...

        except Exception as e:
            # Se falhar, é provável que o 'doc' atual não seja um documento, mas um elemento estrutural
            # O 'continue' pula para o próximo sem parar o script
            # print(f"⚠️ Ignorando item estrutural {i} (não é um documento).") 
            continue

except Exception as e:
    print(f"❌ Erro geral na busca: {e}")