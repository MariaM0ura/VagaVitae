from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

def extract_profile(texto, llm):
    prompt = PromptTemplate(
        input_variables=["texto"],
        template="Extraia nome, contato, formação, experiências e habilidades do texto: {texto}"
    )
    resultado = llm(prompt.format(texto=texto))
    return resultado