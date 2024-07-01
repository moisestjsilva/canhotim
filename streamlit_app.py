import streamlit as st
import os
import fitz  # PyMuPDF

def main():
    st.title('Aplicativo para Renomear e Salvar Arquivos')

    # Interface para selecionar arquivo PDF
    uploaded_file = st.file_uploader("Selecione um arquivo PDF:", type=['pdf'])

    if uploaded_file is not None:
        # Mostra informações do arquivo selecionado
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)

        # Interface para inserir o nome da pasta onde os arquivos serão salvos
        folder_name = st.text_input("Nome da pasta para salvar os arquivos:", "nome_da_pasta")

        if st.button("Salvar Arquivo"):
            try:
                # Cria a pasta se ela não existir
                save_folder = os.path.abspath(folder_name)  # Utiliza caminho absoluto
                os.makedirs(save_folder, exist_ok=True)

                # Renomeia o arquivo com informações extraídas usando PyMuPDF
                saved_file_path = save_pdf_with_info(uploaded_file, save_folder)

                if saved_file_path:
                    st.success(f"Arquivo salvo com sucesso em '{saved_file_path}' dentro da pasta '{folder_name}'.")
                else:
                    st.error("Falha ao salvar o arquivo.")
            except Exception as e:
                st.error(f"Erro ao salvar o arquivo: {str(e)}")

def save_pdf_with_info(uploaded_file, save_folder):
    try:
        # Salva o arquivo temporariamente
        with open(os.path.join(save_folder, uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Lê o conteúdo do PDF para extrair informações usando PyMuPDF
        doc = fitz.open(os.path.join(save_folder, uploaded_file.name))
        first_page_text = doc[0].get_text()

        # Procura pelo marcador "N°" no texto extraído
        start_index = first_page_text.find("N°")
        if start_index != -1:
            info = first_page_text[start_index + len("N°"):].strip().split()[0]

            # Constrói o nome do arquivo com base na informação extraída
            filename = f"documento_{info}.pdf"
            save_path = os.path.join(save_folder, filename)

            # Salva o arquivo renomeado
            doc.save(save_path)
            doc.close()

            # Remove o arquivo temporário
            os.remove(os.path.join(save_folder, uploaded_file.name))

            return save_path
        else:
            # Remove o arquivo temporário
            os.remove(os.path.join(save_folder, uploaded_file.name))
            return None
    except Exception as e:
        raise e

if __name__ == '__main__':
    main()
