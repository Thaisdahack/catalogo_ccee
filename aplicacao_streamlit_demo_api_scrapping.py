# ===========================================================
# 📘 Catálogo de Datasets CCEE + Case Low Code 
# ===========================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import urllib.request
import json
import requests
import time
import os
os.environ["STREAMLIT_WATCHDOG_DISABLED"] = "true"

# =======================================
# 🚀 CONFIGURAÇÃO INICIAL
# =======================================
st.set_page_config(
    page_title="Catálogo de Datasets CCEE",
    page_icon="📘",
    layout="wide"
)


# =======================================
# 🎨 MENU LATERAL COM LOGO CENTRALIZADO E RODAPÉ FIXO
# =======================================
with st.sidebar:
    st.markdown("""
        <style>
        /* ======== SIDEBAR GERAL ======== */
        section[data-testid="stSidebar"] {
            background-color: #0E3B61 !important;
            color: #ffffff !important;
            padding: 0.8rem 1rem 1.2rem 1rem !important;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 100vh;
        }

        /* ======== LOGO ======== */
        .sidebar-logo {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 0.5rem;
            margin-bottom: 0.6rem;
        }
        .sidebar-logo img {
            width: 75px; /* 🔹 tamanho equilibrado */
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }

        /* ======== TÍTULOS (agora alinhados à esquerda) ======== */
        .sidebar-title {
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            text-align: left !important;   /* 🔹 alinhamento à esquerda */
            margin: 0.3rem 0 0.1rem 0.5rem !important;
        }
        .sidebar-sub {
            font-size: 0.95rem !important;
            color: #FFFFFF !important;
            text-align: left !important;   /* 🔹 alinhamento à esquerda */
            margin: 0 0 1rem 0.5rem !important;
        }

        /* ======== BOTÕES MENU ======== */
        div[role="radiogroup"] {
            display: flex;
            flex-direction: column;
            align-items: stretch; /* 🔹 ocupa a largura total */
        }
        div[role="radiogroup"] > label {
            background: transparent !important;
            border: 1.5px solid #5DADE2 !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
            padding: 0.65rem 0.9rem !important;
            margin: 0 0.5rem 0.7rem 0.5rem !important; /* 🔹 alinhamento lateral */
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out;
            display: flex;
            align-items: center;
            justify-content: flex-start;
        }
        div[role="radiogroup"] > label:hover {
            border-color: #AED6F1 !important;
            transform: scale(1.03);
        }
        div[role="radiogroup"] > label:has(input[checked]) {
            border-color: #AED6F1 !important;
            background-color: rgba(173, 216, 230, 0.15) !important;
        }
        div[role="radiogroup"] > label, div[role="radiogroup"] > label * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        /* ======== RODAPÉ (também alinhado à esquerda) ======== */
        .sidebar-footer {
            text-align: left;
            font-size: 0.85rem;
            color: #A9CCE3;
            margin-top: auto;
            margin-left: 0.5rem;
            margin-bottom: 0.4rem;
        }
        .sidebar-footer a {
            color: #76D7C4 !important;
            text-decoration: none;
            font-weight: 600;
        }
        .sidebar-footer a:hover {
            text-decoration: underline;
        }
        </style>
    """, unsafe_allow_html=True)

    # LOGO
    st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
    try:
        
        st.image("logo.png", width=150)  
    except Exception:
        st.write(" ")  
    st.markdown('</div>', unsafe_allow_html=True)

    # TÍTULO E SUBTÍTULO (alinhados à esquerda)
    st.markdown('<div class="sidebar-title">📈 Case técnico Way2</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Integração via API e Low Code de Dados Públicos</div>', unsafe_allow_html=True)

    # MENU DE NAVEGAÇÃO
    menu = st.radio(
        "Navegação",
        ["🏠 Apresentação", "📊 Painéis Power BI", "📚 Sistema Self Service de Dados", "⚙️ Opções Low Code"],
        label_visibility="collapsed",
        index=0
    )

    # RODAPÉ FIXO (também alinhado à esquerda)
    st.markdown(
        """
        <div class="sidebar-footer">
            Desenvolvido por <a href="https://www.linkedin.com/in/thais-helena-dias/" target="_blank">Thaís Dias</a><br>
            <a href="https://github.com/Thaisdahack/catalogo_ccee" target="_blank">🔗 Repositório no GitHub</a>
        </div>
        """,
        unsafe_allow_html=True
    )



