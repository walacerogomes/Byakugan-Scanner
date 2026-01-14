import streamlit as st
import fitz
import Levenshtein
import json
import re

st.set_page_config(page_title="Byakugan Scanner", page_icon="👁️‍🗨️", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); font-family: 'Inter', sans-serif; }
    h1 { color: #f8fafc; text-align: center; font-weight: 700; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%); 
        color: white; font-weight: 700; border: none; box-shadow: 0px 4px 15px rgba(99, 102, 241, 0.4);
    }
    .stTextInput>div>div>input { background-color: #1e293b !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

def carregar_fornecedores():
    try:
        with open('fornecedores.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def analisar_conteudo_pdf(arquivo_pdf):
    try:
        doc = fitz.open(stream=arquivo_pdf.read(), filetype="pdf")
        texto = "".join([pagina.get_text() for pagina in doc])
        
        palavras_chave = ['fatura', 'boleto', 'pagamento', 'vencimento', 'valor']
        eh_fatura = any(palavra in texto.lower() for palavra in palavras_chave)
        
        match = re.search(r'\d{5}-\d{1}', texto)
        conta = match.group(0) if match else None
        
        return eh_fatura, texto, conta
    except Exception:
        return False, "", None

st.markdown("<h1>👁️‍🗨️ BYAKUGAN SCANNER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Detecção de Phishing e Fraude de Identidade por OCR</p>", unsafe_allow_html=True)

email_remetente = st.text_input("E-mail do Remetente", placeholder="Ex: financeiro@fornecedor.com.br")
pdf_fatura = st.file_uploader("Upload da Fatura em PDF", type=["pdf"])

if st.button("ATIVAR VARREDURA"):
    if not email_remetente or not pdf_fatura:
        st.warning("⚠️ Preencha o e-mail e envie o PDF.")
    else:
        with st.spinner('Escaneando fluxo de chakra...'):
            fornecedores = carregar_fornecedores()
            dominio = email_remetente.split('@')[1] if '@' in email_remetente else ""
            eh_fatura, texto_completo, conta_extraida = analisar_conteudo_pdf(pdf_fatura)
            
            st.markdown("### Relatório de Inspeção")

            if not eh_fatura:
                st.error("🚫 **ARQUIVO INVÁLIDO**: O documento não parece ser uma fatura.")
            elif not conta_extraida:
                st.error("🚨 **DADOS AUSENTES**: Não localizamos uma conta bancária no PDF.")
            else:
                encontrado = False
                for dom_confiavel, dados in fornecedores.items():
                    score_dominio = Levenshtein.ratio(dominio, dom_confiavel)
                    
                    if score_dominio == 1.0:
                        conta_correta = (conta_extraida == dados['conta'])
                        nome_oficial = dados['nome'].lower()
                        texto_pdf_lower = texto_completo.lower()
                        nome_presente = nome_oficial in texto_pdf_lower
                        
                        if conta_correta and nome_presente:
                            st.success(f"✅ **FATURA AUTENTICA**: Fatura 100% validada para **{dados['nome']}**.")
                        elif not nome_presente:
                            st.error(f"☢️ **FRAUDE DE IDENTIDADE**: O nome no PDF diverge do cadastro oficial (**{dados['nome']}**).")
                        else:
                            st.error(f"🚨 **FRAUDE BANCÁRIA**: O nome está certo, mas a conta **{conta_extraida}** é suspeita!")
                        
                        encontrado = True
                        break
                    
                    elif 0.8 <= score_dominio < 1.0:
                        st.error(f"🎭 **FRAUDE DETECTADA**: O e-mail '{dominio}' tenta imitar '{dom_confiavel}'!")
                        encontrado = True
                        break
                
                if not encontrado:
                    st.info("ℹ️ **DESCONHECIDO**: Este fornecedor não consta na nossa base de confiança.")

st.markdown("<br><hr><p style='text-align: center; color: #64748b; font-size: 0.8rem;'>Byakugan-Scanner v1.0 | Desenvolvido por Walace Gomes</p>", unsafe_allow_html=True)
