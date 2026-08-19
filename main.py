with open("mdb/cashless.mdb") as arquivo:
    for linha in arquivo:
        linha = linha.strip()

        parts = linha.split(" ", 3)

        data = parts[0]
        hora = parts[1]
        sep = parts[2]
        content = parts[3]

        #se for um registro hexadecimal
        if content.startswith("MDB msg: "):

            inicio = content.find("B: ") + len("B:")
            fim = content.rfind(")")
            dados = content[inicio + 1:fim].strip()

            #se o inicio da variavel dados começar por F1 ou F2
            if dados[0]+dados[1] == "F1" or dados[0]+dados[1] == "F2":
                print("_______________________")
                print("Timestamp", data, hora)
                print("!"+ dados +"!")
                dados_separated = dados.split()
