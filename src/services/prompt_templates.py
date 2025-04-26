from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser
import os

def prompt_text(text):
    try:
        llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.3)
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
        chain = prompt | llm | StrOutputParser()
        resultado = chain.invoke({"texto": text})

        return resultado
    except Exception as e:
        return f"Erro ao processar com LangChain: {str(e)}"