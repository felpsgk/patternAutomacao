# Processamento de Arquivos .feature para Automação de Testes em Java com SerenityBdd

Este projeto em Python tem como objetivo otimizar (automatizando) a geração de arquivos Java para testes automatizados a partir de arquivos .feature usados em Java com Selenium.

## Visão Geral

O projeto utiliza Python para processar arquivos .feature, extrair passos de cenários automatizáveis e gerar automaticamente métodos correspondentes em classes Java para automação de testes. Isso permite automatizar cenários descritos em linguagem natural diretamente em código Java executável.

## Funcionalidades

- **Leitura de Arquivos .feature**: O script lê o conteúdo de arquivos .feature para extrair passos de cenários automatizáveis.
- **Geração Dinâmica de Métodos**: Com base nos passos extraídos, o script gera métodos em classes Java para execução dos testes automatizados.
- **Atualização Automática de Arquivos Java**: Os arquivos Java são automaticamente atualizados com os novos métodos gerados, garantindo a integração com o framework de automação de testes pré-existentes.

## Como Funciona

1. **Leitura de Arquivos .feature**: O script lê o conteúdo dos arquivos .feature na pasta escolhida. Também solicita as pastas StepDefinitions, Steps e Pages
2. **Extração de Passos**: Identifica passos de cenários automatizáveis usando expressões regulares.
3. **Geração de Métodos**: Gera métodos Java correspondentes aos passos extraídos, formatando-os de acordo com as convenções de nomes de método em Java.
4. **Atualização de Arquivos Java**: Atualiza ou cria novos arquivos Java conforme necessário, incorporando os métodos gerados.

## Uso

Para executar o script:

1. Clone o repositório para sua máquina local.
2. Certifique-se de ter Python instalado (versão 3.x).
3. rode "pip install -r reqs.txt" para ter as dependencias necessárias
4. Execute o script Python `main.py`.

Exemplo de comando para execução:
```bash
pip install -r reqs.txt
py main.py
