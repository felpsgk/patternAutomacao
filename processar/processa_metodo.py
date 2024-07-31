import os
import re
from unidecode import unidecode
from processar.processa_texto import TextProcessor
from processar.processa_arquivo import FileProcessor

class DefProcessor:
   
# Função para gerar o nome do método a partir do passo
    @staticmethod
    def gerar_nome_metodo(passo):
        partes = passo.title().split(' ', 1)
        descricao = TextProcessor.remover_texto_dentro_string(partes[1]).replace("'", "").replace('"', '').replace(" ", "").replace(",", "").replace("!", "").replace("?", "").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("í", "i")
        return descricao[0] + descricao[1:]
   
# Função para verificar se um método já existe no conteúdo do arquivo
    @staticmethod
    def metodo_existe(conteudo, metodo):
        # Usar expressão regular para procurar o método
        padrao = re.compile(r'\bpublic void ' + re.escape(metodo) + r'\s*\(', re.MULTILINE)
        return padrao.search(conteudo) is not None
   
# Função para verificar se um método já existe no conteúdo do arquivo
    @staticmethod
    def extrair_metodo_stepdefs_existente(conteudo_steps_definitions_linhas, metodos_steps_definitions_existentes):
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
   
# Função para verificar se um método já existe no conteúdo do arquivo
    @staticmethod
    def extrair_metodo_steps_existente(conteudo_steps_linhas, metodos_steps_existentes):
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
   
# Função para verificar se um método já existe no conteúdo do arquivo
    @staticmethod
    def extrair_metodo_pages_existente(conteudo_pages_linhas, metodos_pages_existentes):
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
         
# Função pra gerar os metodos finais
    @staticmethod
    def gerar_metodos_finais(conteudo_steps_definitions,conteudo_steps,conteudo_pages,matriz_assoc,passos_metodos_unicos,novos_metodos_definitions,novos_metodos_steps,caminho_steps_definitions,caminho_steps,caminho_pages,novos_metodos_pages):
        for passo_metodo_unico in passos_metodos_unicos:
            passo_completo = encontrar_frase_por_metodo(matriz_assoc,passo_metodo_unico)
            #exists = False
            descricao_formatada = ""
            if "'" in passo_completo:  # Se o passo contém aspas, ajustar para passar o parâmetro string
                descricao = passo_completo.split(' ', 1)[1]
                descricao_formatada = TextProcessor.substituir_aspas_por_string(descricao)
                novos_metodos_definitions.append(f"""
    @{passo_completo.split(' ')[0]}("{descricao_formatada}")
    public void {TextProcessor.remover_acentos(passo_metodo_unico)}(String texto) {{
        // Implementar a lógica para {passo_completo}
        {os.path.basename(caminho_steps).replace('.java', '').lower()}.{TextProcessor.remover_acentos(passo_metodo_unico)}(texto);
    }}
""")
                novos_metodos_steps.append(f"""
    @Step("{descricao_formatada}")
    public void {TextProcessor.remover_acentos(passo_metodo_unico)}(String texto) {{
        // Implementar a lógica para {passo_completo}
        {os.path.basename(caminho_pages).replace('.java', '').lower()}.{TextProcessor.remover_acentos(passo_metodo_unico)}(texto);
    }}
""")
                novos_metodos_pages.append(f"""
    public void {TextProcessor.remover_acentos(passo_metodo_unico)}(String texto) {{
        // Implementar a lógica para a página relacionada ao passo {passo_completo}
    }}
""")
            else:
                descricao = passo_completo.split(' ', 1)[1]
                novos_metodos_definitions.append(f"""
    @{passo_completo.split(' ')[0]}("{passo_completo.split(' ', 1)[1]}")
    public void {TextProcessor.remover_acentos(passo_metodo_unico)}() {{
        // Implementar a lógica para {passo_completo}
        {os.path.basename(caminho_steps).replace('.java', '').lower()}.{TextProcessor.remover_acentos(passo_metodo_unico)}();
    }}
""")
                novos_metodos_steps.append(f"""
    @Step("{descricao}")
    public void {TextProcessor.remover_acentos(passo_metodo_unico)}() {{
        // Implementar a lógica para {passo_completo}
        {os.path.basename(caminho_pages).replace('.java', '').lower()}.{TextProcessor.remover_acentos(passo_metodo_unico)}();
    }}
""")
                novos_metodos_pages.append(f"""
    public void {TextProcessor.remover_acentos(passo_metodo_unico)}() {{
        // Implementar a lógica para a página relacionada ao passo {passo_completo}
    }}
""")
        incluir_metodos_no_arquivo(caminho_steps_definitions,caminho_steps,caminho_pages,conteudo_steps_definitions,conteudo_steps,conteudo_pages,novos_metodos_definitions,novos_metodos_steps,novos_metodos_pages)       


# Função pra gerar os metodos finais
def incluir_metodos_no_arquivo(caminho_steps_definitions,caminho_steps,caminho_pages,conteudo_steps_definitions,conteudo_steps,conteudo_pages,novos_metodos_definitions,novos_metodos_steps,novos_metodos_pages):
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
    FileProcessor.escrever_conteudo_arquivo(caminho_steps_definitions, conteudo_steps_definitions)
    FileProcessor.escrever_conteudo_arquivo(caminho_steps, conteudo_steps)
    FileProcessor.escrever_conteudo_arquivo(caminho_pages, conteudo_pages)

          
# Função para encontrar a frase correspondente ao método
def encontrar_frase_por_metodo(matriz, metodo):
    for passo, metodo_gerado in matriz:
        if metodo_gerado == metodo:
            return passo
    return ""
