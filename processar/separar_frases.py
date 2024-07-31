class separaFrases:
    
    #separa frases features
    @staticmethod
    def separa_frases(conteudo_feature,passos):
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
        return passos
