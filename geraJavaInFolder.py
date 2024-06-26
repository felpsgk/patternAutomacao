import os
import re
import glob
from collections import Counter

# Função para ler o conteúdo de um arquivo Java
def ler_conteudo_arquivo(nome_arquivo):
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    return ""

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
                f.write(f"public class {os.path.basename(caminho_steps_definitions).replace('.java', '')} {{\n\n    @Steps\n    {os.path.basename(caminho_steps).replace('.java', '')} {os.path.basename(caminho_steps).replace('.java', '').lower()};\n\n}}\n")
        
        if not os.path.exists(caminho_steps):
            with open(caminho_steps, 'w', encoding='utf-8') as f:
                f.write(f"public class {os.path.basename(caminho_steps).replace('.java', '')} {{\n\n    {os.path.basename(caminho_pages).replace('.java', '')} {os.path.basename(caminho_pages).replace('.java', '').lower()};\n\n}}\n")
        
        if not os.path.exists(caminho_pages):
            with open(caminho_pages, 'w', encoding='utf-8') as f:
                f.write(f"public class {os.path.basename(caminho_pages).replace('.java', '')} {{\n\n}}\n\n")

        # Ler o conteúdo dos arquivos Java existentes
        conteudo_steps_definitions = ler_conteudo_arquivo(caminho_steps_definitions)
        conteudo_steps_definitions_linhas = ler_conteudo_arquivo_linhas(caminho_steps_definitions)
        
        conteudo_steps = ler_conteudo_arquivo(caminho_steps)
        conteudo_pages = ler_conteudo_arquivo(caminho_pages)
        
        #extrair metodos já existentes
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
        
        # Adicionar novos métodos aos arquivos Java, se não existirem
        novos_metodos_definitions = []
        novos_metodos_steps = []
        novos_metodos_pages = []
        metodos_gerados = []
        reserva = ""
        #encontra metodo já escrito
        for passo in passos:
            metodos_gerados.append(gerar_nome_metodo(passo))
        
            
        matriz_assoc = list(zip(passos, metodos_gerados))
        # Função para encontrar a frase correspondente ao método
        def encontrar_frase_por_metodo(matriz, metodo):
            for passo, metodo_gerado in matriz:
                if metodo_gerado == metodo:
                    return passo
            return ""
        
        contagem = Counter(metodos_gerados + metodos_steps_definitions_existentes)
        passos_metodos_unicos = [item for item, count in contagem.items() if count == 1]

        #passos_metodos = metodos_gerados + metodos_steps_definitions_existentes
        #passos_metodos_unicos = set(passos_metodos)
            
        for passo_metodo_unico in passos_metodos_unicos:
            passo_completo = encontrar_frase_por_metodo(matriz_assoc,passo_metodo_unico)
            #exists = False
            descricao_formatada = ""
            if "'" in passo_completo:  # Se o passo contém aspas, ajustar para passar o parâmetro string
                descricao = passo_completo.split(' ', 1)[1]
                descricao_formatada = substituir_aspas_por_string(descricao)
                novos_metodos_definitions.append(f"""
    @{passo_completo.split(' ')[0]}("{descricao_formatada}")
    public void {passo_metodo_unico}(String texto) {{
        // Implementar a lógica para {passo_completo}
        {os.path.basename(caminho_steps).replace('.java', '').lower()}.{passo_metodo_unico}(texto);
    }}
""")
                
                if passo_metodo_unico.startswith(("public void", "public static", "public String", "public int", "public boolean")):
                    print("criando metodo para "+ passo_metodo_unico)
                    if nome_metodo in passo_metodo_unico:
                        print("")
                        print("já existe, nao criado ")
                    elif nome_metodo not in passo_metodo_unico:
                        print("não existe, será criado")
                        print("")
                        

        for passo in passos:
            nome_metodo = gerar_nome_metodo(passo)
            descricao_formatada = ""
            if "'" in passo:  # Se o passo contém aspas, ajustar para passar o parâmetro string
                if not metodo_existe(reserva.rstrip('}\n') + "\n".join(novos_metodos_definitions), nome_metodo):
                   print("")
                if not metodo_existe(reserva.rstrip('}\n') + "\n".join(novos_metodos_steps), nome_metodo):
                    novos_metodos_steps.append(f"""
    @Step("{descricao_formatada}")
    public void {nome_metodo}(String texto) {{
        // Implementar a lógica para {passo}
        {os.path.basename(caminho_pages).replace('.java', '').lower()}.{nome_metodo}(texto);
    }}
""")
                if not metodo_existe(reserva.rstrip('}\n') + "\n".join(novos_metodos_pages), nome_metodo):
                    novos_metodos_pages.append(f"""
    public void {nome_metodo}(String texto) {{
        // Implementar a lógica para a página relacionada ao passo {passo}
    }}
""")
    
            else:
                if not metodo_existe(reserva.rstrip('}\n') + "\n".join(novos_metodos_definitions), nome_metodo):
                    novos_metodos_definitions.append(f"""
    @{passo.split(' ')[0]}("{passo.split(' ', 1)[1]}")
    public void {nome_metodo}() {{
        // Implementar a lógica para {passo}
        {os.path.basename(caminho_steps).replace('.java', '').lower()}.{nome_metodo}();
    }}
""")
                if not metodo_existe(reserva.rstrip('}\n') + "\n".join(novos_metodos_steps), nome_metodo):
                    novos_metodos_steps.append(f"""
    @Step("{descricao_formatada}")
    public void {nome_metodo}() {{
        // Implementar a lógica para {passo}
        {os.path.basename(caminho_pages).replace('.java', '').lower()}.{nome_metodo}();
    }}
""")
                if not metodo_existe(reserva.rstrip('}\n') + "\n".join(novos_metodos_pages), nome_metodo):
                    novos_metodos_pages.append(f"""
    public void {nome_metodo}() {{
        // Implementar a lógica para a página relacionada ao passo {passo}
    }}
""")
                
        # Adicionar novos métodos ao conteúdo existente dentro do bloco da classe
        if novos_metodos_definitions:
            conteudo_steps_definitions = conteudo_steps_definitions.rstrip('}\n') + "\n".join(novos_metodos_definitions) + "\n}\n"
        if novos_metodos_steps:
            conteudo_steps = conteudo_steps.rstrip('}\n') + "\n".join(novos_metodos_steps) + "\n}\n"
        if novos_metodos_pages:
            conteudo_pages = conteudo_pages.rstrip('}\n') + "\n".join(novos_metodos_pages) + "\n}\n"
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
    # Definindo diretórios para os arquivos de saída
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
       
