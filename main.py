from processar.gera_arquivos import GeraArquivos
from processar.processa_diretorio import DirManager

# Exemplo de uso
if __name__ == "__main__":
    # Definindo pasta a ser procurada os arquivos java para escrever os arquivos de saída
    directories = [];
    directories = dir_feature, dir_steps_definitions, dir_steps, dir_pages = DirManager.selecionar_pastas();

     # Criando diretórios se não existirem
    dir_manager = DirManager(directories)
    dir_manager.create_directories()

    # Processar todos os arquivos .feature na pasta atual
    feature_processor = GeraArquivos()
    feature_processor.processar_arquivos_feature_recursivamente(dir_feature, dir_steps_definitions, dir_steps, dir_pages)
    
