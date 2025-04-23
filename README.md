# VagaVitae

## Visão Geral do Projeto
### O objetivo:

- Coletar dados do usuário: Informações como contato, cursos, experiências, habilidades, etc.
- Extrair requisitos da vaga: Analisar a descrição de uma vaga do LinkedIn para identificar habilidades, experiências e qualificações desejadas.
- Gerar um currículo personalizado: Usar NLP para alinhar o perfil do usuário aos requisitos da vaga, destacando as informações mais relevantes e formatando o currículo adequadamente.


### Tecnologias 
- LangChain :
  - Extração de informações: Processar textos não estruturados (perfil do usuário e descrição da vaga) e extrair informações relevantes.
  - Comparação e ranqueamento: Avaliar a compatibilidade entre o perfil do usuário e os requisitos da vaga.
  - Geração de texto: Criar um currículo bem redigido e adaptado à vaga, usando prompts personalizados e LLMs.
 
    
 

### 📁 Estrutura do Projeto

```bash
resume-customizer/
├── data/                   # Arquivos de entrada (ex.: dataset de teste)
├── src/                    # Código-fonte principal
│   ├── extract_profile.py     # Responsável por extrair dados do perfil do usuário
│   ├── extract_job.py         # Responsável por extrair os requisitos da vaga de emprego
│   ├── match_skills.py        # Faz a comparação entre habilidades do perfil e da vaga
│   ├── generate_resume.py     # Gera o currículo personalizado com base nos dados processados
├── requirements.txt        # Lista de dependências do projeto (ex.: langchain, openai, etc.)
├── README.md               # Documentação e instruções de uso do projeto
```

---

