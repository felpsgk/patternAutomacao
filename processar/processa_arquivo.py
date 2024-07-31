import os
import re
from processar.processa_texto import TextProcessor

class FileProcessor:
    # @staticmethod
    # def read_file_content(file_name):
    #     if os.path.exists(file_name):
    #         with open(file_name, 'r', encoding='utf-8') as file:
    #             return file.read()
    #     return ""

    # @staticmethod
    # def read_file_lines(file_name):
    #     if os.path.exists(file_name):
    #         with open(file_name, 'r', encoding='utf-8') as file:
    #             return file.readlines()
    #     return ""
    
# Função para escrever o conteúdo atualizado de volta para o arquivo
    @staticmethod
    def escrever_conteudo_arquivo(nome_arquivo, conteudo):
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
        print(f"Arquivo {nome_arquivo} atualizado com sucesso.")

    # Função para gerar o nome do arquivo StepDefinitions.java
    @staticmethod
    def gerar_nome_arquivo_step_definitions(nome_base, dir_step_definitions):
        nome_base_formatado = TextProcessor.remover_texto_dentro_string(nome_base.title()).replace(" ", "").replace(",", "").replace("!", "").replace("?", "").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("í", "i")
        return dir_step_definitions +"/"+ nome_base_formatado + "StepDefinitions.java"

    # Função para gerar o nome do arquivo Steps.java
    @staticmethod
    def gerar_nome_arquivo_steps(nome_base, dir_steps):
        nome_base_formatado = TextProcessor.remover_texto_dentro_string(nome_base.title()).replace(" ", "").replace(",", "").replace("!", "").replace("?", "").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("í", "i")
        return dir_steps+"/"+ nome_base_formatado + "Steps.java"

    # Função para gerar o nome do arquivo Page.java
    @staticmethod
    def gerar_nome_arquivo_page(nome_base,dir_pages):
        nome_base_formatado = TextProcessor.remover_texto_dentro_string(nome_base.title()).replace(" ", "").replace(",", "").replace("!", "").replace("?", "").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("í", "i")
        return dir_pages+"/"+ nome_base_formatado + "Page.java"

    # Função para gerar o nome do arquivo Page.java
    @staticmethod
    def criaStepDefIfNotExists(caminho_steps_definitions,caminho_steps):
        if not os.path.exists(caminho_steps_definitions):
            with open(caminho_steps_definitions, 'w', encoding='utf-8') as f:
                conteudo = f"public class {os.path.basename(caminho_steps_definitions).replace('.java', '')} {{\n\n    @Steps\n    {os.path.basename(caminho_steps).replace('.java', '')} {os.path.basename(caminho_steps).replace('.java', '').lower()};\n\n}}\n"
                conteudo = adicionar_imports(conteudo, "stepdefinitions", "informe_caminho_seu_projeto")
                f.write(conteudo)

    # Função para gerar o nome do arquivo Page.java
    @staticmethod
    def criaStepIfNotExists(caminho_steps,caminho_pages):
        if not os.path.exists(caminho_steps):
            with open(caminho_steps, 'w', encoding='utf-8') as f:
                conteudo = f"public class {os.path.basename(caminho_steps).replace('.java', '')} {{\n\n    {os.path.basename(caminho_pages).replace('.java', '')} {os.path.basename(caminho_pages).replace('.java', '').lower()};\n\n}}\n"
                conteudo = adicionar_imports(conteudo, "steps", "informe_caminho_seu_projeto")
                f.write(conteudo)

    # Função para gerar o nome do arquivo Page.java
    @staticmethod
    def criaPageIfNotExists(caminho_pages):
        if not os.path.exists(caminho_pages):
            with open(caminho_pages, 'w', encoding='utf-8') as f:
                conteudo = f"public class {os.path.basename(caminho_pages).replace('.java', '')} extends PageBase {{\n\n}}\n\n"
                conteudo = adicionar_imports(conteudo, "page", "informe_caminho_seu_projeto")
                f.write(conteudo)
             
     # Função para ler o conteúdo de um arquivo Java
    @staticmethod
    def ler_conteudo_arquivo(nome_arquivo):
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                return arquivo.read()
        return ""
    
    #ler em linhas o arquivo
    @staticmethod
    def ler_conteudo_arquivo_linhas(nome_arquivo):
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                return arquivo.readlines()
        return ""

           
# Função para adicionar os imports necessários
def adicionar_imports(conteudo, tipo, nome_package):
    imports_comuns = ""
    imports_especificos = ""
    if tipo == "stepdefinitions":
        imports_comuns = """import io.cucumber.java.en.When;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import net.serenitybdd.annotations.Steps;"""
        imports_especificos = f"import {nome_package}.{conteudo.split(' ', 3)[2]};"

    elif tipo == "steps":
        imports_comuns = "import net.serenitybdd.annotations.Step;"
        imports_especificos = f"import {nome_package}.{conteudo.split(' ', 3)[2]};"

    elif tipo == "page":
        imports_comuns = """import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;"""
        imports_especificos = f"import {nome_package}.PageBase;"

    conteudo_imports = f"{imports_comuns}\n{imports_especificos}\n\n"
    return conteudo_imports + conteudo
                
