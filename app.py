import streamlit as st

st.title("VagaVitae")

st.write("Crie um currículo personalizado para a vaga que você deseja!")
st.write("Preencha os campos abaixo para gerar um currículo adaptado à vaga desejada.")


link_vaga = st.text_input("Insira o link da vaga:", placeholder="https://www.linkedin.com/jobs/view/<job_id>")

# Campo para upload do PDF
pdf_file = st.file_uploader("Faça upload do seu curriculo:", type=["pdf"])

# Botão para enviar
if st.button("Produzir Currículo Personalizado"):
    if link_vaga and pdf_file:
        st.success("Link e PDF recebidos com sucesso!")
        st.write(f"**Link da vaga:** {link_vaga}")
        st.write(f"**Arquivo PDF:** {pdf_file.name}")
    else:
        st.error("Por favor, insira o link da vaga e faça upload do PDF.")

