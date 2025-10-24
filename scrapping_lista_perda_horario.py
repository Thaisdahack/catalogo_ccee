from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Inicializa o navegador
driver = webdriver.Chrome()
driver.get("https://www.ccee.org.br/login/pages/pld/index.html#pills-sul")

wait = WebDriverWait(driver, 20)

# Espera os elementos de data aparecerem
datas = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.nav-item a.nav-link")))

data_list = []
for data_item in datas:
    data_text = data_item.text.strip()
    if data_text:
        # Clica na aba da data
        driver.execute_script("arguments[0].click();", data_item)
        time.sleep(2)  # espera o conteúdo da tabela atualizar

        # Captura o título da tabela
        try:
            titulo = driver.find_element(By.CSS_SELECTOR, "div.card-body h2").text.strip()
        except:
            titulo = "PLD Horário"
        
        nome = f"{titulo} - {data_text}"
        link = driver.current_url
        data_list.append({"nome": nome, "link": link})

# Fecha o navegador
driver.quit()

# Converte para DataFrame
df = pd.DataFrame(data_list)
print(df)


# Salvar em CSV
df.to_csv("lista_perda_horario.csv", index=False, encoding="utf-8")