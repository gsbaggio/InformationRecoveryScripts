import os
import json
from collections import defaultdict
import preprocessamento 

def criarData(diretorio):
    arquivoInvertido = defaultdict(lambda: defaultdict(int)) # dicionario - de documentos - guarda outro dificionario - de tokens com sua frequencia
    max_frequencies = defaultdict(int) # guarda a frequencia maxima de cada documento
    tamanho_documentos = defaultdict(int) # guarda o tamanho de cada documento
    termosUnicosDocumento = defaultdict(list) # novo dicionário para termos únicos
    quantidade_documentos = 0 # contador de documentos

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".txt"):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            quantidade_documentos += 1
            print(quantidade_documentos)
            arquivo_sem_txt = arquivo[:-4] # remove o '.txt' do nome do arquivo

            with open(caminho_arquivo, "r", encoding="utf-8") as file:
                conteudo = file.read()
                tokens = preprocessamento.preProcessamento(conteudo)

                tamanho_documentos[arquivo_sem_txt] = len(tokens)
                termosUnicosDocumento[arquivo_sem_txt] = list(set(tokens)) # adiciona lista de tokens únicos

                freq_por_termo = defaultdict(int) # guarda a frequencia de cada token no documento

                for token in tokens:
                    if token not in freq_por_termo:
                        freq_por_termo[token] = 1
                    else:
                        freq_por_termo[token] += 1

                max_freq = max(freq_por_termo.values(), default=1) # pega a frequencia maxima do documento (se nao tiver nenhum termo, o default é = 1)
                max_frequencies[arquivo_sem_txt] = max_freq
                for token, freq in freq_por_termo.items():
                    arquivoInvertido[token][arquivo_sem_txt] = freq # guarda a frequencia do token no documento

    return {
        "arquivoInvertido": arquivoInvertido, 
        "max_frequencies": max_frequencies, 
        "tamanho_documentos": tamanho_documentos,
        "termosUnicosDocumento": termosUnicosDocumento
    }  

def salvarData(conteudo_para_guardar, arquivo_saida):
    with open(arquivo_saida, "w", encoding="utf-8") as file:
        json.dump(conteudo_para_guardar, file, ensure_ascii=False, indent=4)



pasta_documentos = "../documents/filmes_com_tags"

data = criarData(pasta_documentos)
salvarData(data, "../documents/data.json")
