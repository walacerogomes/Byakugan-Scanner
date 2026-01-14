import fitz
import re
import Levenshtein
import streamlit as st

def extrair_dados_pdf(arquivo_pdf):
    doc = fitz.open(stream=arquivo_pdf.read(), filetype="pdf")
    texto = "".join([pagina.get_text() for pagina in doc])
    
    match_conta = re.search(r'\d{5}-\d{1}', texto)
    conta = match_conta.group(0) if match_conta else "N/A"
    
    return texto, conta

if st.button("Ativar Byakugan"):
    texto_pdf, conta_no_pdf = extrair_dados_pdf(arquivo_pdf)
    encontrado = False

    for dom_confiavel, dados in providers.items():
        if Levenshtein.ratio(domain, dom_confiavel) == 1.0:
            nome_esperado = dados['nome'].lower()
            
            conta_valida = (conta_no_pdf == dados['conta'])
            nome_valido = nome_esperado in texto_pdf.lower()
            
            if conta_valida and nome_valido:
                st.success(f"✅ VISÃO CLARA: Fornecedor e Conta validados para {dados['nome']}.")
            elif not nome_valido:
                st.error(f"🚨 FRAUDE DE IDENTIDADE: O nome no PDF não condiz com o fornecedor oficial ({dados['nome']})!")
            else:
                st.error(f"🚨 FRAUDE BANCÁRIA: A conta no PDF diverge do cadastro oficial!")
            
            encontrado = True
            break
