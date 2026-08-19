with open("mdb/cashless.mdb") as arquivo:
    for linha in arquivo: 
        linha = linha.strip()

        parts = linha.split(" ", 3)

        data = parts[0]
        hora = parts[1]
        sep = parts[2]
        content = parts[3]

        print("Timestamp", data, hora)
        
        #se for um registro hexadecimal
        if content.startswith("MDB msg: "):

            inicio = content.find("(")
            fim = content.rfind(")")

            dados = content[inicio + 1:fim].strip()
            print("MDB: " ,dados)

            dados_separated = dados.split()

            for bit in dados_separated[2:]:
                bin_valor= int(bit, 16)
                print(bin_valor)
            print("----------hex------------")

        else:
            print("Nao e uma mensagem MDB, mas o conteudo e:", content)
            print("----------nat------------")