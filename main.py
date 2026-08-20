import binascii

#definição das variáveis globais
ultimo_comando = None
ultimo_dados = None

#definição das funções globais

def exibir_dados(linha, data, hora, dados_bin, tam, control_bytes):
    #Linha bruta
    print("Linha:", linha.strip())

    #mostramos a data e hora
    print("Timestamp", data, hora)

    #mostramos o valor da variavel dados_bin
    print("parseVM: ", dados_bin.hex(" "))

    #Mostramos o tamanho das instruções
    print("Tamanho:", tam)

    #Mostramos os control Bytes
    print("Control Bytes:", control_bytes.hex(" "))


#   definição da função de parseVM
def parseVM(dados_bin, tam):

    if tam<=6:
        print("ACK enviado!")
        return

    #definimos a utilização das variaveis globais
    global ultimo_comando
    global ultimo_dados

    #definimos o comando armazenado em dados_bin[0]
    ultimo_comando = dados_bin[0]
    ultimo_dados = dados_bin

    #separação
    print("\n_____COMANDO_________")

    exibir_dados(linha.strip(), data, hora, dados_bin, tam, control_bytes)

    match ultimo_comando:
        case 0x10 | 0x60:
            print("Comando: Reset")

        case 0x11 | 0x61:
            print("Comando: Setup")
            subcomando = dados_bin[2]
            config_data = dados_bin[2:]
            print("Config data: ", config_data.hex(" "))

            match subcomando:
                case 0x00:
                    for i in range(0, len(config_data), 2):
                        match i:
                            case 2:
                                option = config_data[i]
                                match option:
                                    case 0x01:
                                        print("Config 1: Config relativa a 0x01")

                                    case 0x02:
                                        print("Config 1: Config relativa a 0x02")

                                    case 0x03:
                                        print("Config 1: Config relativa a 0x03")

                            case 4:
                                print("Config 2: Columns on Display. The number of columns on the display. Set to 00H if the display is not available to the reader.")

                            case 6:
                                print("Config 3: Rows on Display. The number of rows on the display")

                            case 8:
                                print("Config 4: ", end="")
                                quarta_config = config_data[i]
                                match quarta_config:
                                    case 0x00:
                                        print("Numbers, upper case letters, blank and decimal point.")

                                    case 0x01:
                                        print("Full ASCII")

                                    case 0x02 | 0x07:
                                        print("Unassigned")

                case 0x01:
                    print("Max/Min prices")
                    for i in range(0, len(config_data), 2):
                        match i:
                            case 2 | 4:
                                print("Y2-Y3")

                            case 6 | 8:
                                print("Y4-Y5")

        case 0x12 | 0x62:
            print("Comando: Poll")
        case 0x13 | 0x63:
            print("Comando: Vend")
        case 0x14 | 0x64:
            print("Comando: Reader")
        case 0x15 | 0x65:
            print("Comando: Revalue")
        case 0x17 | 0x67:
            print("Comando: Expansion")

#   definição da função de parseDevice
def parserDevice(dados_bin, tam):

    #definimos a utilização da variavel global ultimo_comando
    global ultimo_comando

    #separação
    print("\n______RESPOSTA______")

    exibir_dados(linha, data, hora, dados_bin, tam, control_bytes)

    #mostramos a resposta do device
    print("Resposta para o ultimo comando: ", end="")

    match ultimo_comando:
        case 0x10 | 0x60:
            print("#---10")

        case 0x11 | 0x61:
            subcomando = dados_bin[2]
            config_data = dados_bin[2:]
            match subcomando:
                case 0x00:
                    print("Config data: ")
                    for i in range(0, len(config_data), 2):
                        match i:
                            case 2:
                                match config_data[i]:
                                    case 0x01:
                                        print("Config 1: Config relativa a 0x01")

                                    case 0x02:
                                        print("Config 1: Config relativa a 0x02")

                                    case 0x03:
                                        print("Config 1: Config relativa a 0x03")

        case 0x12 | 0x62:
            resp = dados_bin[0]
            match resp:
                case 0x00:
                    print("Just Reset")
                case 0x01:
                    print("Reader Config Data")
                case 0x02:
                    print("Display Request")
                case 0x03:
                    print("Begin Session")
                case 0x04:
                    print("Session Cancel Request")
                case 0x05:
                    print("Vend Approved")
                case 0x06:
                    print("Vend Denied")
                case 0x07:
                    print("End Session")
                case 0x08:
                    print("Cancelled")
                case 0x09:
                    print("Peripheral ID")

        case 0x13 | 0x63:
            print("#---13")

        case 0x14 | 0x64:
            print("#---14")

        case 0x15 | 0x65:
            print("#---15")

        case 0x17 | 0x67:
            print("#---17")

#apertura do arquivo cashless.txt
with open("mdb/cashless.mdb") as arquivo:
    cont = 0
    #definição do nosso dicionário de parse

    #laço for que percorre todas as linhas do arquivo e as define como linha
    for linha in arquivo:
        #Separando a nossa linha
        parts = linha.split(" ", 3)

        #definição das pertes da nossa linha
        data = parts[0]
        hora = parts[1]
        content = parts[3]



        #se for um registro hexadecimal
        if content.startswith("MDB msg: "):

            ini = content.find("B: ") + len("B:")
            fim = content.rfind(")")

            #definimos a variavel dados a partir de content e tiramos os espaços tipo " "
            dados = content[ini + 1 :fim].strip().replace(" ","")

            #definimos a variavel dados como os dois primeiros valores da string dados
            tipo = dados[:2]

            control_bytes = binascii.unhexlify(dados[len(dados)-6:])

            #mudamos o valor de dados ignorando os valores desnecessários para a leitura
            dados = dados[2:-10]

            #utilizando a biblioteca binascii definimos os valores dentro de dados como dados_bin, transformando-os em hex
            dados_bin = binascii.unhexlify(dados)

            #Somente continua se for igual a F1 ou F2
            if not tipo == "F1" or tipo == "F2":
                continue

            #Definição do tamanho da mensagem
            tam = int(content[12:-len(content)+14])

            parseDict = {
                "F1": parseVM,
                "F2": parserDevice
            }

            #criamos a variavel ParseFun como o valor que tem dentro de cada indice do dicionario
            parseFun = parseDict.get(tipo)

            #se parseFun tiver um valor, vai executar a função correspondente ao nome encontrado pelo índice
            if parseFun:
                parseFun(dados_bin, tam)