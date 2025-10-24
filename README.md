📘 Catálogo de Datasets CCEE

Aplicação desenvolvida em Streamlit para navegação, consulta e download de datasets públicos disponibilizados pela CCEE (Câmara de Comercialização de Energia Elétrica). O projeto demonstra integração com a API CKAN da CCEE, exemplos de webscraping automatizado e interface interativa voltada ao uso corporativo.

🚀 Demonstração Online

👉 Acesse o app no Streamlit Cloud https://aplicacao-catalogo.streamlit.app/

🧩 Funcionalidades Principais

📦 Catálogo interativo de datasets: busca e filtros por nome e ano.

🔗 Integração direta com API CCEE: consulta e download de dados via endpoint CKAN.

🌐 Webscraping automatizado: coleta e exibição dos dados do PLD Horário.

💾 Exportação em CSV com registro de solicitações realizadas.

👤 Formulário de identificação (nome, e-mail, empresa).

💡 Tema claro personalizado e layout responsivo.

📁 API/
├── 📘 aplicacao_streamlit_demo_api_scrapping.py     # Código principal da aplicação Streamlit  
├── 🕷️ scrapping_pld_horario_final.py                 # Script de webscraping do PLD Horário  
├── 🌐 api_exposicao_financeira_mensal_2025.py        # Exemplo de consulta à API da CCEE  
├── 📄 lista_datasets_completa.csv                    # Catálogo com metadados dos datasets  
├── 🧾 solicitacoes_clientes.csv                      # Log das solicitações de download  
├── ⚙️ requirements.txt                               # Dependências da aplicação  



⚙️ Instalação e Execução Local

1️⃣ Clone o repositório

git clone https://github.com/Thaisdahack/catalogo_ccee.git
cd catalogo_ccee


2️⃣ Crie e ative o ambiente virtual

python -m venv .venv
.venv\Scripts\activate


3️⃣ Instale as dependências

pip install -r requirements.txt


4️⃣ Execute a aplicação

streamlit run aplicacao_streamlit_demo_api_scrapping.py

📊 Exemplo de Uso

Acesse o app e preencha suas informações de identificação.

Selecione um dataset pelo nome ou ano desejado.

Clique em 📥 Baixar para realizar o download.

Veja exemplos práticos de:

Integração via API CCEE (CKAN)

Webscraping automatizado do PLD Horário

Armazenamento de logs de uso e downloads.

| 💡 Categoria    | ⚙️ Tecnologia                                |
| :-------------- | :------------------------------------------- |
| **Linguagem**   | 🐍 Python 3.11                               |
| **Framework**   | 📊 Streamlit 1.40                            |
| **Bibliotecas** | 🧮 Pandas • 🌐 Requests • 🕷️ BeautifulSoup4 |
| **APIs**        | 🔗 CCEE Open Data (CKAN)                     |
| **Deploy**      | ☁️ Streamlit Cloud                           |


🧑‍💼 Contexto

Projeto desenvolvido como case técnico de BI e dados, com o objetivo de demonstrar:

Integração com APIs públicas e coleta automatizada de dados;

Criação de pipelines leves e dinâmicos;

Construção de interfaces interativas em Streamlit;

Documentação e deploy completo em ambiente cloud;

Boas práticas de versionamento e entrega.

📜 Licença

Este projeto é de uso educacional e demonstrativo, sem vínculo oficial com a CCEE.

💬 Contato

Desenvolvido por Thaís Dias
📧 thaishelena.data@gmail.com

💼 https://www.linkedin.com/in/thais-helena-dias/