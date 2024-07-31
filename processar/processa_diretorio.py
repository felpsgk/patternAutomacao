import os
import tkinter as tk
from tkinter import filedialog

class DirManager:
    def __init__(self, directories):
        self.directories = directories

    def create_directories(self):
        for directory in self.directories:
            os.makedirs(directory, exist_ok=True)
            
    # Função para selecionar pastas usando tkinter
    def selecionar_pastas():
        # Criar janela Tkinter
        root = tk.Tk()
        root.withdraw()

        # Exibir diálogos de seleção de pastas
        dir_feature = filedialog.askdirectory(title="Selecione a pasta dos arquivos .feature")
        dir_steps_definitions = filedialog.askdirectory(title="Selecione a pasta das Steps Definitions")
        dir_steps = filedialog.askdirectory(title="Selecione a pasta dos Steps")
        dir_pages = filedialog.askdirectory(title="Selecione a pasta das Pages")

        # Retornar os caminhos selecionados
        return dir_feature, dir_steps_definitions, dir_steps, dir_pages
