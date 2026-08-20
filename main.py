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
        #caso Reset
        case 0x10 | 0x60:
            print("Comando: Reset")

        #caso Setup
        case 0x11 | 0x61:
            print("Comando: Setup")
            subcommand = dados_bin[2]
            config_data = dados_bin[2:]
            print("Config data: ", config_data.hex(" "))

            match subcommand:
                case 0x00:
                    for i in range(0, len(config_data), 2):
                        match i:
                            case 2:
                                option = config_data[i]
                                match option:
                                    case 0x01:
                                        print("The VMC is not capable or will not perform the advanced features as specified in Table 1: COMMANDS & RESPONSES following; Section 7.3.2. The reader will not provide advanced information to; the VMC, but can do the advanced features internally (transparently; to the VMC). The reader has no revaluation capability.")

                                    case 0x02:
                                        print("Config 1: The VMC is capable and willing to perform the advanced features as; specified in Table 1: COMMANDS & RESPONSES following; Section 7.3.2. The reader will provide advanced information to the; VMC (if possible) and will not do the advanced features internally.")

                                    case 0x03:
                                        print("Config 1: The VMC is able to support level 02, but also supports some or all of; the optional features listed in the EXPANSION ID command (i.e., file; transfer, 32 bit credit, multi-currency / language features, negative; vend, and / or data entry).")

                            case 4:
                                print("Columns on Display:", int(config_data[4]))

                            case 6:
                                print("ows on Display:", int(config_data[6]))

                            case 8:
                                print("Display Information: ", end="")
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
                            case 2:
                                max_prices = [config_data[2], config_data[4]]
                                print("Max Price:", int.from_bytes(max_prices, byteorder="little"))
                            case 6:
                                min_price = [config_data[6], config_data[8]]
                                print("Min Price:", int.from_bytes(min_price,  byteorder="little"))

        #caso Poll
        case 0x12 | 0x62:
            print("Comando: Poll")

        #caso Vend
        case 0x13 | 0x63:
            config_data = dados_bin[2:]
            subcommand = dados_bin[2]

            print("Comando: Vend")
            print("Subcomando: ", end="")

            match subcommand:
                #Vend Request
                case 0x00:
                    print("Vend Request")

                #Vend Cancel
                case 0x01:
                    print("Vend Cancel")

                #Vend Sucess
                case 0x02:
                    print('Vend Sucess')

                #Vend Failure
                case 0x03:
                    print('Vend Failure')

                #Session Complete
                case 0x04:
                    print("Session complete")

                #Cash Sale
                case 0x05:
                    print("Cash Sale")

                #Negative Vend Request
                case 0x06:
                    print("Negative Vend Request")

        #caso Reader
        case 0x14 | 0x64:
            config_data = dados_bin[2:]
            subcommand = dados_bin[2]

            print("Comando: Reader")
            print("Subcomando: ", end="")

            match subcommand:
                #Reader Disable
                case 0x00:
                    print('Reader Disable')

                #Reader Enable
                case 0x01:
                    print('Reader Enable')

                #Reader Cancel
                case 0x02:
                    print('Reader Cancel')

                #Data Entry Response
                case 0x03:
                    print('Data Entry; Response')

        #caso Revalue
        case 0x15 | 0x65:
            config_data = dados_bin[2:]
            subcommand = dados_bin[2]

            print("Comando: Revalue")
            print("Subcomando: ", end="")

            match subcommand:
                #Revalue Request
                case 0x00:
                    print('Revalue Request')

                #Revalue Limit Request
                case 0x01:
                    print('Revalue Limit Request')

        #caso Expansion
        case 0x17 | 0x67:
            config_data = dados_bin[2:]
            subcommand = dados_bin[2]

            print("Comando: Expansion")
            print("Subcomando: ", end="")

            match subcommand:
                #Request ID
                case 0x00:
                    print('Request ID')

                #Read User File
                case 0x01:
                    print('Read User File')

                #Write User File
                case 0x02:
                    print('Write User File')

                #White time/Date
                case 0x03:
                    print('White time/Date')

                #Optional No Data Feature Enabled
                case 0x04:
                    print('Optional No Data Feature Enabled')

                #FTL REQ TO RCV
                case 0xFA:
                    print('FTL REQ TO RCV')

                #FTL RETRY / DENY
                case 0xFB:
                    print('FTL RETRY / DENY')

                #FTL SEND BLOCK
                case 0xFC:
                    print('FTL SEND BLOCK')

                #FTL OK TO SEND
                case 0xFD:
                    print('FTL OK TO SEND')

                #FTL REQ TO SEND
                case 0xFE:
                    print('FTL REQ TO SEND')

                #Diagnostics
                case 0xFF:
                    print('Diagnostics')

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
        #caso Reset
        case 0x10 | 0x60:
            print("#---10")

        #caso Setup
        case 0x11 | 0x61:
            subcomando = dados_bin[2]
            config_data = dados_bin[2:]
            match subcomando:
                case 0x00:
                    print("Config data")
                    for i in range(0, len(config_data), 2):
                        match i:
                            case 2: #Z2
                                match config_data[i]:
                                    case 0x01:
                                        print("Config 1: The reader is not capable or will not perform the advanced features as specified in Table 1: COMMANDS & RESPONSES following; Section 7.3.2. The reader will not provide advanced information to; the VMC, but can do the advanced features internally (transparently; to the VMC). The reader has no revaluation capability.")

                                    case 0x02:
                                        print("Config 1: The reader is capable and willing to perform the advanced features as specified in Table 1: COMMANDS & RESPONSES following; Section 7.3.2. The reader will provide advanced information to the; VMC (if possible) and will not do the advanced features internally.")

                                    case 0x03:
                                        print("Config 1: The reader is able to support level 02, but also supports some or all; of the optional features listed in the EXPANSION ID command (i.e.,; file transfer, 32 bit credit, multi-currency / language features,; negative vend, and / or data entry).")

                            case 4: #Z3-Z4
                                print("Country/ Currency code: ")
                                codigo_ISO = hex(config_data[0])
                                print("Tipo de código numérico ISO:", end="")
                                print(codigo_ISO)
                                match codigo_ISO:
                                    #fiquei na dúvida como realmente podemos comparar esse valor
                                    case 0x00:
                                        print('International Telephone Code')
                                    case 0x01:
                                        print('Latest version of the ISO 4217')
                            case 8: #Z5
                                print("Configuração referente a Z5")
                            case 10: #Z6
                                print("Configuração refente a Z6")
                            case 12: #Z7
                                print("Configuração referente a Z7")
                            case 14: #Z8
                                print("Configuração refente a Z8")

                case 0x01:
                    print("No data *")

        #caso Poll
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

        #caso Vend
        case 0x13 | 0x63:
            print("#---13")

        #caso Reader
        case 0x14 | 0x64:
            print("#---14")

        #caso Revalue
        case 0x15 | 0x65:
            print("#---15")

        #caso Expansion
        case 0x17 | 0x67:
            print("#---17")

#apertura do arquivo cashless.txt
with open("mdb/cashless.txt") as arquivo:
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
            if tipo not in ("F1", "F2"):
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