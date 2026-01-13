import streamlit as st
import fitz
import Levenshtein
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Byakugan Scanner", page_icon="👁️‍🗨️", layout="centered")

# --- CSS PROFISSIONAL ---
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

def load_providers():
    try:
        with open('fornecedores.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def analyze_pdf_content(pdf_file):
    """Extrai texto e conta, verificando integridade básica."""
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        
        # Validação de palavras-chave
        keywords = ['fatura', 'boleto', 'pagamento', 'vencimento', 'valor']
        is_invoice = any(word in text.lower() for word in keywords)
        
        # Busca padrão de conta
        match = re.search(r'\d{5}-\d{1}', text)
        account = match.group(0) if match else None
        
        return is_invoice, text, account
    except Exception:
        return False, "", None

# --- INTERFACE ---
st.markdown("<h1>👁️‍🗨️ BYAKUGAN SCANNER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Detecção de Phishing e Fraude de Identidade por OCR</p>", unsafe_allow_html=True)

sender_email = st.text_input("E-mail do Remetente", placeholder="Ex: financeiro@fornecedor.com.br")
pdf_invoice = st.file_uploader("Upload da Fatura em PDF", type=["pdf"])

if st.button("ATIVAR VARREDURA"):
    if not sender_email or not pdf_invoice:
        st.warning("⚠️ Preencha o e-mail e envie o PDF.")
    else:
        with st.spinner('Escaneando fluxo de chakra...'):
            providers = load_providers()
            domain = sender_email.split('@')[1] if '@' in sender_email else ""
            is_invoice, full_text, extracted_account = analyze_pdf_content(pdf_invoice)
            
            st.markdown("### Relatório de Inspeção")

            if not is_invoice:
                st.error("🚫 **ARQUIVO INVÁLIDO**: O documento não parece ser uma fatura.")
            elif not extracted_account:
                st.error("🚨 **DADOS AUSENTES**: Não localizamos uma conta bancária no PDF.")
            else:
                found = False
                for trusted_domain, data in providers.items():
                    # 1. Verifica similaridade do domínio
                    domain_score = Levenshtein.ratio(domain, trusted_domain)
                    
                    if domain_score == 1.0:
                        # 2. Verifica se a conta bate exatamente
                        correct_account = (extracted_account == data['conta'])
                        
                        # 3. VERIFICAÇÃO DE NOME (O "Pulo do Gato")
                        # Verifica se o nome oficial está contido no texto do PDF
                        official_name = data['nome'].lower()
                        pdf_text_lower = full_text.lower()
                        
                        # Se o nome no PDF tiver erro de digitação (ex: Wallace vs Walace), 
                        # ele não será encontrado exatamente.
                        name_present = official_name in pdf_text_lower
                        
                        if correct_account and name_present:
                            st.success(f"✅ **FATURA AUTENTICA**: Fatura 100% validada para **{data['nome']}**.")
                        elif not name_present:
                            st.error(f"☢️ **FRAUDE DE IDENTIDADE**: O nome no PDF diverge do cadastro oficial (**{data['nome']}**). Possível tentativa de personificação!")
                        else:
                            st.error(f"🚨 **FRAUDE BANCÁRIA**: O nome está certo, mas a conta **{extracted_account}** é suspeita!")
                        
                        found = True
                        break
                    
                    elif 0.8 <= domain_score < 1.0:
                        st.error(f"🎭 **FRAUDE DETECTADA**: O e-mail '{domain}' tenta imitar '{trusted_domain}'!")
                        found = True
                        break
                
                if not found:
                    st.info("ℹ️ **DESCONHECIDO**: Este fornecedor não consta na nossa base de confiança.")

st.markdown("<br><hr><p style='text-align: center; color: #64748b; font-size: 0.8rem;'>Byakugan-Scanner v1.0 | Desenvolvido por Walace Gomes</p>", unsafe_allow_html=True)