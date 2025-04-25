from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

def extract_job_requirements(vaga_texto, llm):
    prompt = PromptTemplate(
        input_variables=["vaga"],
        template="Extraia habilidades, experiência mínima e formação da descrição: {vaga}"
    )
    resultado = llm(prompt.format(vaga=vaga_texto))
    return resultado

if __name__ == "__main__":
    # Carregar chave de API do .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Erro: OPENAI_API_KEY não encontrada no arquivo .env")
        exit(1)

    # Configurar o LLM
    llm = OpenAI(api_key=api_key)

    # Ler o arquivo vaga_exemplo.txt
    try:
        with open("data/vaga_exemplo.txt", "r", encoding="utf-8") as file:
            vaga_texto = file.read()
    except FileNotFoundError:
        print("Erro: Arquivo data/vaga_exemplo.txt não encontrado")
        exit(1)

    # Executar a extração
    resultado = extract_job_requirements(vaga_texto, llm)
    print("Resultado da Extração:")
    print(resultado)


if __name__ == "__main__":
    # Carregar chave de API do .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Erro: OPENAI_API_KEY não encontrada no arquivo .env")
        exit(1)

    llm = OpenAI(api_key=api_key)

    try:
        with open("data/vaga_exemplo.pdf", "r", encoding="utf-8") as file:
            vaga_texto = file.read()
    except FileNotFoundError:
        print("Erro: Arquivo data/vaga_exemplo.txt não encontrado")
        exit(1)

    resultado = extract_job_requirements(vaga_texto, llm)
    print("Resultado da Extração:")
    print(resultado)