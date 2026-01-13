 # 👁️‍🗨️ Byakugan Scanner

O **Byakugan Scanner** é uma ferramenta de auditoria de faturas desenvolvida em Python para prevenir fraudes financeiras e ataques de Phishing. 

Este projeto foi inspirado por uma notícia da **InfoSecurity Magazine**, que aponta que as fraudes financeiras já superaram o ransomware como a maior ameaça digital no mundo atual. O sistema utiliza OCR (Reconhecimento de Caracteres) e análise de domínios para garantir que o pagamento chegue ao destino correto.

---

### ✨ Funcionalidades Principais

- **Validação de Identidade:** Detecta erros sutis de grafia no nome do fornecedor (Ex: "Wallace Banking" vs "Walace Banking").
- **Inspeção Bancária:** Extrai automaticamente a conta do PDF e cruza com uma base de dados homologada.
- **Detecção de Phishing:** Identifica domínios de e-mail falsos que tentam imitar parceiros reais.
- **Interface Moderna:** UI desenvolvida com Streamlit e CSS personalizado para uma experiência intuitiva.

---

### 🛠️ Como usar este projeto

Siga os passos abaixo para rodar a ferramenta na sua máquina:

#### 1. Clonar o repositório
Abra o terminal e digite:

```bash
git clone [https://github.com/SEU_USUARIO/Byakugan-Scanner.git]
cd Byakugan-Scanner
````
#### 2. Instalar as dependências
Certifique-se de ter o Python instalado. Rode o comando abaixo para instalar tudo automaticamente:

```bash
pip install -r requirements.txt
```
#### 3. Configurar a Base de Dados (Fornecedores)
Edite o arquivo fornecedores.json com os dados dos seus parceiros de confiança

#### 4. Executar o Aplicativo
Agora, basta iniciar o Streamlit:
```bash
streamlit run app.py
```
O navegador abrirá automaticamente no endereço http://localhost:8501.

🤝 Contribuições

Fiz tudo usando Python e Streamlit para ser o mais prático possível. Críticas construtivas e sugestões são muito bem-vindas para a melhoria do projeto!

Desenvolvido por Walace Gomes 🚀
