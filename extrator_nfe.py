import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
from io import BytesIO

st.set_page_config(page_title="Extrator NFe XML", layout="wide")

st.title("📄 Extrator de Itens da NFe (XML)")

# Upload de múltiplos arquivos XML
uploaded_files = st.file_uploader("Selecione arquivos XML de Nota Fiscal", type="xml", accept_multiple_files=True)

data = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()

        # Namespace fix
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # Dados principais
        try:
            fornecedor = root.find('.//nfe:emit/nfe:xNome', ns).text
            numero_nf = root.find('.//nfe:ide/nfe:nNF', ns).text
            total_nf = root.find('.//nfe:total/nfe:ICMSTot/nfe:vNF', ns).text
        except:
            fornecedor = numero_nf = total_nf = "Não encontrado"

        # Itens da NF
        for det in root.findall('.//nfe:det', ns):
            prod = det.find('nfe:prod', ns)

            if prod is not None:
                nome_item = prod.find('nfe:xProd', ns).text
                quantidade = prod.find('nfe:qCom', ns).text
                valor_unitario = prod.find('nfe:vUnCom', ns).text
                valor_total_item = prod.find('nfe:vProd', ns).text

                data.append({
                    'Fornecedor': fornecedor,
                    'Número NF': numero_nf,
                    'Item': nome_item,
                    'Quantidade': quantidade,
                    'Valor Unitário': valor_unitario,
                    'Valor Total Item': valor_total_item,
                    'Valor Total NF': total_nf
                })

    # Exibir resultado
    df = pd.DataFrame(data)
    st.dataframe(df)

    # Download Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    st.download_button(
        label="📥 Baixar como Excel",
        data=output.getvalue(),
        file_name="itens_nfe.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("📥 Carregue um ou mais arquivos XML de NFe para começar.")
