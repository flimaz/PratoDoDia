import streamlit as st
from init_db import init_db

# Inicializa banco ao abrir o app
init_db()

st.set_page_config(page_title="Início", page_icon="🍽️", layout="wide")

hide_menu_style = """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebarNav"] > ul {
            display: none;
        }
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.sidebar.title("🍽️ Navegação")
st.sidebar.markdown("Use o menu abaixo para acessar as funções:")
st.sidebar.page_link("app.py", label="🏠 Início")
st.sidebar.page_link("pages/01_Quem_procura.py", label="🔎 Buscar Refeição")
st.sidebar.page_link("pages/02_Quem_oferece.py", label="📢 Oferecer Refeição")
st.sidebar.page_link("pages/03_Avisos.py", label="📬 Avisos de Retirada")



st.title("Bem-vindo ao PratoDoDia")
st.markdown("Este é um projeto solidário para conectar quem precisa de comida com quem pode oferecer.")
st.info("Use o menu lateral para navegar entre as páginas de solicitação ou doação.")

st.markdown("## 👨‍🍳 Como funciona o sistema 'Prato do Dia' com ajuda do Geronimi")

st.markdown("""
**🧠 Geronimi** é a inteligência artificial do projeto baseado no Gemini da Google ✨. Ele conecta quem precisa de uma refeição com quem tem comida para doar.

### 👉 Para quem **precisa de comida**:
1. Acesse a aba **🔎 Buscar Refeição**;
2. Preencha seu nome, cidade e descreva sua necessidade;
3. O **Geronimi** tentará encontrar uma oferta compatível;
4. Se encontrar, ele sugere a retirada diretamente;
5. Se não houver oferta, seu pedido será registrado e aguardará um doador.

### 👉 Para quem **deseja doar**:
1. Acesse a aba **📢 Oferecer Refeição**;
2. Preencha seu nome, cidade, o que está oferecendo e onde será a retirada;
3. O **Geronimi** tentará encontrar alguém que esteja precisando;
4. Se houver compatibilidade, ele sugere quem você pode ajudar;
5. Se não houver, sua oferta será registrada e ficará disponível no sistema.

### 📬 Acompanhar retiradas:
- Vá até a aba **📬 Avisos de Retirada**;
- Veja se seu pedido foi atendido, e informações de retirada em tempo real!
""")




