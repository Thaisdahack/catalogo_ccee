# ===========================================================
# 📘 Catálogo de Datasets CCEE - Versão Estável para Deploy
# ===========================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import urllib.request
import json
import requests
import time

# =======================================
# 🚀 CONFIGURAÇÃO INICIAL
# =======================================
st.set_page_config(
    page_title="Catálogo de Datasets CCEE",
    page_icon="📘",
    layout="wide"
)

# =======================================
# 💅 ESTILO PERSONALIZADO - FUNDO CLARO GERAL
# =======================================
st.markdown("""
<style>
    /* ======= FUNDO CLARO ======= */
    [data-testid="stAppViewContainer"], [data-testid="stApp"], .stDataFrame, .stSelectbox, .stTextInput {
        background-color: #f9fafc !important;
        color: #2c3e50 !important;
    }

    /* ======= TÍTULOS E TEXTOS ======= */
    h1, h2, h3, label, p, div {
        color: #1a5276 !important;
    }

    /* ======= CONTAINER ======= */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* ======= BOTÕES ======= */
    .stButton>button, .stDownloadButton>button {
        background-color: #2471A3 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out;
        padding: 0.6rem 1.2rem !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #1A5276 !important;
        transform: scale(1.02);
    }

    /* ======= INPUTS ======= */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: white !important;
        color: #2c3e50 !important;
        border-radius: 8px !important;
        border: 1px solid #d6dbdf !important;
    }

    /* ======= DATATABLE ======= */
    [data-testid="stDataFrame"] table {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border-radius: 8px !important;
    }

    /* ======= BOX INFORMATIVO ======= */
    .stAlert {
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    /* ======= TÍTULO PRINCIPAL ======= */
    .main-title {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# =======================================
# 🧭 CABEÇALHO
# =======================================
st.markdown("""
<div class="main-title">
    <span style="font-size:2em;">📘</span>
    <h1>Catálogo de Datasets CCEE</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =======================================
# 🧾 FORMULÁRIO DO CLIENTE
# =======================================
for key in ["dados_cliente_confirmados", "nome", "email", "empresa"]:
    if key not in st.session_state:
        st.session_state[key] = None

with st.form("form_cliente"):
    st.markdown("### 👤 Informações do Cliente")
    nome_input = st.text_input("👤 Nome completo", value=st.session_state.nome or "")
    email_input = st.text_input("📧 E-mail corporativo", value=st.session_state.email or "")
    empresa_input = st.text_input("🏢 Empresa", value=st.session_state.empresa or "")
    enviado = st.form_submit_button("✅ Confirmar dados")

if enviado:
    st.session_state.dados_cliente_confirmados = True
    st.session_state.nome = nome_input
    st.session_state.email = email_input
    st.session_state.empresa = empresa_input

if not st.session_state.dados_cliente_confirmados:
    st.info("Por favor, preencha suas informações para acessar os conjuntos de dados.")
else:
    nome = st.session_state.nome
    email = st.session_state.email
    empresa = st.session_state.empresa

    st.success(f"Bem-vindo(a), **{nome}** da **{empresa}**!")
    st.markdown("---")

# =======================================
# 📦 CARREGAR LISTA DE DATASETS
# =======================================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("lista_datasets_completa.csv")
    df["link_original"] = df["link"]
    df["link"] = df["link"].apply(lambda x: f'<a href="{x}" target="_blank">🔗 Abrir Dataset</a>')
    return df

df = carregar_dados()

# =======================================
# 🔍 FILTROS DE CONSULTA
# =======================================
st.markdown("### 🔍 Filtros de consulta")

nomes_dataset = sorted(df["nome"].dropna().unique())
dataset_selecionado = st.selectbox(
    "Buscar dataset pelo nome:",
    options=[""] + nomes_dataset,
    index=0
)

if dataset_selecionado:
    df_filtrado = df[df["nome"].str.contains(dataset_selecionado, case=False, na=False)]
else:
    df_filtrado = df.copy()

ano_selecionado = st.selectbox(
    "📅 Selecione o ano do dataset:",
    options=["Todos", "2023", "2024", "2025"],
    index=0
)

if ano_selecionado != "Todos" and "ano" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["ano"] == int(ano_selecionado)]

st.markdown(f"**Total de datasets encontrados:** {len(df_filtrado)}")
st.markdown("---")

# =======================================
# 📥 DOWNLOAD AUTOMÁTICO
# =======================================
st.markdown("### 📥 Baixar Datasets")

arquivo_solicitacoes = os.path.join(os.getcwd(), "solicitacoes_clientes.csv")

def baixar_dataset_api(resource_id: str, limit: int = 100):
    try:
        url = f"https://dadosabertos.ccee.org.br/api/3/action/datastore_search?resource_id={resource_id}&limit={limit}"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        if data.get("success") and len(data["result"]["records"]) > 0:
            df = pd.DataFrame(data["result"]["records"])
            csv_data = df.to_csv(index=False, sep=";", encoding="utf-8-sig")
            return csv_data, f"✅ {len(df)} registros carregados via API."
        else:
            return None, "⚠️ API retornou sucesso, mas sem registros."
    except Exception as e:
        return None, f"❌ Erro ao acessar API: {e}"

