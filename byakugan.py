# ... (suas funções de carregamento e extração)

def extrair_dados_completos_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    texto = "".join([pagina.get_text() for pagina in doc])
    
    # Busca a conta
    match_conta = re.search(r'\d{5}-\d{1}', texto)
    conta = match_conta.group(0) if match_conta else "N/A"
    
    # Retornamos o texto completo para procurar o nome nele depois
    return texto, conta

# --- Na parte do botão de análise ---
if st.button("Ativar Byakugan"):
    # ... (pega domínios e carrega banco)
    texto_pdf, conta_no_pdf = extrair_dados_completos_pdf(arquivo_pdf)
    
    status_found = False
    for dom_confiavel, dados in providers.items():
        similarity = Levenshtein.ratio(domain, dom_confiavel)
        
        if similarity == 1.0:
            # Pega o nome esperado do banco de dados (ex: "Walace Banking")
            nome_esperado = dados['nome'].lower()
            
            # 1. Verifica se a conta está certa
            conta_valida = (conta_no_pdf == dados['conta'])
            
            # 2. Verifica se o nome do fornecedor REALMENTE aparece no texto do PDF
            nome_no_pdf_valido = nome_esperado in texto_pdf.lower()
            
            if conta_valida and nome_no_pdf_valido:
                st.success(f"✅ VISÃO CLARA: Fornecedor e Conta validados para {dados['nome']}.")
            elif not nome_no_pdf_valido:
                st.error(f"🚨 FRAUDE DE IDENTIDADE: O nome no PDF não condiz com o fornecedor oficial ({dados['nome']})!")
            else:
                st.error(f"🚨 FRAUDE BANCÁRIA: A conta no PDF diverge do cadastro oficial!")
            
            status_found = True
            break