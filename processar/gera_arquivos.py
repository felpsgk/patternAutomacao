import os
from collections import Counter
from processar.processa_arquivo import FileProcessor
from processar.separar_frases import separaFrases
from processar.processa_texto import TextProcessor
from processar.processa_metodo import DefProcessor

class GeraArquivos:
    def __init__(self):
        self.file_reader = FileProcessor()
    #rastreia todos os arquivos *.feature
    def processar_arquivos_feature_recursivamente(self,dir_feature, dir_step_definitions, dir_steps, dir_pages):
        for root, _, files in os.walk(dir_feature):
            for file in files:
                if file.endswith(".feature"):
                    caminho_feature = os.path.join(root, file)
                    nome_feature = os.path.basename(caminho_feature.replace(".feature","").replace("_"," "))
                    processar_features(caminho_feature, nome_feature, dir_step_definitions, dir_steps, dir_pages)

# Processa todos os arquivos
def processar_features(caminho_feature, nome_feature, dir_step_definitions, dir_steps, dir_pages):
    file_processor = FileProcessor()
    caminho_steps_definitions = file_processor.gerar_nome_arquivo_step_definitions(nome_feature, dir_step_definitions)
    caminho_steps = file_processor.gerar_nome_arquivo_steps(nome_feature, dir_steps)
    caminho_pages = file_processor.gerar_nome_arquivo_page(nome_feature, dir_pages)
    
    try:
        # Ler o conteúdo do arquivo .feature
        with open(caminho_feature, 'r', encoding='utf-8') as arquivo_feature:
            conteudo_feature = arquivo_feature.readlines()
        # Extrair os backgrounds e passos de cenários automatizáveis
        passos = []
        passos = separaFrases.separa_frases(conteudo_feature,passos)
          
        # Criar os arquivos Java se não existirem
        file_processor.criaStepDefIfNotExists(caminho_steps_definitions,caminho_steps)
             
        # Criar os arquivos Java se não existirem
        file_processor.criaStepIfNotExists(caminho_steps,caminho_pages)
                    
        # Criar os arquivos Java se não existirem
        file_processor.criaPageIfNotExists(caminho_pages)
        
        #Cria array novos métodos aos arquivos Java, se não existirem
        novos_metodos_definitions = []
        novos_metodos_steps = []
        novos_metodos_pages = []

        # Ler o conteúdo dos arquivos Java existentes
        conteudo_steps_definitions = file_processor.ler_conteudo_arquivo(caminho_steps_definitions)
        conteudo_steps_definitions_linhas = file_processor.ler_conteudo_arquivo_linhas(caminho_steps_definitions)
        conteudo_steps = file_processor.ler_conteudo_arquivo(caminho_steps)
        conteudo_steps_linhas = file_processor.ler_conteudo_arquivo_linhas(caminho_steps)
        conteudo_pages = file_processor.ler_conteudo_arquivo(caminho_pages)
        conteudo_pages_linhas = file_processor.ler_conteudo_arquivo_linhas(caminho_pages)
        #Extrair metodos steps definitions já existentes
        metodos_steps_definitions_existentes = []
        DefProcessor.extrair_metodo_stepdefs_existente(conteudo_steps_definitions_linhas,metodos_steps_definitions_existentes)
        
        #a partir do passo, gera metodo steps definitions e guarda
        metodos_gerados = []
        for passo in passos:
            metodos_gerados.append((DefProcessor.gerar_nome_metodo(passo)))
            
        #unificar metodos gerados
        unificar = list(dict.fromkeys(metodos_gerados))
        #counter para unificar metodos steps definitions
        contagem = Counter(metodos_steps_definitions_existentes + unificar)
        passos_metodos_unicos = [item for item, count in contagem.items() if count == 1]
            
        #Extrair metodos steps já existentes        
        metodos_steps_existentes = []
        DefProcessor.extrair_metodo_steps_existente(conteudo_steps_linhas,metodos_steps_existentes)
        
        #a partir do passo, gera metodo steps definitions e guarda
        metodos_steps_gerados = []
        for passo_steps in passos:
            metodos_steps_gerados.append(DefProcessor.gerar_nome_metodo(passo_steps))
            
        #counter para unificar metodos steps definitions
        contagem_steps = Counter(metodos_steps_gerados + metodos_steps_existentes)
        passos_metodos_steps_unicos = [item for item, count in contagem_steps.items() if count == 1]
            
        #Extrair metodos pages já existentes
        metodos_pages_existentes = []
        DefProcessor.extrair_metodo_pages_existente(conteudo_pages_linhas,metodos_pages_existentes)
                        
        #a partir do passo, gera metodo steps definitions e guarda
        metodos_pages_gerados = []
        for passo_pages in passos:
            metodos_pages_gerados.append(DefProcessor.gerar_nome_metodo(passo_pages))
        #counter para unificar metodos steps definitions
        contagem_pages = Counter(metodos_pages_gerados + metodos_pages_existentes)
        passos_metodos_pages_unicos = [item for item, count in contagem_pages.items() if count == 1]
            
        #matriz que associa o passo ao metodo
        matriz_assoc = list(zip(passos, metodos_gerados))
        DefProcessor.gerar_metodos_finais(conteudo_steps_definitions,conteudo_steps,conteudo_pages,matriz_assoc,passos_metodos_unicos,novos_metodos_definitions,novos_metodos_steps,caminho_steps_definitions,caminho_steps,caminho_pages,novos_metodos_pages)
                
    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
