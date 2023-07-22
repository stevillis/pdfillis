"""PDFillis module."""

import os
from tkinter import *
from tkinter import filedialog

import fitz


DEFAULT_FONT_SIZE = ["TkDefaultFont", "10", "bold"]


class PDFillis:
    """Defines the GUI and all PDF handling functions."""

    def __init__(self) -> None:
        self._selected_files = []

        # GUI
        self._window = Tk()
        self._window.title("PDFillis - Combinador de PDFs")
        self._window.geometry("415x360")
        self._window.config(background="white")

        # Widgets definition
        self._button_explore = Button(
            self._window,
            text="Escolher Arquivos",
            font=DEFAULT_FONT_SIZE,
            fg="white",
            bg="#6c757d",
            command=self._browse_files,
        )
        self._button_merge_pdf = Button(
            self._window,
            text="Combinar PDFs",
            font=DEFAULT_FONT_SIZE,
            fg="white",
            background="#28a745",
            command=self.merge_pdf,
        )
        self._button_exit = Button(
            self._window,
            text="Sair",
            font=DEFAULT_FONT_SIZE,
            width=10,
            fg="white",
            bg="#dc3545",
            command=exit,
        )
        self._label_file_explorer = Label(
            self._window, text="Arquivos selecionados:", font=DEFAULT_FONT_SIZE, fg="#6c757d", bg="white"
        )

        # Widgets positioning
        padx_default = 15
        pady_default = 10

        self._button_explore.grid(column=1, row=1, padx=padx_default, pady=pady_default)
        self._button_merge_pdf.grid(column=2, row=1, padx=padx_default, pady=pady_default)
        self._button_exit.grid(column=5, row=1, padx=padx_default, pady=pady_default)
        self._label_file_explorer.grid(
            column=1,
            row=2,
            columnspan=3,
        )

    def _browse_files(self):
        """Open the file explorer window."""
        initial_dir = f"C://Users//{os.getlogin()}//Downloads"

        file_name = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Selecione um Arquivo PDF",
            filetypes=[("PDF", "*.pdf")],
        )

        self._selected_files.append(file_name)

        selected_files_text = "\n ".join(self._selected_files)
        self._label_file_explorer.configure(text=f"Arquivos selecionados:\n{selected_files_text}", fg="blue")

    def merge_pdf(self):
        """Merge the selected PDFs into a single one, in the same order they were selected."""
        if len(self._selected_files) == 0:
            self._label_file_explorer.configure(text="Nenhum arquivo selecionado!", fg="red")
            return

        accepted_file_types = [("PDF", "*.pdf")]
        pdf_file = filedialog.asksaveasfile(
            filetypes=accepted_file_types,
            defaultextension=accepted_file_types,
            title="Salvar arquivos combinados",
        )

        if pdf_file:
            pdf_file_name = pdf_file.name
            pdf_file.close()

            merged_pdf = fitz.open()

            for selected_file in self._selected_files:
                with fitz.open(selected_file) as pdf:
                    merged_pdf.insert_pdf(pdf)

            merged_pdf.save(pdf_file_name)
            merged_pdf.close()

            self._selected_files.clear()
            self._label_file_explorer.configure(text="Arquivos combinados com sucesso!", fg="green")

    def run(self):
        """Run the app."""
        self._window.mainloop()
