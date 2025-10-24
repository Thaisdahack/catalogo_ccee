import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -------------------------------
# ⚙️ CONFIGURAÇÃO INICIAL
# -------------------------------
st.set_page_config(page_title="📊 Catálogo de Datasets", layout="wide")

# Logo
st.image("logo.png", width=500)
st.title("📊 Catálogo de Datasets Disponíveis")
st.markdown("---")

# -------------------------------
# 🧾 FORMULÁRIO DO CLIENTE
# -------------------------------
# Inicializa session_state
for key in ["dados_cliente_confirmados", "nome", "email", "empresa"]:
    if key not in st.session_state:
        st.session_state[key] = None

with st.form("form_cliente"):
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
    st.info("Por favor, preencha suas informações para acessar os datasets.")
    st.stop()

# Dados do cliente confirmados
nome = st.session_state.nome
email = st.session_state.email
empresa = st.session_state.empresa

st.success(f"Bem-vindo(a), **{nome}** da **{empresa}**!")
st.markdown("---")

# -------------------------------
# 📦 CARREGAR DATASETS
# -------------------------------
@st.cache_data
def carregar_dados():
    df = pd.read_csv("lista_datasets_completa.csv")
    df["link_original"] = df["link"]  # mantém link original
    df["link"] = df["link"].apply(lambda x: f'<a href="{x}" target="_blank">🔗 Abrir Dataset</a>')
    return df

df = carregar_dados()

# -------------------------------
# 🔍 FILTROS DE DATASET
# -------------------------------
st.subheader("Filtros de consulta")

# Filtro pelo nome
nomes_dataset = sorted(df["nome"].dropna().unique())
dataset_selecionado = st.selectbox(
    "🔍 Buscar dataset pelo nome",
    options=[""] + nomes_dataset,
    index=0
)

if dataset_selecionado:
    df_filtrado = df[df["nome"].str.contains(dataset_selecionado, case=False, na=False)]
else:
    df_filtrado = df.copy()

# Filtro por ano
ano_selecionado = st.selectbox(
    "Selecione o ano do dataset:",
    options=["Todos", "2023", "2024", "2025"],
    index=0
)

if ano_selecionado != "Todos":
    if "ano" in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado["ano"] == int(ano_selecionado)]
    else:
        st.info("⚠️ Nenhuma coluna 'ano' disponível no CSV para filtrar.")

st.markdown(f"**Total de datasets encontrados:** {len(df_filtrado)}")
st.markdown("---")

# -------------------------------
# 📥 DOWNLOAD COM REGISTRO AUTOMÁTICO
# -------------------------------
st.subheader("📥 Baixar Datasets")

arquivo_solicitacoes = os.path.join(os.getcwd(), "solicitacoes_clientes.csv")

def baixar_dataset_placeholder(link):
    """Função placeholder para download"""
    return f"Conteúdo do dataset de {link}".encode("utf-8")

# Layout tipo card
for idx, row in df_filtrado.iterrows():
    nome_dataset = row["nome"]
    link_dataset = row["link_original"]

    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{nome_dataset}**  {row['link']}", unsafe_allow_html=True)
        with col2:
            if st.button(f"📥 Baixar", key=idx):
                # Registrar solicitação
                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                solicitacao = {
                    "data": data_atual,
                    "nome_cliente": nome,
                    "email": email,
                    "empresa": empresa,
                    "dataset": nome_dataset,
                    "filtro_usado": dataset_selecionado if dataset_selecionado else "Sem filtro",
                    "ano_selecionado": ano_selecionado
                }
                nova_linha = pd.DataFrame([solicitacao])

                # Cria ou anexa CSV na pasta do projeto
                if os.path.exists(arquivo_solicitacoes):
                    nova_linha.to_csv(arquivo_solicitacoes, mode="a", index=False, header=False, encoding="utf-8-sig")
                else:
                    nova_linha.to_csv(arquivo_solicitacoes, index=False, header=True, encoding="utf-8-sig")

                # Download direto (placeholder)
                conteudo = baixar_dataset_placeholder(link_dataset)
                st.download_button(
                    label=f"💾 Salvar {nome_dataset}.csv",
                    data=conteudo,
                    file_name=f"{nome_dataset}.csv",
                    mime="text/csv"
                )

                st.success(f"✅ Solicitação registrada e {nome_dataset} pronto para download!")
