import io
import json
import os

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader

# Carrega as variáveis de ambiente
load_dotenv()

# Configura a API do Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Configura CORS para comunicação com o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    content: str

@app.post("/")
@app.post("/analyze")
async def analyze_email(request: EmailRequest):
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')

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

        response = model.generate_content(prompt)
        
        # Remove markdown formatting se presente
        cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
        
        data = json.loads(cleaned_response)

        return data

    except json.JSONDecodeError:
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
        
        if file.filename.endswith(".pdf"):
            pdf_bytes = await file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                content += page.extract_text() + "\n"
                
        elif file.filename.endswith(".txt"):
            content = (await file.read()).decode("utf-8")
            
        else:
            return {"category": "Erro", "response": "Formato não suportado. Use PDF ou TXT."}

        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Limita o conteúdo para evitar exceder o limite de tokens
        prompt = f"""
        Atue como um classificador de emails corporativos especializado.
        Analise o texto abaixo e retorne APENAS um JSON com "category" (Produtivo/Improdutivo) e "response".
        
        Conteúdo do arquivo:
        "{content[:5000]}"
        """
        
        response = model.generate_content(prompt)
        cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)

    except Exception as e:
        return {"category": "Erro", "response": f"Falha ao ler arquivo: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "API Online 🚀"}