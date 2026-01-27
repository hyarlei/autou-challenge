# 📧 AutoU Email Triagem (AI Powered)

![Project Status](https://img.shields.io/badge/status-concluído-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![React](https://img.shields.io/badge/React-19-blue)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)

Uma solução inteligente para triagem automática de emails corporativos. O sistema utiliza Inteligência Artificial para ler, interpretar e classificar mensagens (incluindo anexos PDF e TXT) em "Produtivas" ou "Improdutivas", sugerindo respostas automáticas para otimizar o tempo da equipe.

---

## 🚀 Funcionalidades

- **Classificação Inteligente:** Analisa o sentimento e a intenção do email usando LLMs (Google Gemini)
- **Suporte a Arquivos:** Leitura e extração de texto de anexos `.pdf` e `.txt`
- **Sugestão de Resposta:** Gera automaticamente uma resposta polida e contextualizada
- **Interface Moderna:** UI limpa e responsiva desenvolvida com React e TailwindCSS

---

## 🛠️ Tecnologias Utilizadas

### Backend (API)

- **Linguagem:** Python 3.10+
- **Framework:** FastAPI (alta performance e assíncrono)
- **AI Model:** Google Gemini 2.5 Flash
- **PDF Processing:** PyPDF

### Frontend (UI)

- **Library:** React 19 (Vite)
- **Styling:** TailwindCSS v4
- **HTTP Client:** Axios
- **Icons:** Lucide React

---

## 📦 Como Rodar Localmente

### Pré-requisitos

- Python 3.10+
- Node.js e NPM
- Uma chave de API do Google Gemini (gratuita no [AI Studio](https://aistudio.google.com))

### 1️⃣ Configurando o Backend

```bash
cd backend
```

**Criar e ativar o ambiente virtual:**

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

**Instalar dependências:**

```bash
pip install -r requirements.txt
```

**Configurar variáveis de ambiente:**

Crie um arquivo `.env` na pasta `backend` com:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

**Rodar o servidor:**

```bash
uvicorn main:app --reload
```

Backend rodará em: `http://127.0.0.1:8000`

### 2️⃣ Configurando o Frontend

```bash
cd frontend
```

**Instalar dependências:**

```bash
npm install
```

**Rodar a aplicação:**

```bash
npm run dev
```

Acesse no navegador: `http://localhost:5173`

---

## 🧠 Decisões Arquiteturais

**FastAPI no Backend:** Escolhido pela velocidade de desenvolvimento, validação automática de dados (Pydantic) e suporte nativo a processamento assíncrono, ideal para chamadas de IA.

**Google Gemini:** Optei pelo modelo Gemini 2.5 Flash por ser extremamente rápido e eficiente (custo-benefício) para tarefas de classificação de texto em comparação a modelos maiores.

**TailwindCSS v4:** Para garantir uma interface limpa, responsiva e com desenvolvimento ágil, simulando um produto SaaS real.

---

## 📝 Licença

Este projeto foi desenvolvido como parte do processo seletivo da AutoU.
