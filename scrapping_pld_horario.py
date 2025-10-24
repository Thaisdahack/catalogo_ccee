# -*- coding: utf-8 -*-
import re, time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

URL = "https://www.ccee.org.br/login/pages/pld/index.html#pills-sul"

def parse_num(txt):
    if not txt:
        return None
    txt = txt.strip().replace(".", "").replace(",", ".")
    try:
        return float(txt)
    except:
        return None

def format_br(x):
    if pd.isna(x):
        return ""
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def wait_dom_ready(driver, timeout=60):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

def find_date_buttons(driver):
    elems = driver.find_elements(By.XPATH, "//button|//a")
    return [e for e in elems if re.fullmatch(r"\d{2}/\d{2}/\d{2}", e.text.strip())]

# =============================
# Configuração do navegador
# =============================
opts = Options()
opts.add_argument("--start-maximized")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
# opts.add_argument("--headless=new")  # opcional
driver = webdriver.Chrome(options=opts)

# =============================
# Página principal
# =============================
driver.get(URL)
wait_dom_ready(driver)
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'PLD Horário')]"))
)
time.sleep(6)

botoes = find_date_buttons(driver)
datas = [b.text.strip() for b in botoes]
if not datas:
    raise SystemExit("❌ Nenhum botão de data encontrado.")
print("Datas encontradas:", datas)

# =============================
# Loop principal
# =============================
for data_label in datas:
    print(f"\n=== Coletando {data_label} ===")

    # acha o botão certo
    botoes = find_date_buttons(driver)
    botao = next((b for b in botoes if b.text.strip() == data_label), None)
    if not botao:
        print(f"⚠️ Botão {data_label} não encontrado. Pulando…")
        continue

    # guarda HTML atual da tabela
    try:
        tabela_antiga = driver.find_element(By.CSS_SELECTOR, "table tbody").get_attribute("innerHTML")
    except:
        tabela_antiga = ""

    # clica e espera a classe "active"
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", botao)

    # espera o botão ficar ativo
    WebDriverWait(driver, 30).until(
        lambda d: "active" in botao.get_attribute("class")
    )

    # espera a tabela realmente mudar
    for _ in range(60):
        try:
            tabela_nova = driver.find_element(By.CSS_SELECTOR, "table tbody").get_attribute("innerHTML")
            if tabela_nova != tabela_antiga and len(tabela_nova.strip()) > 50:
                print("✅ Tabela atualizada!")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("⚠️ A tabela pode não ter sido atualizada totalmente.")

    time.sleep(2)

    # lê HTML da tabela
    tabela_html = driver.find_element(
        By.CSS_SELECTOR, "table.table.table-hover.table-sm"
    ).get_attribute("outerHTML")

    soup = BeautifulSoup(tabela_html, "html.parser")
    headers = [th.get_text(strip=True) for th in soup.select("thead th")]
    linhas = []
    for tr in soup.select("tbody tr"):
        cols = [td.get_text(" ", strip=True) for td in tr.select("td")]
        if cols:
            linhas.append([cols[0]] + [parse_num(c) for c in cols[1:]])

    if not linhas:
        print(f"⚠️ Nenhuma linha encontrada para {data_label}. Pulando.")
        continue

    df = pd.DataFrame(linhas, columns=headers)
    for c in df.columns[1:]:
        df[c] = df[c].apply(format_br)

    nome_arquivo = f"pld_horario_{data_label.replace('/', '-')}.csv"
    df.to_csv(nome_arquivo, index=False, sep=";", encoding="utf-8-sig")
    print(f"💾 Arquivo salvo: {nome_arquivo} ({len(df)} linhas)")

driver.quit()
print("\n🎯 Scraping finalizado com sucesso!")
