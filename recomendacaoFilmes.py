import calculosSimilaridade
import os

diretorio = "../documents/filmes_com_tags"

def encontrar_filme(filme_parcial):
    filmes_encontrados = []
    for arquivo in os.listdir(diretorio):
        if filme_parcial.lower() in arquivo.lower():
            filmes_encontrados.append(arquivo)
    
    if len(filmes_encontrados) == 0:
        return None
    elif len(filmes_encontrados) == 1:
        return filmes_encontrados[0]
    else:
        return filmes_encontrados

def recomendar_filmes(filme, metodo_busca):
    caminho_arquivo = os.path.join(diretorio, filme)
    

    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        tags_filme = file.read()
            
        if metodo_busca == 1:  # vetorial
            filmes_similares = calculosSimilaridade.buscaVetorial(tags_filme)
        else:  # probabilístico
            filmes_similares = calculosSimilaridade.buscaProbabilistica(tags_filme)
                
        if filmes_similares:
            print(f"\nFilmes recomendados para '{filme}':")
            for doc, score in filmes_similares[:10]:  # top 10 resultados
                print(f"{doc} -> {score:.4f} score")
        else:
            print("\nNenhum filme recomendado.")



while True:
    print("\n-- Sistema de Recomendação de Filmes --")
    print("1. Recomendação por modelo Vetorial")
    print("2. Recomendação por modelo Probabilístico")
    print("3. Sair")
        

    opcao = int(input("\nEscolha uma opção -> "))
            
    if opcao == 3:
        break
                
    filme_parcial = input("\nDigite o nome (ou parte do nome) do filme: ")
            
    resultado_busca = encontrar_filme(filme_parcial)
            
    if resultado_busca is None:
        print(f"\nNenhum filme encontrado contendo '{filme_parcial}'.")
    elif isinstance(resultado_busca, list):
        print("\nVários filmes encontrados, seja mais especifico:")
        for i, filme in enumerate(resultado_busca):
            print(f"{i+1}. {filme}")
    else:
        recomendar_filmes(resultado_busca, opcao)
                

