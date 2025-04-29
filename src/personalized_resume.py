import json
import os
from dotenv import load_dotenv


from langchain.prompts import PromptTemplate

from langchain_core.output_parsers.string import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from src.process_job import job_info
from src.process_profile import result_profile
from src.services.Profile.cv_pdf_processed import generate_resume_pdf


from pathlib import Path
import uuid



load_dotenv()


class ResumeOutput(BaseModel):
    personalized_resume: dict = Field(description="Resumo personalizado contendo experiências e habilidades")
    match_metric: float = Field(description="Percentual de adequação à vaga")
    requirements: list = Field(description="Lista de requisitos da vaga")
    matched_requirements: list = Field(description="Requisitos atendidos pelo candidato")

def create_personalized_resume(job, cv):
    """
    Cria um currículo personalizado com base nos requisitos da vaga..
    """
    # Configuração do LLM (exemplo usando OpenAI)
    llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.3
        )

    # Extrair requisitos da vaga
    job_data = job.get("data", {}) if isinstance(job, dict) else {}
    if not job_data:
        return {
            "status": "error",
            "message": "Nenhum dado de vaga encontrado.",
            "personalized_resume": {"experiences": [], "skills": []},
            "match_metric": 0.0,
            "requirements": [],
            "matched_requirements": []
        }

    parser = JsonOutputParser(pydantic_object=ResumeOutput)

    prompt_template = PromptTemplate(
        input_variables=["cv_text", "job_info"],
        template="""
        Você é um especialista em recrutamento. Sua tarefa é criar um currículo personalizado com base nos requisitos de uma vaga de emprego.

        **Instruções:**
        1. Analise as informações da vaga fornecidas em `job_info` e identifique os requisitos (habilidades técnicas, experiências profissionais, certificações, etc.).
        2. A partir do texto do currículo em `cv_text`, selecione SOMENTE as experiências profissionais, habilidades e certificações que correspondem diretamente aos requisitos da vaga. Ignore informações irrelevantes. Se nenhuma experiência for relevante, selecione apenas uma experiência mais próxima, selecione pelo menos 5 habilidades e mais importantes se houver.
        3. Crie um **Resumo Profissional** de até 3 linhas sobre o candidato, baseado no currículo e alinhado ao perfil da vaga.
        4. Crie um **Objetivo Profissional**, uma pequena frase sobre o interesse do candidato em conquistar a vaga.
        5. Estruture o currículo personalizado como um JSON, com os seguintes campos:
            - `contact`: informações de contato (nome, email, LinkedIn).
            - `academic_background`: formação acadêmica (curso, instituição, ano).
            - `certifications`: lista de certificações relevantes.
            - `experiences`: lista de experiências relevantes (empresa, cargo, duração, descrição curta de até 50 palavras).
            - `skills`: lista de habilidades técnicas relevantes.
            - `professional_summary`: texto breve de resumo sobre o candidato.
            - `career_objective`: frase sobre o objetivo do candidato relacionado à vaga.
        6. Liste todos os requisitos identificados na vaga.
        7. Liste todos os requisitos identificados na vaga.
        8. Liste os requisitos atendidos pelo currículo.
        9. Calcule a métrica de adequação como a porcentagem de requisitos atendidos (ex.: 3 de 4 = 75%).

        **Entrada:**
        - Texto do currículo: {cv_text}
        - Informações da vaga: {job_info}

        **Saída (JSON):**
        ```json
        {{
            "personalized_resume": {{
                "contact": {{
                    "name": "string",
                    "email": "string",
                    "linkedin": "string"
                }},
                "academic_background": {{
                    "degree": "string",
                    "institution": "string",
                    "year": "string"
                }},
                "certifications": ["string"],
                "experiences": [
                    {{
                        "company": "string",
                        "role": "string",
                        "duration": "string",
                        "description": "string"
                    }}
                ],
                "skills": ["string"],
                "professional_summary": "string",
                "career_objective": "string"
            }},
            "match_metric": 0.0,
            "requirements": ["string"],
            "matched_requirements": ["string"]
        }}
        ```
        """,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )


    chain = prompt_template | llm | parser

    try:
        job_info_str = json.dumps(job["data"], ensure_ascii=False) 

        result = chain.invoke({"job_info": job_info_str, "cv_text":cv})

        result["match_metric"] = str(result["match_metric"]) + "%"
        result["status"] = "success"

        # print(f"############# Currículo personalizado gerado com sucesso. #############")
        print(result)
        return result

    except Exception as e:
        return {
        "error": f"Erro ao processar o currículo: {str(e)}",
        "personalized_resume": {"experiences": [], "skills": []},
        "match_metric": 0.0,
        "requirements": [],
        "matched_requirements": []
        }
    

def process(cv_path, job_url):

    # Extrair informações da vaga
    try:
        
        result_job = job_info(job_url)
        
        if result_job["status"] not in ["success_raw", "success_structured"]:
            print(f"Erro ao extrair vaga: {result_job['message']}")

    except Exception as e:
        print(f"Erro ao processar a vaga: {str(e)}")
        exit()

    # Extrair informações do Currículo
    try:
        cv = result_profile(f'data/{cv_path}.pdf')
    except Exception as e:
        print(f"Erro ao processar o currículo: {str(e)}")
        exit()

    # Criar currículo personalizado
    result = create_personalized_resume(result_job, cv)

    if "error" not in result:
        # Generate PDF
        output_pdf = 'data/'f"resume_{str(uuid.uuid4())[:8]}.pdf"
        generate_resume_pdf(result, str(output_pdf))
        print(f"############# Currículo personalizado gerado com sucesso. #############\n")
        
        return {
            "status": "success",
            "pdf_path": str(output_pdf),
            "result": result
        }


    if os.path.exists(cv_path):
        file_path = f'/data/{str(uuid.uuid4())}.pdf'
        os.remove(file_path)
    
    