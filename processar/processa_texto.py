from unidecode import unidecode
import re

class TextProcessor:
   
    # Função para remover acentos de uma string
    @staticmethod
    def remover_acentos(texto):
        return unidecode(texto)
    
    @staticmethod
    def substituir_aspas_por_string(texto):
        padrao = r"'([^']*)'"
        return re.sub(padrao, r"{string}", texto)
    
    @staticmethod
    def remover_texto_dentro_string(texto):
        padrao = r"'([^']*)'"
        return re.sub(padrao, r"", texto)
    
