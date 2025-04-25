import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from .prompt_templates import prompt_text

def process_data(file=None):
    if not file:
        return "Nenhum arquivo fornecido para processamento."
    
    result = ""
    
    print(" ############# Iniciando LLM. ############# ")

    text = prompt_text(file)
    if isinstance(text, str) and text.startswith("Erro"):

        return text
    
    if text:
        #result += "Texto bruto extraído do PDF:\n"
        result += text
        result += "\n\n"
        
        try:
            extracted_info = prompt_text(text)
            #result += "Informações extraídas com LangChain:\n"
            result += extracted_info
            
            #lines = extracted_info.split("\n")
            #df = pd.DataFrame(lines, columns=["Conteúdo"])
            #result += f"\n\nDados em formato DataFrame:\n{df.to_string()}\n"
            
        except Exception as e:
            result += f"Erro ao processar com LangChain: {str(e)}"
    else:
        result += "Nenhum texto encontrado no PDF."

    print(" ############# Processamento concluído. ############# ")
    
    return result




    