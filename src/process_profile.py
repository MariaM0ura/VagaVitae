
from .services.Profile.extract_pdf import extract_text_from_pdf
from .services.Profile.process_data import process_data

"""
This script extracts text from a CV file and processes it to create a structured CV.
"""
def result_profile(path_profile):
    with open(path_profile, "rb") as file:
        text = "texto extraido"
        text += extract_text_from_pdf(file)
    
    cv = ""

    cv += process_data(text)
    
    # with open("output_cv.txt", "w", encoding="utf-8") as f:
    #    f.write(cv)
        
    print(" ############# Extração de texto e curriculo concluídos. ############# ")

    return cv

