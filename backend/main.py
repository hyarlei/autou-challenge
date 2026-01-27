import os
import json
import io
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader

# Carrega as variáveis de ambiente
load_dotenv()

# Configura a API do Google (pegue sua chave no Google AI Studio)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Configura CORS (para o seu Frontend React conversar com o Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Na produção, mude para o domínio do seu site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados que vai vir do Frontend
class EmailRequest(BaseModel):
    content: str

@app.post("/analyze")
async def analyze_email(request: EmailRequest):
    try:
        # Configura o modelo (o flash é mais rápido e barato/grátis)
        model = genai.GenerativeModel('models/gemini-2.5-flash')

        # O Prompt Mágico (Aqui está o segredo do sucesso)
        prompt = f"""
        Atue como um classificador de emails corporativos especializado.
        Analise o texto abaixo e retorne APENAS um JSON (sem markdown, sem aspas extras) com dois campos:
        1. "category": Deve ser exatamente "Produtivo" ou "Improdutivo".
        2. "response": Uma sugestão de resposta curta e polida para o remetente.

        Email para análise:
        "{request.content}"
        
        Exemplos de classificação:
        - "Solicito orçamento", "Erro no sistema" -> Produtivo
        - "Feliz Natal", "Obrigado", "Bom dia" -> Improdutivo
        """

        # Gera a resposta
        response = model.generate_content(prompt)
        
        # Limpeza básica caso a IA mande ```json no começo
        cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
        
        # Transforma o texto em Dicionário Python
        data = json.loads(cleaned_response)

        return data

    except json.JSONDecodeError:
        # Fallback caso a IA não retorne um JSON perfeito
        return {
            "category": "Indefinido",
            "response": "Não foi possível processar a resposta da IA. Tente novamente."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    try:
        content = ""
        
        # Se for PDF
        if file.filename.endswith(".pdf"):
            # Lê o arquivo da memória
            pdf_bytes = await file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_file)
            # Extrai texto de todas as páginas
            for page in reader.pages:
                content += page.extract_text() + "\n"
                
        # Se for TXT
        elif file.filename.endswith(".txt"):
            content = (await file.read()).decode("utf-8")
            
        else:
            return {"category": "Erro", "response": "Formato não suportado. Use PDF ou TXT."}

        # Reutiliza a lógica da IA (sem repetir código!)
        # Aqui chamamos direto o modelo com o texto extraído
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        prompt = f"""
        Atue como um classificador de emails corporativos especializado.
        Analise o texto abaixo e retorne APENAS um JSON com "category" (Produtivo/Improdutivo) e "response".
        
        Conteúdo do arquivo:
        "{content[:5000]}"  # Limitamos a 5000 caracteres para não estourar tokens
        """
        
        response = model.generate_content(prompt)
        cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)

    except Exception as e:
        return {"category": "Erro", "response": f"Falha ao ler arquivo: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "API Online 🚀"}