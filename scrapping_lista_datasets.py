import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

base_url = "https://dadosabertos.ccee.org.br"
url = f"{base_url}/dataset"
datasets = []
page = 1

while True:
    print(f"🔎 Coletando página {page}...")
    response = requests.get(url, params={"page": page})
    soup = BeautifulSoup(response.text, "html.parser")

    # Busca todos os datasets na página
    items = soup.find_all("div", class_="dataset-content")
    if not items:
        print("❌ Nenhum dataset encontrado, encerrando...")
        break

    for item in items:
        title = item.find("h2", class_="dataset-heading")
        if title:
            link_tag = title.find("a")
            if link_tag:
                name = link_tag.text.strip()
                link = base_url + link_tag["href"]
                datasets.append({"nome": name, "link": link})

    # Verifica se há mais páginas
    pagination = soup.find("ul", class_="pagination")
    if not pagination:
        print("⚠️ Nenhuma paginação encontrada — fim dos resultados.")
        break

    # Verifica se a última página está desativada (disabled)
    disabled_pages = pagination.find_all("li", class_="disabled")
    if disabled_pages and "Próximo" in pagination.text:
        # Caso o "Próximo" esteja desativado, acabou
        print("✅ Última página alcançada.")
        break

    # Testa se existe mais conteúdo ao tentar próxima página
    page += 1
    time.sleep(1)  # pausa para evitar bloqueios no servidor

print(f"\n📊 Total de datasets coletados: {len(datasets)}")
for d in datasets:
    print(f"{d['nome']} -> {d['link']}")


# Converte para DataFrame
df_datasets = pd.DataFrame(datasets)

print(df_datasets)

# Salvar em CSV
df_datasets.to_csv("lista_datasets.csv", index=False, encoding="utf-8")