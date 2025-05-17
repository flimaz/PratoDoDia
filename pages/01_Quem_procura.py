import streamlit as st
import sqlite3
import google.generativeai as genai
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import re

# Configuração
st.set_page_config(page_title="Procurar Refeição", layout="wide")
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash")
conn = sqlite3.connect("db/PratoDoDia.db", check_same_thread=False)
cursor = conn.cursor()

@st.cache_data
def carregar_cidades():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return sorted([m["nome"] for m in resposta.json()])
    return []

cidades_brasil = carregar_cidades()

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

st.title("🔎 Procurar Refeição")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Preencha para solicitar")

    cidade = st.selectbox("Cidade", ["Escolher"] + cidades_brasil)
    if cidade == "Escolher":
        st.warning("Por favor, selecione uma cidade antes de continuar.")

    nome = st.text_input("Seu nome")
    descricao = st.text_area("O que você precisa?", placeholder="Ex: Preciso de 1 marmita para mim e meu filho.")

    if "id_oferta_escolhida" not in st.session_state:
        st.session_state.id_oferta_escolhida = None
    if "texto_ia_oferta" not in st.session_state:
        st.session_state.texto_ia_oferta = None

    if st.button("Buscar"):
        if not nome or not descricao:
            st.warning("Preencha todos os campos.")
        else:
            cursor.execute("SELECT id, nome, descricao FROM ofertas WHERE cidade = ?", (cidade,))
            resultados = cursor.fetchall()

            if resultados:
                dados_ofertas = [{"id": i, "nome": n, "descricao": d} for (i, n, d) in resultados]

                prompt = f"""
Você é um assistente solidário. Abaixo há um pedido de comida e algumas ofertas disponíveis na mesma cidade.
Escolha **uma oferta específica** que pareça adequada ao pedido.
Gere uma resposta empática e solidária (máx. 2 frases) incentivando a pessoa a aceitá-la.
Retorne também o ID da oferta escolhida no formato: [ID: X].

Pedido: {descricao}
Ofertas:
{dados_ofertas}
"""
                resposta = model.generate_content(prompt)
                texto_ia = resposta.text.strip()
                match = re.search(r"\[ID:\s*(\d+)\]", texto_ia)

                st.session_state.id_oferta_escolhida = int(match.group(1)) if match else None
                st.session_state.texto_ia_oferta = re.sub(r"\[ID:\s*\d+\]", "", texto_ia).strip()

            else:
                prompt = f"""
                Crie uma única frase objetiva para um pedido solidário de comida.
                Formato: [Cidade: {cidade}: {nome}] {nome} precisa de {descricao}.
                Use apenas essa estrutura e nada mais.
                """

                resposta = model.generate_content(prompt)
                resumo = resposta.text.strip()
                cursor.execute("INSERT INTO pedidos (cidade, nome, descricao, criado_em) VALUES (?, ?, ?, ?)",
                               (cidade, nome, resumo, datetime.now().isoformat()))
                conn.commit()
                st.markdown("### Pedido Registrado:")
                st.success("Seu pedido foi registrado com sucesso!")

    if st.session_state.texto_ia_oferta:
        st.markdown("### 🤖 Sugestão do Geronimi:")
        st.info(st.session_state.texto_ia_oferta)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Aceitar sugestão") and st.session_state.id_oferta_escolhida:
                id_escolhida = st.session_state.id_oferta_escolhida
                cursor.execute("SELECT nome, descricao FROM ofertas WHERE id = ?", (id_escolhida,))
                resultado = cursor.fetchone()

                if resultado:
                    doador, texto_oferta = resultado
                    cursor.execute("DELETE FROM ofertas WHERE id = ?", (id_escolhida,))
                    mensagem = f"{nome}, encontramos uma refeição para você! Por favor, retirar com {doador}: {texto_oferta}"
                    cursor.execute("INSERT INTO avisos (cidade, mensagem, criado_em) VALUES (?, ?, ?)",
                                   (cidade, mensagem, datetime.now().isoformat()))
                    conn.commit()
                    st.success("Uma oferta foi consumida. Esperamos que ajude!")
                    st.session_state.id_oferta_escolhida = None
                    st.session_state.texto_ia_oferta = None
                    st.rerun()
                else:
                    st.warning("A oferta sugerida não foi encontrada. Ela pode ter sido removida por outra pessoa.")

        with col_b:
            if st.button("❌ Recusar e registrar pedido"):
                prompt = f"""
                Crie uma única frase no formato abaixo, sem mensagens adicionais, sem parágrafos extras:

                Formato: [Cidade: {cidade}: {nome}] {nome} precisa de {descricao}.
                """
                resposta = model.generate_content(prompt)
                resumo = resposta.text.strip()

                cursor.execute("INSERT INTO pedidos (cidade, nome, descricao, criado_em) VALUES (?, ?, ?, ?)",
                               (cidade, nome, resumo, datetime.now().isoformat()))
                conn.commit()
                st.success("Pedido registrado com sucesso!")
                st.session_state.id_oferta_escolhida = None
                st.session_state.texto_ia_oferta = None

with col2:
    st.subheader("🍱 Refeições Disponíveis na sua cidade")
    st.markdown("<span style='color:red; font-size: 0.9em;'>Descreva o seu pedido ao lado para o nosso ajudante Geronimi encontrar a melhor combinação para você.</span>", unsafe_allow_html=True)
    if cidade:
        cursor.execute("SELECT id, nome, descricao FROM ofertas WHERE cidade = ? ORDER BY id DESC", (cidade,))
        resultados = cursor.fetchall()

        if not resultados:
            st.info("Nenhuma oferta encontrada na cidade no momento.")
        else:
            for id, nome, desc in resultados:
                st.markdown(f"📍{desc}")
