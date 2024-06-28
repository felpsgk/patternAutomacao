import os
import re
import glob
from unidecode import unidecode
from collections import Counter

# Função para ler o conteúdo de um arquivo Java
def ler_conteudo_arquivo(nome_arquivo):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    return ""

# Função para remover acentos de uma string
def remover_acentos(texto):
    return unidecode(texto)

#ler em linhas o arquivo
def ler_conteudo_arquivo_linhas(nome_arquivo):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.readlines()
    return ""

# Função para escrever o conteúdo atualizado de volta para o arquivo
def escrever_conteudo_arquivo(nome_arquivo, conteudo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(conteudo)
    print(f"Arquivo {nome_arquivo} atualizado com sucesso.")

# Função para verificar se um método já existe no conteúdo do arquivo
def metodo_existe(conteudo, metodo):
    # Usar expressão regular para procurar o método
    padrao = re.compile(r'\bpublic void ' + re.escape(metodo) + r'\s*\(', re.MULTILINE)
    return padrao.search(conteudo) is not None

def substituir_aspas_por_string(texto):
    padrao = r"'([^']*)'"
    return re.sub(padrao, r"{string}", texto)

def remover_texto_dentro_string(texto):
    padrao = r"'([^']*)'"
    return re.sub(padrao, r"", texto)

# Função para gerar o nome do método a partir do passo
def gerar_nome_metodo(passo):
    partes = passo.title().split(' ', 1)
    descricao = remover_texto_dentro_string(partes[1]).replace("'", "").replace('"', '').replace(" ", "").replace(",", "").replace("!", "").replace("?", "").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("í", "i")
    return descricao[0] + descricao[1:]

# Função para gerar o nome do arquivo StepDefinitions.java
def gerar_nome_arquivo_step_definitions(nome_base):
    nome_base_formatado = remover_texto_dentro_string(nome_base.title()).replace(" ", "").replace(",", "").replace("!", "").replace("?", "").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("í", "i")
    return os.path.abspath("stepdefinitions") +"\\"+ nome_base_formatado + "StepDefinitions.java"

# Função para gerar o nome do arquivo Steps.java
def gerar_nome_arquivo_steps(nome_base):
    nome_base_formatado = remover_texto_dentro_string(nome_base.title()).replace(" ", "").replace(",", "").replace("!", "").replace("?", "").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("í", "i")
    return os.path.abspath("steps")+"\\"+ nome_base_formatado + "Steps.java"

# Função para gerar o nome do arquivo Page.java
def gerar_nome_arquivo_page(nome_base):
    nome_base_formatado = remover_texto_dentro_string(nome_base.title()).replace(" ", "").replace(",", "").replace("!", "").replace("?", "").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("í", "i")
    return os.path.abspath("pages") +"\\"+ nome_base_formatado + "Page.java"

# Função para encontrar a frase correspondente ao método
def encontrar_frase_por_metodo(matriz, metodo):
    for passo, metodo_gerado in matriz:
        if metodo_gerado == metodo:
            return passo
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

# Função principal para processar a feature e atualizar os arquivos Java
def processar_feature(caminho_feature, nome_feature):
    caminho_steps_definitions = gerar_nome_arquivo_step_definitions(nome_feature)
    caminho_steps = gerar_nome_arquivo_steps(nome_feature)
    caminho_pages = gerar_nome_arquivo_page(nome_feature)
    try:
        # Ler o conteúdo do arquivo .feature
        with open(caminho_feature, 'r', encoding='utf-8') as arquivo_feature:
            conteudo_feature = arquivo_feature.readlines()

        # Extrair os backgrounds e passos de cenários automatizáveis
        passos = []
        in_automatizar = False
        in_scenario = False
        in_background = False
        for linha in conteudo_feature:
            linha = linha.strip()
            if linha.startswith("@automatizar"):
                in_automatizar = True
            elif linha.startswith("Background:"):
                in_background = True
            elif linha.startswith("Scenario:"):
                in_scenario = True     
            elif linha.startswith("Given") or linha.startswith("When") or linha.startswith("Then") or linha.startswith("And"):
                if in_background:
                    passos.append(linha)
                elif in_automatizar:
                    if in_scenario:
                        passos.append(linha)
            elif linha == "":
                in_automatizar = False
                in_scenario = False
                in_background = False
                
        # Criar os arquivos Java se não existirem
        if not os.path.exists(caminho_steps_definitions):
            with open(caminho_steps_definitions, 'w', encoding='utf-8') as f:
                conteudo = f"public class {os.path.basename(caminho_steps_definitions).replace('.java', '')} {{\n\n    @Steps\n    {os.path.basename(caminho_steps).replace('.java', '')} {os.path.basename(caminho_steps).replace('.java', '').lower()};\n\n}}\n"
                conteudo = adicionar_imports(conteudo, "stepdefinitions", "informe_caminho_seu_projeto")
                f.write(conteudo)

        if not os.path.exists(caminho_steps):
            with open(caminho_steps, 'w', encoding='utf-8') as f:
                conteudo = f"public class {os.path.basename(caminho_steps).replace('.java', '')} {{\n\n    {os.path.basename(caminho_pages).replace('.java', '')} {os.path.basename(caminho_pages).replace('.java', '').lower()};\n\n}}\n"
                conteudo = adicionar_imports(conteudo, "steps", "informe_caminho_seu_projeto")
                f.write(conteudo)

        if not os.path.exists(caminho_pages):
            with open(caminho_pages, 'w', encoding='utf-8') as f:
                conteudo = f"public class {os.path.basename(caminho_pages).replace('.java', '')} extends PageBase {{\n\n}}\n\n"
                conteudo = adicionar_imports(conteudo, "page", "informe_caminho_seu_projeto")
                f.write(conteudo)

        #Cria array novos métodos aos arquivos Java, se não existirem
        novos_metodos_definitions = []
        novos_metodos_steps = []
        novos_metodos_pages = []

        # Ler o conteúdo dos arquivos Java existentes
        conteudo_steps_definitions = ler_conteudo_arquivo(caminho_steps_definitions)
        conteudo_steps_definitions_linhas = ler_conteudo_arquivo_linhas(caminho_steps_definitions)
        conteudo_steps = ler_conteudo_arquivo(caminho_steps)
        conteudo_steps_linhas = ler_conteudo_arquivo_linhas(caminho_steps)
        conteudo_pages = ler_conteudo_arquivo(caminho_pages)
        conteudo_pages_linhas = ler_conteudo_arquivo_linhas(caminho_pages)
        
        #Extrair metodos steps definitions já existentes
        metodos_steps_definitions_existentes = []
        in_metodo = False
        for linha in conteudo_steps_definitions_linhas:
            linha = linha.strip()
            if linha.startswith(("public void", "public static", "public String", "public int", "public boolean")):
                in_metodo = True
            if in_metodo:
                metodo_final = re.search(r'\s(\w+)\(', linha)
                if metodo_final:
                    metodos_steps_definitions_existentes.append(metodo_final.group(1))
            elif linha == "":
                in_metodo = False
                
        #a partir do passo, gera metodo steps definitions e guarda
        metodos_gerados = []
        for passo in passos:
            metodos_gerados.append(gerar_nome_metodo(passo))
        
        #unificar metodos gerados
        unificar = list(dict.fromkeys(metodos_gerados))
        
        #counter para unificar metodos steps definitions
        contagem = Counter(metodos_steps_definitions_existentes + unificar)
        passos_metodos_unicos = [item for item, count in contagem.items() if count == 1]
            
        #Extrair metodos steps já existentes
        metodos_steps_existentes = []
        in_metodo_steps = False
        for linha_steps in conteudo_steps_linhas:
            linha_steps = linha_steps.strip()
            if linha_steps.startswith(("public void", "public static", "public String", "public int", "public boolean")):
                in_metodo_steps = True
            if in_metodo_steps:
                metodo_steps_final = re.search(r'\s(\w+)\(', linha_steps)
                if metodo_steps_final:
                    metodos_steps_existentes.append(metodo_steps_final.group(1))
            elif linha_steps == "":
                in_metodo_steps = False
                
        #a partir do passo, gera metodo steps definitions e guarda
        metodos_steps_gerados = []
        for passo_steps in passos:
            metodos_steps_gerados.append(gerar_nome_metodo(passo_steps))
        #counter para unificar metodos steps definitions
        contagem_steps = Counter(metodos_steps_gerados + metodos_steps_existentes)
        passos_metodos_steps_unicos = [item for item, count in contagem_steps.items() if count == 1]
            
        #Extrair metodos pages já existentes
        metodos_pages_existentes = []
        in_metodo_pages = False
        for linha_pages in conteudo_pages_linhas:
            linha_pages = linha_pages.strip()
            if linha_pages.startswith(("public void", "public static", "public String", "public int", "public boolean")):
                in_metodo_pages = True
            if in_metodo_pages:
                metodo_pages_final = re.search(r'\s(\w+)\(', linha_pages)
                if metodo_pages_final:
                    metodos_pages_existentes.append(metodo_pages_final.group(1))
            elif linha_pages == "":
                in_metodo_pages = False
                
        #a partir do passo, gera metodo steps definitions e guarda
        metodos_pages_gerados = []
        for passo_pages in passos:
            metodos_pages_gerados.append(gerar_nome_metodo(passo_pages))
        #counter para unificar metodos steps definitions
        contagem_pages = Counter(metodos_pages_gerados + metodos_pages_existentes)
        passos_metodos_pages_unicos = [item for item, count in contagem_pages.items() if count == 1]
            
            
        #matriz que associa o passo ao metodo
        matriz_assoc = list(zip(passos, metodos_gerados))
        
        for passo_metodo_unico in passos_metodos_unicos:
            passo_completo = encontrar_frase_por_metodo(matriz_assoc,passo_metodo_unico)
            #exists = False
            descricao_formatada = ""
            if "'" in passo_completo:  # Se o passo contém aspas, ajustar para passar o parâmetro string
                descricao = passo_completo.split(' ', 1)[1]
                descricao_formatada = substituir_aspas_por_string(descricao)
                novos_metodos_definitions.append(f"""
    @{passo_completo.split(' ')[0]}("{descricao_formatada}")
    public void {remover_acentos(passo_metodo_unico)}(String texto) {{
        // Implementar a lógica para {passo_completo}
        {os.path.basename(caminho_steps).replace('.java', '').lower()}.{remover_acentos(passo_metodo_unico)}(texto);
    }}
""")
                novos_metodos_steps.append(f"""
    @Step("{descricao_formatada}")
    public void {remover_acentos(passo_metodo_unico)}(String texto) {{
        // Implementar a lógica para {passo_completo}
        {os.path.basename(caminho_pages).replace('.java', '').lower()}.{remover_acentos(passo_metodo_unico)}(texto);
    }}
""")
                novos_metodos_pages.append(f"""
    public void {remover_acentos(passo_metodo_unico)}(String texto) {{
        // Implementar a lógica para a página relacionada ao passo {passo_completo}
    }}
""")
            else:
                descricao = passo_completo.split(' ', 1)[1]
                novos_metodos_definitions.append(f"""
    @{passo_completo.split(' ')[0]}("{passo_completo.split(' ', 1)[1]}")
    public void {remover_acentos(passo_metodo_unico)}() {{
        // Implementar a lógica para {passo_completo}
        {os.path.basename(caminho_steps).replace('.java', '').lower()}.{remover_acentos(passo_metodo_unico)}();
    }}
""")
                novos_metodos_steps.append(f"""
    @Step("{descricao}")
    public void {remover_acentos(passo_metodo_unico)}() {{
        // Implementar a lógica para {passo_completo}
        {os.path.basename(caminho_pages).replace('.java', '').lower()}.{remover_acentos(passo_metodo_unico)}();
    }}
""")
                novos_metodos_pages.append(f"""
    public void {remover_acentos(passo_metodo_unico)}() {{
        // Implementar a lógica para a página relacionada ao passo {passo_completo}
    }}
""")
        if novos_metodos_definitions:
            index_ultima_chave = conteudo_steps_definitions.rfind('}')
            if index_ultima_chave != -1:
                conteudo_steps_definitions = conteudo_steps_definitions[:index_ultima_chave] + conteudo_steps_definitions[index_ultima_chave+1:]
                conteudo_steps_definitions = conteudo_steps_definitions + "\n".join(novos_metodos_definitions) + "\n}\n"
        if novos_metodos_steps:
            index_ultima_chave = conteudo_steps.rfind('}')
            if index_ultima_chave != -1:
                conteudo_steps = conteudo_steps[:index_ultima_chave] + conteudo_steps[index_ultima_chave+1:]
                conteudo_steps = conteudo_steps + "\n".join(novos_metodos_steps) + "\n}\n"
        if novos_metodos_pages:
            index_ultima_chave = conteudo_pages.rfind('}')
            if index_ultima_chave != -1:
                conteudo_pages = conteudo_pages[:index_ultima_chave] + conteudo_pages[index_ultima_chave+1:]
                conteudo_pages = conteudo_pages + "\n".join(novos_metodos_pages) + "\n}\n"

        
        # Escrever o conteúdo atualizado nos arquivos Java
        escrever_conteudo_arquivo(caminho_steps_definitions, conteudo_steps_definitions)
        escrever_conteudo_arquivo(caminho_steps, conteudo_steps)
        escrever_conteudo_arquivo(caminho_pages, conteudo_pages)

    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# Exemplo de uso
if __name__ == "__main__":
    # Definindo pasta a ser procurada os arquivos java para escrever os arquivos de saída
    dir_steps_definitions = 'stepdefinitions'
    dir_steps = 'steps'
    dir_pages = 'pages'

    # Criando diretórios se não existirem
    os.makedirs(dir_steps_definitions, exist_ok=True)
    os.makedirs(dir_steps, exist_ok=True)
    os.makedirs(dir_pages, exist_ok=True)

    # Processar todos os arquivos .feature na pasta atual
    for caminho_feature in glob.glob("*.feature"):
        caminho_feature = os.path.abspath(caminho_feature)
        nome_feature = os.path.basename(caminho_feature.replace(".feature","").replace("_"," "))
        processar_feature(caminho_feature, nome_feature)
       