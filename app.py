import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- 1. CONFIGURAÇÃO DA PÁGINA E IDENTIDADE VISUAL ---
# Carregamos a foto principal para usar como ícone na aba do browser (Favicon)
# E para a barra lateral.
img_perfil_main = Image.open("perfil.png")

# Carregamos a segunda foto para o cabeçalho central.
img_perfil_head = Image.open("perfil_2.png")

st.set_page_config(
    page_title="Simão Digital",
    page_icon=img_perfil_main, # MANTEMOS A TUA FOTO PRINCIPAL NA ABA!
    layout="centered"
)

# --- 2. CONFIGURAÇÃO DA API (Tua chave vencedora) ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 3. CARREGAMENTO DO CONTEXTO (TEU CÉREBRO DIGITAL) ---
def carregar_contexto():
    ficheiros = ['persona.md', 'cv.md', 'Recruiter_FAQs.md', 'Biografia.md']
    contexto = ""
    for f_nome in ficheiros:
        if os.path.exists(f_nome):
            with open(f_nome, 'r', encoding='utf-8') as f:
                contexto += f.read() + "\n\n"
    return contexto

contexto_simao = carregar_contexto()

# --- Secção 4. BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image(img_perfil_main, width=150) # TUA FOTO PRINCIPAL AQUI!
    st.title("Simão Lind")
    st.write("Senior Backend Developer & IA Enthusiast")
    st.markdown("---")
    st.markdown("🔗 [LinkedIn](https://pt.linkedin.com/in/sim%C3%A3o-lind-a2649654)")
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

# --- 5. CABEÇALHO DA PÁGINA ---
# Ajustamos a proporção das colunas para [1, 4] para dar mais espaço à foto
col1, col2 = st.columns([1, 4]) 

with col1:
    # Aumentamos o width de 80 para 150 (ou o valor que preferires)
    st.image(img_perfil_head, width=150) 

with col2:
    # Adicionamos um pouco de espaço no topo para alinhar o texto com o meio da foto
    st.write("") 
    st.title("Digital Simão")
    st.caption("My intelligent assistant trained on my journey and vision.")

# --- Secção 6 (Lógica do Chat) ---
# ... (Manter igual ao teu código atual) ...
# --- 6. LÓGICA DO CHAT ---

if "chat" not in st.session_state:
    # Adicionamos um reforço explícito aqui no sistema
    reforco_idioma = "\n\n Important: Always reply on users language (PT, EN, ES ou DE)."
    
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash',
        system_instruction=contexto_simao + reforco_idioma # Fundimos o contexto com a regra
    )
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do utilizador
if prompt := st.chat_input("Hello! What would you like to know about me?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"There was a small hiccup in the API. Error: {e}")