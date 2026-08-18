with open("mdb/cashless.mdb") as arquivo:
    for linha in arquivo: 
        linha = linha.strip()

        partes = linha.split(" ", 3)

        data = partes[0]
        hora = partes[1]
        sep = partes[2]
        conteudo = partes[3]

        print("Timestamp", data, hora)
        
        #se for um registro hexadecimal
        if conteudo.startswith("MDB msg: "):

            inicio = conteudo.find("(")
            fim = conteudo.rfind(")")

            dados = conteudo[inicio + 1:fim].strip()
            print("MDB: " ,dados)

            dados_separados = dados.split() 

            for bit in dados_separados[2:]:
                bin_valor= int(bit, 16)
                print(bin_valor)
            
            # print("Data:", data)
            # print("Hora: ", hora)
            # print("Dados: ",restante)
            print("----------hex------------")

        else:
            # É uma mensagem natural
            # print("Data:", data)
            # print("Hora: ", hora)
            print("Nao e uma mensagem MDB, mas o conteudo e:", conteudo)
            print("----------nat------------")