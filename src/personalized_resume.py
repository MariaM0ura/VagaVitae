import json
import os
from dotenv import load_dotenv


from langchain.prompts import PromptTemplate
# StrOutputParser
from langchain_core.output_parsers.string import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from process_job import job_info
from process_profile import result_profile

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
        2. A partir do texto do currículo em `cv_text`, selecione SOMENTE as experiências profissionais e habilidades que correspondem diretamente aos requisitos da vaga. Ignore informações irrelevantes.
        3. Estruture o currículo personalizado como uma lista JSON com dois campos: `experiences` (lista de experiências relevantes) e `skills` (lista de habilidades relevantes).
        4. Cada experiência deve conter: `company` (empresa), `role` (cargo), `duration` (duração, ex.: "2020-2022") e `description` (descrição curta, máx. 50 palavras).
        5. Cada habilidade deve ser uma string (ex.: "Python", "Gestão de Projetos").
        6. Liste todos os requisitos identificados na vaga.
        7. Liste os requisitos atendidos pelo currículo.
        8. Calcule a métrica de adequação como a porcentagem de requisitos atendidos (ex.: 3 de 4 = 75%).

        **Entrada:**
        - Texto do currículo: {cv_text}
        - Informações da vaga: {job_info}

        **Saída (JSON):**
        ```json
        {{
        "personalized_resume": {{
            "experiences": [
            {{"company": "string", "role": "string", "duration": "string", "description": "string"}}
            ],
            "skills": ["string"]
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

        print(f"Currículo personalizado gerado com sucesso.")

        return result

    except Exception as e:
        return {
        "error": f"Erro ao processar o currículo: {str(e)}",
        "personalized_resume": {"experiences": [], "skills": []},
        "match_metric": 0.0,
        "requirements": [],
        "matched_requirements": []
        }
    




# Exemplo de uso com o código fornecido
if __name__ == "__main__":
    # Exemplo de dados da vaga
    job_url = "https://www.linkedin.com/jobs/view/4181438889"
    path = "data/tales_resume_simplified.pdf"

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
        cv = result_profile(path)
    except Exception as e:
        print(f"Erro ao processar o currículo: {str(e)}")
        exit()

    # Criar currículo personalizado
    result = create_personalized_resume(result_job, cv)

    # Exibir resultado
    print("Currículo Personalizado:")
    print(json.dumps(result, indent=2, ensure_ascii=False))