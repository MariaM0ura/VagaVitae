# VagaVitae

## Visão Geral do Projeto
### O objetivo:

- Coletar dados do usuário: Informações como contato, cursos, experiências, habilidades, etc.
- Extrair requisitos da vaga: Analisar a descrição de uma vaga do LinkedIn para identificar habilidades, experiências e qualificações desejadas.
- Gerar um currículo personalizado: Usar NLP para alinhar o perfil do usuário aos requisitos da vaga, destacando as informações mais relevantes e formatando o currículo adequadamente.

- ## 🚀 Proposta

Facilitar o processo de candidatura a vagas de emprego, gerando currículos adaptados automaticamente para cada vaga, aumentando a **adequação do candidato** ao perfil exigido.

---
 
# 🧠 Resume Match AI - Geração de Currículos Personalizados com NLP

Este projeto utiliza **Processamento de Linguagem Natural (NLP)** para automatizar a criação de **currículos personalizados** a partir de **vagas de emprego extraídas da internet**. Ele combina técnicas de **web scraping**, **extração de informação** com **LLMs (Large Language Models)** e **formatação inteligente** de currículos.

## 🚀 Proposta

Facilitar o processo de candidatura a vagas de emprego, gerando currículos adaptados automaticamente para cada vaga, aumentando a **adequação do candidato** ao perfil exigido.

---

## 🔧 Tecnologias Utilizadas

- 🐍 **Python**
- 🌐 **Requests** e **BeautifulSoup** (Web Scraping)
- 🤖 **LangChain** + **OpenAI GPT-4o-mini** (NLP e geração de conteúdo)
- 📄 **PyMuPDF** (extração de conteúdo de PDFs)
- 📦 **pydantic** (validação de dados)
- 🧰 **Prompt Engineering**

---
### 📁  Estrutura Geral


```bash
resume-customizer/
├── data/                      # Arquivos de entrada e saida (ex.: dataset de teste)
├── src/                       # Código-fonte principal
├────── services/              # funções de extração         
│       ├── Job                    # Responsável por extrair os requisitos da vaga de emprego 
│       ├── Profile                # Responsável por extrair dados do perfil do usuário
│   ├──         # Faz a comparação entre habilidades do perfil e da vaga
│   ├── personalize_resume.py     # Gera o currículo personalizado com base nos dados processados
├── requirements.txt           # Lista de dependências do projeto (ex.: langchain, openai, etc.)
├── app.py                     # GUI 
├── README.md                  # Documentação e instruções de uso do projeto
```

---

