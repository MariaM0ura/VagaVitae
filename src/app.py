import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

# Carregar chaves de API
load_dotenv()
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configurar a página
st.set_page_config(page_title="ResumeCraft", layout="wide")
st.title("ResumeCraft: Crie seu Currículo Personalizado")

# Layout com duas colunas
col1, col2 = st.columns([1, 1])

# Coluna 1: Entrada de dados
with col1:
    st.header("Insira seus Dados")
    nome = st.text_input("Nome Completo")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone")
    formacao = st.text_area("Formação (ex.: Ciência da Computação, USP, 2023)")
    experiencias = st.text_area("Experiências (ex.: Desenvolvedor Python, Tech Corp, 2021-2023)")
    habilidades = st.text_input("Habilidades (separadas por vírgula)")
    vaga_texto = st.text_area("Descrição da Vaga (copie do LinkedIn)")

    if st.button("Gerar Currículo"):
        # Dados do perfil
        perfil = f"Nome: {nome}; Contato: {email}, {telefone}; Formação: {formacao}; Experiências: {experiências}; Habilidades: {habilidades}"

        # Prompt para gerar currículo
        prompt_curriculo = PromptTemplate(
            input_variables=["perfil", "vaga"],
            template="Crie um currículo personalizado para a vaga ({vaga}) com base no perfil ({perfil}). Inclua seções: Informações de Contato, Resumo Profissional, Experiências, Formação, Habilidades."
        )
        curriculo = llm(prompt_curriculo.format(perfil=perfil, vaga=vaga_texto))

        # Armazenar currículo na sessão para visualização
        st.session_state.curriculo = curriculo

# Coluna 2: Visualização do currículo
with col2:
    st.header("Currículo Gerado")
    if "curriculo" in st.session_state:
        st.markdown(st.session_state.curriculo)
        # Botão para download (DOCX será adicionado depois)
        st.download_button(
            label="Baixar Currículo (TXT)",
            data=st.session_state.curriculo,
            file_name="curriculo.txt",
            mime="text/plain"
        )
    else:
        st.write("Insira os dados e clique em 'Gerar Currículo' para visualizar.")
