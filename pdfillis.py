"""PDFillis module."""

import fitz
import streamlit as st


class PDFillis:
    """Defines the web interface and all PDF handling functions."""

    def __init__(self):
        self._selected_files = []
        st.set_page_config(page_title="PDFillis - Combinador de PDFs")
        st.title("PDFillis - Combinador de PDFs")

        if "selected_files" not in st.session_state:
            st.session_state.selected_files = []
        if "message" not in st.session_state:
            st.session_state.message = ""
            st.session_state.message_color = "blue"

    def run(self):
        """Run the Streamlit app."""
        # File uploader
        uploaded_files = st.file_uploader(
            "Escolher arquivos", type="pdf", accept_multiple_files=True
        )

        if st.button("Combinar PDFs", type="primary"):
            self.merge_pdf()

        # Display messages
        if st.session_state.message:
            if st.session_state.message_color == "red":
                st.error(st.session_state.message)
            elif st.session_state.message_color == "green":
                st.success(st.session_state.message)
            else:
                st.info(st.session_state.message)

    def merge_pdf(self):
        """Merge the selected PDFs into a single one."""
        if not st.session_state.selected_files:
            st.session_state.message = "Nenhum arquivo selecionado!"
            st.session_state.message_color = "red"
            return

        merged_pdf = fitz.open()

        try:
            for uploaded_file in st.session_state.selected_files:
                pdf_bytes = uploaded_file.read()
                pdf_document = fitz.open("pdf", pdf_bytes)
                merged_pdf.insert_pdf(pdf_document)
                pdf_document.close()

            merged_pdf_bytes = merged_pdf.write()
            merged_pdf.close()

            st.download_button(
                label="Download PDF Combinado",
                data=merged_pdf_bytes,
                file_name="merged_document.pdf",
                mime="application/pdf",
            )

            st.session_state.message = "Arquivos combinados com sucesso!"
            st.session_state.message_color = "green"

        except Exception as e:
            st.session_state.message = f"Erro ao combinar arquivos: {str(e)}"
            st.session_state.message_color = "red"
