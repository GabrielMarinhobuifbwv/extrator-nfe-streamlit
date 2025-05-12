import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd

st.set_page_config(page_title="Extrator de Itens NFe XML", layout="wide")
st.title("📄 Extrator de Itens NFe XML")

uploaded_files = st.file_uploader("Selecione os arquivos XML da NFe", type="xml", accept_multiple_files=True)

# Função para extrair dados de cada NFe
def extrair_dados(xml_content):
    root = ET.fromstring(xml_content)

    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    # Dados principais
    nome_fornecedor = root.findtext('.//nfe:emit/nfe:xNome', namespaces=ns)
    numero_nf = root.findtext('.//nfe:ide/nfe:nNF', namespaces=ns)
    valor_total_nf = root.findtext('.//nfe:ICMSTot/nfe:vNF', namespaces=ns)

    # Itens (det)
    itens = []
    for det in root.findall('.//nfe:det', namespaces=ns):
        nome_item = det.findtext('nfe:prod/nfe:xProd', namespaces=ns)
        quantidade = det.findtext('nfe:prod/nfe:qCom', namespaces=ns)
        valor_unitario = det.findtext('nfe:prod/nfe:vUnCom', namespaces=ns)
        valor_total_item = det.findtext('nfe:prod/nfe:vProd', namespaces=ns)

        itens.append({
            'Nome Fornecedor': nome_fornecedor,
            'Nº NF': numero_nf,
            'Nome Item': nome_item,
            'Quantidade': quantidade,
            'Valor Unitário': valor_unitario,
            'Valor Total Item': valor_total_item,
            'Valor Total NF': valor_total_nf
        })

    return itens

# Processar arquivos
if uploaded_files:
    resultados = []
    for file in uploaded_files:
        try:
            content = file.read().decode('utf-8')
            dados = extrair_dados(content)
            resultados.extend(dados)
        except Exception as e:
            st.error(f"Erro ao processar o arquivo {file.name}: {e}")

    if resultados:
        df = pd.DataFrame(resultados)
        st.subheader("📊 Resultados extraídos:")
        st.dataframe(df)

        # Download Excel
        excel = df.to_excel(index=False, engine='openpyxl')
        st.download_button("📥 Baixar como Excel", data=excel, file_name='itens_nfe.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
