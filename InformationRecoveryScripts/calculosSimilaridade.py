import json
import preprocessamento
import os
from collections import defaultdict
import math

with open("../documents/data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    arquivoInvertido = data["arquivoInvertido"]
    max_frequencies = data["max_frequencies"]
    tamanho_documentos = data["tamanho_documentos"]
    termosUnicosDocumento = data["termosUnicosDocumento"]

total_documentos = len(os.listdir("../documents/filmes_com_tags")) # total de documentos

def buscaBooleana(consulta):

    tokens = preprocessamento.preProcessamento(consulta) # tokenização da consulta

    # print(tokens)
    
    resultado = set() # armazena cada documento que contém os tokens da consulta
    operador = "OR"  # operador padrão
    
    for token in tokens:
        if token.upper() in ["AND", "OR"]:
            operador = token.upper() 
        else:  #                                         /-> esse .get aqui é pra caso o token não exista no arquivo invertido, ele não dê erro (o usuario pode pesquisar um token que não exista)
            documentos = set(arquivoInvertido.get(token, {}).keys())  # pega o arquivo na posição index (termos) e pega as chaves (documentos) que estão na posicao do token
            
            if not resultado:
                resultado = documentos
            elif operador == "AND":
                resultado &= documentos  # interseção
            elif operador == "OR":
                resultado |= documentos  # união
    
    return resultado

def calculaPeso(termo, documento, freq_consulta, max_freq_consulta):
    df = len(arquivoInvertido.get(termo, {})) # df = numero de documentos que contem o termo
    if documento == "consulta":
        tf = freq_consulta[termo] / max_freq_consulta # tf = frequencia do termo na consulta / frequencia maxima de um termo na consulta (normalização)
    else:
        tf = arquivoInvertido[termo][documento] / max_frequencies[documento] # tf = frequencia do termo no documento / frequencia maxima de um termo no documento (normalização)
    idf = math.log10(total_documentos/df) if df > 0 else 0 # idf = total documentos / numero de documentos que contem o termo
    return (tf * idf)

def buscaVetorial(consulta):

    tokens = preprocessamento.preProcessamento(consulta) # tokenização da consulta

    freq_consulta = defaultdict(int) # guarda a frequencia de cada token na consulta

    tokens_unicos = list(set(tokens)) # pega os tokens unicos da consulta

    for token in tokens:
        if token not in freq_consulta:
            freq_consulta[token] = 1
        else:
            freq_consulta[token] += 1
    max_freq_consulta = max(freq_consulta.values(), default=1) # pega a frequencia maxima da consulta (se nao tiver nenhum termo, o default é = 1)

    scores = defaultdict(float) # guarda o score de cada documento

    documentos_relevantes = set() # guarda os documentos que contém PELO MENOS UM dos tokens da consulta

    for token in tokens:
        documentos_relevantes_lista = list(arquivoInvertido.get(token, {}).keys()) # pega os documentos que contém os tokens da consulta
        for doc in documentos_relevantes_lista:
            documentos_relevantes.add(doc)

    modulo_vetor_consulta = 0
    for token in tokens_unicos:  
        modulo_vetor_consulta += calculaPeso(token, "consulta", freq_consulta, max_freq_consulta)**2
    modulo_vetor_consulta = modulo_vetor_consulta**(1/2) # tira a raiz quadrada

    for documento in documentos_relevantes:
        scores[documento] = 0
        modulo_vetor_documento = 0
        for token in tokens_unicos: # só preciso multiplicar com os tokens que aparecem na consula, pois todos os outros tokens terão peso de consulta 0
            if token in arquivoInvertido: # produto escalar no numerador (vetor consulta * vetor documento)
                scores[documento] += calculaPeso(token, "consulta", freq_consulta, max_freq_consulta)*calculaPeso(token, documento, freq_consulta, max_freq_consulta) if documento in arquivoInvertido[token] else 0

        for termo in termosUnicosDocumento[documento]:
            modulo_vetor_documento += calculaPeso(termo, documento, freq_consulta, max_freq_consulta)**2
        modulo_vetor_documento = modulo_vetor_documento**(1/2) # tira a raiz quadrada

        scores[documento] = scores[documento] / (modulo_vetor_consulta * modulo_vetor_documento) # calcula a similaridade de cossenos
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True) # ordena os documentos por score (decrescente), e retorna uma lista com os documentos e seus scores

def buscaProbabilistica(consulta):

    tokens = preprocessamento.preProcessamento(consulta) # tokenização da consulta

    scores = defaultdict(float) # guarda o score de cada documento

    k1 = 1.2
    k2 = 100
    b = 0.75
    avdll = sum(tamanho_documentos.values()) / total_documentos
    N = total_documentos
    freq_consulta = defaultdict(int) # guarda a frequencia de cada token na consulta

    for token in tokens:
        if token not in freq_consulta:
            freq_consulta[token] = 1
        else:
            freq_consulta[token] += 1

    documentos_relevantes = set() # guarda os documentos que contém PELO MENOS UM dos tokens da consulta

    for token in tokens:
        documentos_relevantes_lista = list(arquivoInvertido.get(token, {}).keys())
        for doc in documentos_relevantes_lista:
            documentos_relevantes.add(doc)

    for documento in documentos_relevantes:
        scores[documento] = 0
        K = k1*((1 - b) + b*(tamanho_documentos[documento]/avdll))
        for token in tokens:
            df = len(arquivoInvertido.get(token, {}))
            tf = (arquivoInvertido.get(token, {})).get(documento, 0) # tf = frequencia do termo no documento
            qf = freq_consulta[token]

            scores[documento] += math.log10((N - df + 0.5)/(df + 0.5)) * ((k1 + 1)*tf)/(K + tf) * ((k2 + 1)*qf)/(k2 + qf)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True) # ordena os documentos por score (decrescente), e retorna uma lista com os documentos e seus scores