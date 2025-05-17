# 🥣 Prato do Dia – Sistema de Doações de Refeições com IA

Bem-vindo ao **Prato do Dia**, uma plataforma solidária que conecta pessoas que precisam de refeições com doadores dispostos a compartilhar um prato de comida. Este projeto utiliza **Streamlit** e **Gemini AI (apelidado de Geronimi)** para sugerir automaticamente as melhores combinações entre ofertas e pedidos.

## 🧭 Contexto do Projeto
O Prato do Dia foi desenvolvido como parte do desafio proposto durante a Imersão de IA com o Google Gemini, promovida pela Alura em parceria com o Google durante a edição de 2025.

A proposta era criar uma aplicação prática utilizando o poder dos modelos generativos da família Gemini, com foco em resolver problemas reais de forma empática e acessível. Assim nasceu o Geronimi, o assistente solidário do nosso projeto, que ajuda a conectar refeições com quem mais precisa.

## ✨ Funcionalidades

- 🔎 Buscar refeição (para quem precisa de comida)
- 📢 Oferecer refeição (para quem deseja doar)
- 📬 Acompanhar avisos de retirada (ver quem está sendo ajudado em tempo real)
- ⚡ Sugestões automáticas de combinação por IA (Geronimi)
- 🧠 IA integrada com Google Gemini (gemini-2.0-flash)
- 🔁 Atualização automática de avisos a cada 10 segundos

## 🧠 Sobre o Geronimi

O **Geronimi** é nosso assistente inteligente. Ele analisa as descrições inseridas por quem está oferecendo ou pedindo uma refeição e faz sugestões automáticas de quem pode ajudar quem.

Exemplo:
> Sugiro ajudar João, pois ele precisa de arroz e você tem uma marmita com arroz.

Se não houver compatibilidade, a IA informa e a oferta ou pedido é salvo para futuras correspondências.

---

## 🚀 Tecnologias utilizadas

- Python 
- Streamlit
- SQLite
- Google Generative AI (Gemini)
- dotenv
- requests
- streamlit-autorefresh

---

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/flimaz/PratoDoDia
cd prato-do-dia
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` com sua chave de API Gemini:
```
GOOGLE_API_KEY=sua_chave_aqui
```

5. Inicie o projeto:
```bash
streamlit run app.py
```

---

## 📂 Estrutura do Projeto

```
├── app.py                 # Página inicial com explicação
├── init_db.py            # Script para criação de tabelas SQLite
├── db/                   # Pasta onde o banco .db é salvo
├── pages/
│   ├── 01_Quem_procura.py
│   ├── 02_Quem_oferece.py
│   └── 03_Avisos.py
├── .env                  # Chave da API Gemini (não subir para o Git)
├── requirements.txt
└── README.md
```

---

## 🙌 Contribuições

Contribuições são bem-vindas! Você pode abrir uma issue ou enviar um pull request com melhorias, correções ou novas ideias.

---

## ❤️ Agradecimentos

Projeto idealizado com foco em empatia, comida e tecnologia. Que possamos espalhar mais solidariedade pelo mundo!