def baixar_dataset_csv_direto(link: str):
    try:
        r = requests.get(link)
        r.raise_for_status()
        return r.content, "✅ Arquivo baixado diretamente do portal."
    except Exception as e:
        return None, f"❌ Falha ao baixar CSV direto: {e}"

for idx, row in df_filtrado.iterrows():
    nome_dataset = row["nome"]
    link_dataset = row["link_original"]
    resource_id = None
    if "resource_id=" in link_dataset:
        resource_id = link_dataset.split("resource_id=")[-1].split("&")[0]

    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{nome_dataset}**  {row['link']}", unsafe_allow_html=True)
        with col2:
            if st.button(f"📥 Baixar", key=f"btn_{idx}"):
                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                solicitacao = {
                    "data": data_atual,
                    "nome_cliente": nome,
                    "email": email,
                    "empresa": empresa,
                    "dataset": nome_dataset,
                    "filtro_usado": dataset_selecionado or "Sem filtro",
                    "ano_selecionado": ano_selecionado
                }
                nova_linha = pd.DataFrame([solicitacao])

                if os.path.exists(arquivo_solicitacoes):
                    nova_linha.to_csv(arquivo_solicitacoes, mode="a", index=False, header=False, encoding="utf-8-sig")
                else:
                    nova_linha.to_csv(arquivo_solicitacoes, index=False, header=True, encoding="utf-8-sig")

                with st.spinner("⏳ Consultando API da CCEE..."):
                    time.sleep(1)
                    conteudo, msg = (None, "")
                    if resource_id:
                        conteudo, msg = baixar_dataset_api(resource_id)
                    if not conteudo:
                        st.warning(msg)
                        st.info("🔁 Tentando baixar o arquivo direto do portal...")
                        conteudo, msg = baixar_dataset_csv_direto(link_dataset)

                if conteudo:
                    st.success(msg)
                    st.download_button(
                        label=f"💾 Salvar {nome_dataset}.csv",
                        data=conteudo,
                        file_name=f"{nome_dataset}.csv",
                        mime="text/csv"
                    )
                else:
                    st.error("❌ Não foi possível obter o dataset de nenhuma forma.")

st.markdown("---")

# =======================================
# 🔬 DEMONSTRAÇÃO: API FUNCIONAL
# =======================================
st.markdown("### 🔬 Demonstração: Consulta à API da CCEE")

if st.button("🚀 Consultar dados (PLD Histórico Semanal)"):
    with st.spinner("⏳ Consultando API da CCEE..."):
        try:
            resource_id = "7c90a379-5e98-46ff-a11b-9120bcf81ac4"
            url = f"https://dadosabertos.ccee.org.br/api/3/action/datastore_search?resource_id={resource_id}&limit=50"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())

            if data.get("success"):
                df_demo = pd.DataFrame(data["result"]["records"])
                st.success(f"✅ {len(df_demo)} registros carregados via API da CCEE.")
                st.dataframe(df_demo.head(10))
                st.download_button(
                    label="💾 Baixar CSV da API (exemplo)",
                    data=df_demo.to_csv(index=False, sep=";", encoding="utf-8-sig"),
                    file_name="pld_semanal_historico_exemplo.csv",
                    mime="text/csv"
                )
            else:
                st.error("⚠️ API respondeu, mas não retornou registros.")
        except Exception as e:
            st.error(f"❌ Erro ao consultar API: {e}")

# =======================================
# 🕷️ DEMONSTRAÇÃO: WEBSCRAPING PLD HORÁRIO
# =======================================
st.markdown("### 🕷️ Demonstração: Webscraping do PLD Horário (CCEE)")

st.write("""
Esta demonstração mostra como o webscraping automatizado coleta os valores do **PLD Horário**
diretamente do portal da **CCEE**, salvando os dados em arquivos CSV.
""")

st.info("""
⚙️ O processo completo utiliza **Selenium + BeautifulSoup**, abrindo o site da CCEE, 
clicando nas datas disponíveis e salvando os dados de cada tabela localmente.
""")

pasta_scraping = os.getcwd()
arquivos_pld = sorted(
    [f for f in os.listdir(pasta_scraping) if f.startswith("pld_horario_") and f.endswith(".csv")],
    reverse=True
)

if arquivos_pld:
    arquivo_mais_recente = arquivos_pld[0]
    st.success(f"📅 Arquivo mais recente encontrado: **{arquivo_mais_recente}**")

    df_pld = pd.read_csv(os.path.join(pasta_scraping, arquivo_mais_recente), sep=";")
    st.dataframe(df_pld.head(15))

    with open(os.path.join(pasta_scraping, arquivo_mais_recente), "rb") as f:
        st.download_button(
            label="💾 Baixar último PLD Horário (CSV)",
            data=f,
            file_name=arquivo_mais_recente,
            mime="text/csv"
        )
else:
    st.warning("⚠️ Nenhum arquivo `pld_horario_*.csv` foi encontrado na pasta do projeto.")
    st.info("Execute o script `scrapping_pld_horario_final.py` para gerar os dados.")
