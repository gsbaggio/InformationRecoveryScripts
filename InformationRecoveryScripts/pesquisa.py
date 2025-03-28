import calculosSimilaridade

while True:

    metodo_consulta = int(input("Digite o método de consulta desejado:\n 1 = Booleano\n 2 = Vetorial\n 3 = Probabilístico\n 4 = Sair\n"))

    if(metodo_consulta == 1):
        print("\n-- Consulta booleana --\n")

        consulta = input("\nDigite sua busca (use AND / OR entre tokens) ->  ")
        
        documentos = calculosSimilaridade.buscaBooleana(consulta)

        if documentos:
            print("\nDocumentos encontrados:", documentos)
        else:
            print("\nNenhum documento encontrado para essa consulta.")

        print("\n\n\n")

    elif(metodo_consulta == 2):
        print("\n-- Consulta vetorial --\n")

        consulta = input("\nDigite sua busca ->  ")
        
        documentos = calculosSimilaridade.buscaVetorial(consulta)
        
        if documentos:
            print("\nDocumentos mais relevantes:")
            for doc, score in documentos[:5]:  # top 5 resultados
                print(f"{doc} -> {score:.4f} score")
        else:
            print("\nNenhum documento relevante encontrado.")

        print("\n\n\n")

    elif(metodo_consulta == 3):
        print("\n-- Consulta probabilística --\n")

        consulta = input("\nDigite sua busca ->  ")

        documentos = calculosSimilaridade.buscaProbabilistica(consulta)

        if documentos:
            print("\nDocumentos mais relevantes:")
            for doc, score in documentos[:5]:  # top 5 resultados
                print(f"{doc} -> {score:.4f} score")
        else:
            print("\nNenhum documento relevante encontrado.")

    else:
        break