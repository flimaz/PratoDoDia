import streamlit as st
import sqlite3
import google.generativeai as genai
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import re
import time

# Configuração
st.set_page_config(page_title="Oferecer Refeição", layout="wide")
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash")
conn = sqlite3.connect("db/PratoDoDia.db", check_same_thread=False)
cursor = conn.cursor()

# Carrega cidades do IBGE
@st.cache_data
def carregar_cidades():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        cidades = sorted([m["nome"] for m in resposta.json()])
        return cidades
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

st.title("📢 Oferecer Refeição")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Preencha para doar")

    cidade = st.selectbox("Cidade", ["Escolher"] + cidades_brasil)

    if cidade == "Escolher":
        st.warning("Por favor, selecione uma cidade antes de continuar.")

    nome = st.text_input("Seu nome ou do estabelecimento")
    descricao = st.text_area("O que está oferecendo?", placeholder="Ex: Tenho 2 marmitas com arroz, feijão e legumes. Informe também o local para retirada.")

    if "id_escolhido" not in st.session_state:
        st.session_state.id_escolhido = None
    if "texto_ia" not in st.session_state:
        st.session_state.texto_ia = None

    if st.button("Buscar"):
        if not nome or not descricao:
            st.warning("Preencha todos os campos.")
        else:
            if len(descricao.strip().split()) < 5:
                st.warning("Descreva melhor a comida oferecida e o local de retirada, por favor.")
            else:
                cursor.execute("SELECT id, nome, descricao FROM pedidos WHERE cidade = ?", (cidade,))
                resultados = cursor.fetchall()

                if resultados:
                    dados_pedidos = [{"id": i, "nome": n, "descricao": d} for (i, n, d) in resultados]

                    prompt = f"""
Você é um assistente solidário. Abaixo há uma oferta de comida e alguns pedidos na mesma cidade.
Escolha **uma pessoa específica** que pareça mais urgente ou compatível e sugira ajudar ela.
Inclua o nome e o pedido na resposta (máx. 2 frases).
Retorne também o ID da pessoa escolhida no formato: [ID: X].

Oferta: {descricao}
Pedidos:
{dados_pedidos}
"""
                    resposta = model.generate_content(prompt)
                    texto_ia = resposta.text.strip()

                    match = re.search(r"\[ID:\s*(\d+)\]", texto_ia)
                    st.session_state.id_escolhido = int(match.group(1)) if match else None
                    st.session_state.texto_ia = re.sub(r"\[ID:\s*\d+\]", "", texto_ia).strip()
                else:
                    prompt = f"""
Você é um assistente solidário. Avalie a descrição abaixo enviada por uma pessoa oferecendo comida.

Confirme se ela menciona:
1. O que está sendo oferecido (ex: marmita, lanche, frutas);
2. Um local de retirada, que pode ser:
   - um endereço (com ou sem número);
   - um ponto de referência claro (ex: em frente à igreja, no mercado X, perto da escola Y).

Se ambas as informações estiverem presentes, gere uma descrição empática no formato:
[Cidade: X] Fulano está oferecendo Y, retirar [no local informado na mensagem].

Caso contrário, diga:
"A descrição está incompleta. Por favor, informe o que está oferecendo e o local de retirada com mais detalhes."

Nome: {nome}
Cidade: {cidade}
Oferta: {descricao}
"""
                    resposta = model.generate_content(prompt)
                    resumo = resposta.text.strip()

                    if "A descrição está incompleta" in resumo:
                        st.warning("A descrição está incompleta. Por favor, informe o que está oferecendo e o local de retirada com mais detalhes.")
                    else:
                        cursor.execute("INSERT INTO ofertas (cidade, nome, descricao, criado_em) VALUES (?, ?, ?, ?)",
                                       (cidade, nome, resumo, datetime.now().isoformat()))
                        conn.commit()
                        st.success("Nenhum pedido encontrado. Sua oferta foi registrada com sucesso!")

    if st.session_state.texto_ia:
        st.markdown("### 🤖 Sugestão do Geronimi:")
        st.info(st.session_state.texto_ia)
        # Registro automático se a IA disser que não pode ajudar
        if "não posso ajudar" in st.session_state.texto_ia.lower():
            st.warning("O Geronimi não encontrou alguém compatível, mas sua oferta será publicada.")
            cursor.execute("INSERT INTO ofertas (cidade, nome, descricao, criado_em) VALUES (?, ?, ?, ?)",
                        (cidade, nome, descricao, datetime.now().isoformat()))
            conn.commit()
            st.success("Oferta registrada com sucesso!")
            st.session_state.id_escolhido = None
            st.session_state.texto_ia = None
            st.sleep(1)
            st.rerun()


        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ Quero atender essa pessoa") and st.session_state.id_escolhido:
                id_escolhido = st.session_state.id_escolhido
                cursor.execute("SELECT COUNT(*) FROM pedidos WHERE id = ?", (id_escolhido,))
                existe = cursor.fetchone()[0]

                if existe:
                    # Obter nome e descrição do pedido antes de excluir
                    cursor.execute("SELECT nome, descricao FROM pedidos WHERE id = ?", (id_escolhido,))
                    resultado_pedido = cursor.fetchone()

                    if resultado_pedido:
                        nome_pedido, texto_pedido = resultado_pedido
                        mensagem = f"{nome_pedido}, encontramos uma refeição para você! Por favor, retirar com {nome}: {descricao}"
                        cursor.execute("INSERT INTO avisos (cidade, mensagem, criado_em) VALUES (?, ?, ?)",
                                    (cidade, mensagem, datetime.now().isoformat()))

                    cursor.execute("DELETE FROM pedidos WHERE id = ?", (id_escolhido,))
                    time.sleep(0.2)
                    conn.commit()
                    time.sleep(0.2)
                    st.success("Pedido atendido com sua oferta. Obrigado por ajudar!")
                    time.sleep(0.5)
                    st.session_state.id_escolhido = None
                    st.session_state.texto_ia = None
                    st.rerun()

                else:
                    st.warning("⚠️ O pedido indicado pela IA não foi encontrado. Talvez ele já tenha sido atendido.")

        with col_b:
            if st.button("❌ Não, registrar como nova oferta"):
                prompt = f"""
Crie uma descrição empática para uma doação de comida. Máximo 2 frases.

Nome: {nome}
Cidade: {cidade}
Oferta: {descricao}
Formato: [Cidade: X] Fulano está oferecendo Y.
"""
                resposta = model.generate_content(prompt)
                resumo = resposta.text.strip()

                cursor.execute("INSERT INTO ofertas (cidade, nome, descricao, criado_em) VALUES (?, ?, ?, ?)",
                               (cidade, nome, resumo, datetime.now().isoformat()))
                conn.commit()
                st.success("Oferta registrada com sucesso!")
                st.session_state.id_escolhido = None
                st.session_state.texto_ia = None

    elif not st.session_state.texto_ia and not descricao:
        st.info("Preencha os campos e clique em Buscar para que o Geronimi o ajude.")

with col2:
    st.subheader("🙋 Refeições Registradas na sua Cidade")
    st.markdown("<span style='color:red; font-size: 0.9em;'>Descreva sua doação ao lado para que o Geronimi encontre uma pessoa para ser ajudada.</span>", unsafe_allow_html=True)
    if cidade:
        cursor.execute("SELECT id, nome, descricao FROM pedidos WHERE cidade = ? ORDER BY id DESC", (cidade,))
        resultados = cursor.fetchall()

        if not resultados:
            st.info("Nenhum pedido encontrado na cidade no momento.")
        else:
            for id, nome, desc in resultados:
                st.markdown(f"📍{desc}")
