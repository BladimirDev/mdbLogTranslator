import binascii

#definição das variáveis globais
ultimo_comando = None
ultimo_dados = None

#definição das funções globais

#   definição da função de parseVM
def parseVM(dados_bin):

    #definimos a utilização das variaveis globais
    global ultimo_comando
    global ultimo_dados

    #definimos o comando armazenado em dados_bin[0]
    ultimo_comando = dados_bin[0]
    ultimo_dados = dados_bin

    #separação
    print("\n_____COMANDO_________")

    #mostramos a data e hora
    print("Timestamp", data, hora)

    #mostramos o valor da variavel dados_bin
    print("parseVM: ", dados_bin)


    match ultimo_comando:
        case 0x10 | 0x60:
            print("Comando: Reset")
        case 0x11 | 0x61:
            print("Comando: Setup")
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
def parserDevice(dados_bin):

    #definimos a utilização da variavel global ultimo_comando
    global ultimo_comando

    #separação
    print("\n______RESPOSTA______")

    #mostramos a data e hora
    print("Timestamp:", data, hora)

    #mostramos o valor da variavel dados_bin
    print("parseDevice:", dados_bin)

    #mostramos a resposta do device
    print("Resposta para o ultimo comando: ", end="")

    match ultimo_comando:
        case 0x10 | 0x60:
            print("#---10")

        case 0x11 | 0x61:
            print("#---11")

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
with open("mdb/cashless.txt") as arquivo:

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

            #mudamos o valor de dados ignorando os valores desnecessários para a leitura
            dados = dados[2:-6]

            #utilizando a biblioteca binascii definimos os valores dentro de dados como dados_bin, transformando-os em hex
            dados_bin = binascii.unhexlify(dados)


            parseDict = {
                "F1": parseVM,
                "F2": parserDevice
            }

            #criamos a variavel ParseFun como o valor que tem dentro de cada indice do dicionario
            parseFun = parseDict.get(tipo)


            #se parseFun tiver um valor, vai executar a função correspondente ao nome encontrado pelo índice
            if parseFun:
                parseFun(dados_bin)