# =======================================
# 💅 ESTILO VISUAL GERAL
# =======================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"], [data-testid="stApp"], .stDataFrame, .stSelectbox, .stTextInput {
    background-color: #f9fafc !important;
    color: #2c3e50 !important;
}
h1, h2, h3, label, p, div { color: #1a5276 !important; }
.stButton>button, .stDownloadButton>button {
    background-color: #2471A3 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    background-color: #1A5276 !important;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# 🏠 APRESENTAÇÃO
# ===========================================================
if menu == "🏠 Apresentação":
    st.title("📘 Catálogo de dados, Painéis e Soluções Low-Code - Way2")

    st.markdown("""
    Este aplicativo foi desenvolvido como parte de um **case técnico** para demonstrar a capacidade de integrar 
    **fontes públicas da CCEE** em soluções **low-code** e **self-service de dados**, assim como painéis desenvolvidos em **Power BI**.

    ### 🎯 Objetivos:
    - Criar um **catálogo automatizado** de datasets da CCEE.  
    - Demonstrar a **integração via API pública (CKAN)**.  
    - Exibir uma **prova de conceito** de automação de dados **sem API**, via Power Automate Desktop.  
    - Consolidar o raciocínio técnico do projeto em um único ambiente Streamlit.
    - Desenvolver painéis em Power BI para atender a demanda do cliente.

    ---

    🔧 **Tecnologias utilizadas**
    | Categoria | Ferramenta |
    |------------|------------|
    | Linguagem | Python 3.11 |
    | Framework | Streamlit |
    | Bibliotecas | Pandas, Requests, BeautifulSoup4 | Selenium
    | APIs | CCEE Open Data (CKAN) |
    | Low Code | Power BI, Power Automate Desktop |
    | Deploy | Streamlit Cloud |
    """)

# ===========================================================
# 📊 PAINÉIS POWER BI
# ===========================================================
elif menu == "📊 Painéis Power BI":
    st.title("📊 Painéis Power BI ")

    st.markdown("""
    Nesta seção, estão listados os **painéis Power BI** desenvolvidos para o case, com base nas APIs e datasets da CCEE.

    🔹 [Painel 1 - Exposição Financeira Mensal](https://app.powerbi.com/view?r=eyJrIjoiZDVmOTZhNWUtYWQ4MS00Yjk3LTgxZjUtOWQ5MzU5MGM1ZDM2IiwidCI6IjJjZjdkNGQ1LWJkMWItNDk1Ni1hY2Y4LTI5OTUzOTliMjE2OCJ9)  
    🔹 [Painel 2 - Perda RB Horário](https://app.powerbi.com/view?r=eyJrIjoiZjAyN2E2YmEtOTgwOC00NzJmLWJmMWYtYTIzN2RmOTc2MjgxIiwidCI6IjJjZjdkNGQ1LWJkMWItNDk1Ni1hY2Y4LTI5OTUzOTliMjE2OCJ9)  
    
    """)

# ===========================================================
# 📚 SISTEMA SELF SERVICE DE DADOS (CATÁLOGO PRINCIPAL)
# ===========================================================
elif menu == "📚 Sistema Self Service de Dados":

    st.title("📚 Sistema Self Service de Dados - Datasets CCEE")
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
        dataset_selecionado = st.selectbox("Buscar dataset pelo nome:", options=[""] + nomes_dataset, index=0)

        if dataset_selecionado:
            df_filtrado = df[df["nome"].str.contains(dataset_selecionado, case=False, na=False)]
        else:
            df_filtrado = df.copy()

        ano_selecionado = st.selectbox("📅 Selecione o ano do dataset:", options=["Todos", "2023", "2024", "2025"], index=0)
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

        # =======================================
        # 🔬 DEMONSTRAÇÃO: API FUNCIONAL
        # =======================================
        st.markdown("---")
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

# ===========================================================
# ⚙️ OPÇÕES LOW CODE
# ===========================================================
elif menu == "⚙️ Opções Low Code":
    st.title("⚙️ Soluções Low-Code para Automação de Dados")

    st.markdown("""
    Esta seção apresenta duas abordagens complementares para automatizar a entrega de dados ao cliente,
    considerando fontes **com API pública** e **sem API disponível**.

    ---

    ## 🧩 1️⃣ Aquisição via API (Power BI + Power Query)

    Esta abordagem é ideal para fontes **com APIs abertas**, como o portal de **dados abertos da CCEE**.  
    O objetivo é permitir a coleta de múltiplos datasets de forma automatizada.
    
    **📋 Exemplo de função personalizada:**

    ```m
    let
        fnColetarCCEE = (resource_id as text) =>
            let
                url = "https://dadosabertos.ccee.org.br/api/3/action/datastore_search?resource_id=" & resource_id & "&limit=10000",
                json = Json.Document(Web.Contents(url)),
                registros = json[result][records],
                tabela = Table.FromList(registros, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
                expandido = Table.ExpandRecordColumn(tabela, "Column1", Record.FieldNames(registros{0})),
                tipos = Table.TransformColumnTypes(expandido, List.Transform(Table.ColumnNames(expandido), each {_, type text}))
            in
                tipos
    in
        fnColetarCCEE
    ```

    **📋 Exemplo de Consulta de Tabelas Específicas:**

    ```m
    // PLD Horário
    let
        Fonte = fnColetarCCEE("7c90a379-5e98-46ff-a11b-9120bcf81ac4")
    in
        Fonte

    // Exposição Financeira Mensal
    let
        Fonte = fnColetarCCEE("bfba2fcf-ccd5-47a3-86f9-c6a1e8ba8fbf")
    in
        Fonte
    ```

    **✨ Benefícios:**
    - Automação completa dentro do Power BI  
    - Atualizações agendadas via Power BI Service  
    - Flexibilidade para novos datasets apenas com `resource_id`

    ---

    ## 🕷️ 2️⃣ Aquisição sem API (Power Automate Desktop)

    Quando a fonte **não possui opção de download ou API pública**, utiliza-se um fluxo **RPA (Robotic Process Automation)** no **Power Automate Desktop**.

    **🧩 Etapas do fluxo:**
    1. Abrir navegador e acessar o site da CCEE.  
    2. Simular login/navegação automática.  
    3. Extrair tabela com “Extract data from web page”.  
    4. Salvar como CSV.  
    5. Enviar automaticamente ao cliente via Power Automate Web.

    ```
    Power Automate Cloud → Executa fluxo Desktop → Extrai tabela → Gera CSV → Envia e-mail
    ```

    **✨ Benefícios:**
    - Dispensa API  
    - Automação web robusta  
    - Entregas programadas por e-mail  
    - Ideal para dados que só estão disponíveis em páginas dinâmicas

    ---

    ## 🧭 Resumo das Estratégias Low-Code

    | Cenário | Ferramenta | Entrega | Complexidade |
    |----------|-------------|----------|---------------|
    | Dados com API | Power BI (Power Query) | Tabelas automatizadas via função personalizada | 🟢 Baixa |
    | Dados sem API | Power Automate Desktop | Extração RPA e envio automático ao cliente | 🟡 Média |
    """)
