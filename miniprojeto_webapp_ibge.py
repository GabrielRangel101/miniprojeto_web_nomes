from pprint import pprint 
import requests
import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Web App Nomes", page_icon="📊", layout="wide")

def fazer_request(url, params=None):
    resp = requests.get(url, params=params)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        st.error(f'Erro ao buscar dados: {e}')
        resultado = None
    else: 
        resultado = resp.json()
    return resultado

def pegar_nome_por_decada(nome): 
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"
    dados_decada = fazer_request(url=url)
    
    if not dados_decada:
        return {}

    dict_decadas = {}
    for dados in dados_decada[0]['res']:
        decada = dados['periodo']
        quantidade = dados['frequencia']
        dict_decadas[decada] = quantidade
    return dict_decadas

def main():
    # Barra lateral (Sidebar)
    with st.sidebar:
        st.header("🔗 Links Úteis")
        st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/gabriel-r-lima-a954ba26a/)")
        st.markdown("[📂 Portfólio](https://gabriel-rangel.netlify.app/)")
        st.write("---")
        st.write("Este app consulta a popularidade de nomes ao longo do tempo com dados do IBGE.")
        st.markdown("**Feito por Gabriel Rangel**")

    # Título principal
    st.markdown("## 📊 Web App Nomes")
    st.markdown("### Dados do IBGE (fonte: [IBGE API](https://servicodados.ibge.gov.br/api/docs/nomes?versao=2))")

    # Campo de entrada para o nome
    nome = st.text_input("🔍 Consulte um nome:", value="Juliano")
    if not nome:
        st.stop()

    dict_decadas = pegar_nome_por_decada(nome)
    if not dict_decadas:
        st.warning(f'Nenhum dado encontrado para o nome **{nome}**')
        st.stop()
        
    # Transformando os dados em DataFrame
    df = pd.DataFrame.from_dict(dict_decadas, orient="index", columns=["Frequência"])
    df.index.name = "Década"
    df = df.reset_index()

    # Criando layout com colunas
    col1, col2 = st.columns([0.4, 0.6])
    
    with col1:
        st.subheader("📅 Frequência por década")
        st.dataframe(df, hide_index=True, width=400)

    with col2:
        st.subheader("📈 Evolução no tempo")
        st.line_chart(df.set_index("Década"))

if __name__ == '__main__':
    main()
