import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import pandas as pd
import os

# Função para extrair dados do XML
def processar_xml(caminho):
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    tree = ET.parse(caminho)
    root = tree.getroot()

    # Nome do fornecedor
    emitente = root.find('.//nfe:emit/nfe:xNome', ns)
    nome_fornecedor = emitente.text if emitente is not None else ''

    # Número da NF
    ide = root.find('.//nfe:ide/nfe:nNF', ns)
    numero_nf = ide.text if ide is not None else ''

    # Valor total da NF
    total_nf = root.find('.//nfe:ICMSTot/nfe:vNF', ns)
    valor_total_nf = total_nf.text if total_nf is not None else ''

    # Itens da nota
    itens = []
    for det in root.findall('.//nfe:det', ns):
        prod = det.find('nfe:prod', ns)
        if prod is not None:
            item = {
                'Fornecedor': nome_fornecedor,
                'Numero NF': numero_nf,
                'Item': prod.find('nfe:xProd', ns).text if prod.find('nfe:xProd', ns) is not None else '',
                'Quantidade': prod.find('nfe:qCom', ns).text if prod.find('nfe:qCom', ns) is not None else '',
                'Valor Unitario': prod.find('nfe:vUnCom', ns).text if prod.find('nfe:vUnCom', ns) is not None else '',
                'Valor Total Item': prod.find('nfe:vProd', ns).text if prod.find('nfe:vProd', ns) is not None else '',
                'Valor Total NF': valor_total_nf
            }
            itens.append(item)
    return itens

# Função para selecionar e processar arquivos
def selecionar_arquivos():
    arquivos = filedialog.askopenfilenames(filetypes=[("XML files", "*.xml")])
    if not arquivos:
        return

    todos_itens = []
    for arquivo in arquivos:
        try:
            itens_nf = processar_xml(arquivo)
            todos_itens.extend(itens_nf)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar {os.path.basename(arquivo)}: {e}")

    if todos_itens:
        df = pd.DataFrame(todos_itens)
        salvar_arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if salvar_arquivo:
            df.to_excel(salvar_arquivo, index=False)
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{salvar_arquivo}")
    else:
        messagebox.showwarning("Aviso", "Nenhum item encontrado nos arquivos selecionados.")

# Janela principal (Tkinter)
janela = tk.Tk()
janela.title("Extrator de NF-e XML para Excel")
janela.geometry("400x200")

label = tk.Label(janela, text="Selecione os arquivos XML das NF-e:", font=("Arial", 12))
label.pack(pady=20)

botao = tk.Button(janela, text="Selecionar XMLs", command=selecionar_arquivos, width=20, height=2)
botao.pack()

janela.mainloop()
