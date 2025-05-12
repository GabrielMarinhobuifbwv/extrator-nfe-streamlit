import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd

st.set_page_config(page_title="Extrator de NFe XML", layout="wide")
st.title("📄 Extrator de NFe XML - Multi Arquivos")

# Upload de múltiplos arquivos XML
uploaded_files = st.file_uploader("Selecione os arquivos XML da NFe", type="xml", accept_multiple_files=True)

# Função para extrair dados de um XML NFe
def extrair_dados(xml_content):
    root = ET.fromstring(xml_content)

    ns = {
        'nfe': 'http://www.portalfiscal.inf.br/nfe'
    }

    # Dados principais
    cnpj_emitente = root.findtext('.//nfe:emit/nfe:CNPJ', namespaces=ns)
    razao_social_emitente = root.findtext('.//nfe:emit/nfe:xNome', namespaces=ns)
    cnpj_destinatario = root.findtext('.//nfe:dest/nfe:CNPJ', namespaces=ns)
    razao_social_destinatario = root.findtext('.//nfe:dest/nfe:xNome', namespaces=ns)
    valor_total = root.findtext('.//nfe:ICMSTot/nfe:vNF', namespaces=ns)
    data_emissao = root.findtext('.//nfe:ide/nfe:dhEmi', namespaces=ns)
    chave_nfe = root.attrib.get('Id', '').replace('NFe', '')

    return {
        'Chave NFe': chave_nfe,
        'CNPJ Emitente': cnpj_emitente,
        'Razão Social Emitente': razao_social_emitente,
        'CNPJ Destinatário': cnpj_destinatario,
        'Razão Social Destinatário': razao_social_destinatario,
        'Valor Total (R$)': valor_total,
        'Data Emissão': data_emissao
    }

# Processamento dos arquivos
if uploaded_files:
    resultados = []
    for file in uploaded_files:
        try:
            content = file.read().decode('utf-8')
            dados = extrair_dados(content)
            resultados.append(dados)
        except Exception as e:
            st.error(f"Erro ao processar o arquivo {file.name}: {e}")

    if resultados:
        df = pd.DataFrame(resultados)
        st.subheader("📊 Resultados extraídos:")
        st.dataframe(df)

        # Download CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar como CSV", data=csv, file_name='dados_nfe.csv', mime='text/csv')
