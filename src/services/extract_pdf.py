
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader


def extract_text_from_pdf(file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file.read())
            tmp_file_path = tmp_file.name
        
        loader = PyPDFLoader(tmp_file_path)
        documents = loader.load()
        
        text = "\n".join([doc.page_content for doc in documents])
        
        os.unlink(tmp_file_path)
        print(" ############# Texto extraído do PDF com sucesso. ############# ")
        #print(f": {text[:100]}...")  # Exibe os primeiros 100 caracteres do texto extraído
        
        return text
    except Exception as e:
        return f"Erro ao extrair texto do PDF: {str(e)}"