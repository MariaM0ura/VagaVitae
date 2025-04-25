from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
import os
from dotenv import load_dotenv

def prompt_text(text):
    try:
        llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.3)
    except Exception as e:
        return f"Erro ao configurar o LLM: {str(e)}"
    
    prompt = PromptTemplate(
        input_variables=["texto"],
        template="""
        Extraia as seguintes informações do texto do currículo fornecido:
        - Nome
        - Contato (e-mail, telefone, LinkedIn, etc.)
        - Formação (instituições, cursos, datas)
        - Experiências Profissionais (empresas, cargos, períodos, responsabilidades)
        - Habilidades (técnicas e interpessoais)
        
        Formate a saída como um texto claro e organizado, separando cada categoria.
        Texto do currículo: {texto}
        """
    )
    
    try:
        resultado = llm(prompt.format(texto=text))
        return resultado
    except Exception as e:
        return f"Erro ao processar com LangChain: {str(e)}"