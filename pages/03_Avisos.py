
import streamlit as st
import sqlite3
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# Configuração
st.set_page_config(page_title="📬 Avisos de Retirada", layout="wide")
conn = sqlite3.connect("db/PratoDoDia.db", check_same_thread=False)
cursor = conn.cursor()

# Auto refresh a cada 10 segundos
st_autorefresh(interval=10000, key="refresh")


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

st.title("📬 Avisos de Retirada")

cursor.execute("SELECT DISTINCT cidade FROM avisos ORDER BY cidade")
cidades_disponiveis = [row[0] for row in cursor.fetchall()]

cidade = st.selectbox("Selecione a cidade para acompanhar as retiradas:", ["Escolher"] + cidades_disponiveis)

if cidade != "Escolher":
    cursor.execute("SELECT mensagem, criado_em FROM avisos WHERE cidade = ? ORDER BY criado_em DESC", (cidade,))
    avisos = cursor.fetchall()

    if not avisos:
        st.info("Nenhum aviso registrado recentemente para esta cidade.")
    else:
        for mensagem, criado_em in avisos:
            with st.container():
                st.markdown(f"""
                <div style='padding: 10px; border-radius: 10px; background-color: #fff3cd; border: 1px solid #ffeeba; margin-bottom: 10px;'>
                    <strong>📣 {mensagem}</strong><br>
                    <span style='font-size: 0.8em; color: gray;'>⏰ {criado_em}</span>
                </div>
                """, unsafe_allow_html=True)
else:
    st.warning("Selecione uma cidade para visualizar os avisos.")
