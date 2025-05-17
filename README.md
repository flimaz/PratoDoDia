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

O Geronimi é o assistente inteligente do projeto, baseado no modelo Gemini 2.0 Flash. Ele atua como uma ponte solidária entre quem precisa e quem oferece comida, analisando os dados e sugerindo as melhores conexões possíveis com empatia e rapidez.

Funcionalidades principais do Geronimi:
- 🤖 Sugestões automáticas de combinação: avalia pedidos e ofertas e sugere a melhor combinação com base na descrição e na cidade.

- 🔍 Validação de ofertas: antes de permitir que uma oferta seja publicada, o Geronimi analisa se ela contém:

- O tipo de comida oferecida.

- Um local claro e seguro de retirada.

- ⛔ Bloqueio de publicações incompletas: se a descrição não estiver adequada, a publicação não é permitida até ser corrigida.

- 🤝 Mensagem personalizada de match: quando há compatibilidade, ele gera uma frase personalizada para incentivar a doação.

- 📝 Geração automática de registros: caso não haja combinações no momento, o pedido ou oferta é salvo de forma clara e padronizada.

O Geronimi foi projetado para atuar com empatia, acessibilidade e agilidade, criando uma experiência simples e humana no processo de ajudar o próximo.

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
cd PratoDoDia
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

### 📸 Capturas de Tela

#### 🏠 Tela Inicial (Desktop)
![Tela Inicial](https://github.com/flimaz/PratoDoDia/blob/main/img/TelaInicial_Desktop.png?raw=true)

#### 🔎 Página de Busca (Desktop)
![Buscar Refeição](https://github.com/flimaz/PratoDoDia/blob/main/img/Buscar_Desktop.png?raw=true)

#### 📢 Página de Oferta (Mobile)
![Oferecer Refeição](https://github.com/flimaz/PratoDoDia/blob/main/img/Oferecer_Mobile.png?raw=true)

#### 📬 Avisos de Retirada (Mobile)
![Avisos de Retirada](https://github.com/flimaz/PratoDoDia/blob/main/img/AvisosRetirada_Mobile.png?raw=true)

#### 💡 Sugestão Gerada pela IA
![Sugestão da IA](https://github.com/flimaz/PratoDoDia/blob/main/img/SugestaoParecida.png?raw=true)

---

## 🙌 Contribuições

Contribuições são bem-vindas! Você pode abrir uma issue ou enviar um pull request com melhorias, correções ou novas ideias.

---

## ❤️ Agradecimentos

Projeto idealizado com foco em empatia, comida e tecnologia. Que possamos espalhar mais solidariedade pelo mundo!