with open("mdb/cashless.txt") as arquivo:
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
                print(dados)
                dados_separated = dados.split()
                necessary_bytes = dados_separated[1:5]
                print(necessary_bytes)

                match necessary_bytes[0]:
                    case "10" | "60":
                        print("Comando: Reset")
                    case "11" | "61":
                        print("Comando: Setup")
                    case "12" | "62":
                        print("Comando: Poll")
                    case "13" | "63":
                        print("Comando: Vend")
                    case "14" | "64":
                        print("Comando: Reader")
                    case "15" | "65":
                        print("Comando: Revalue")
                    case "17" | "67":
                        print("Comando: Expansion")