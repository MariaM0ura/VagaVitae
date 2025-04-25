
from services.extract_pdf import extract_text_from_pdf
from services.process_data import process_data

if __name__ == "__main__":
    path = "data/curriculo_exemplo.pdf"
    
    with open(path, "rb") as file:
        text = "texto extraido"
        text += extract_text_from_pdf(file)
    
    cv = ""

    cv += process_data(text)
    #print(cv)
    with open("output_cv.txt", "w", encoding="utf-8") as f:
        f.write(cv)
        
    print(" ############# Extração de texto e processamento concluídos. ############# ")

    