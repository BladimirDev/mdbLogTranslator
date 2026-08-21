import binascii

from click import prompt

#definição das variáveis globais
ultimo_comando = None
ultimo_dados = None

#definição das funções globais
def exibir_dados(linha, data, hora, dados_bin, tam, control_bytes):
    #Linha bruta
    print("Linha:", linha.strip())

    #mostramos a data e hora
    print("Timestamp:", data, hora)

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
                                print("VMC Feature Level: ", end='')
                                option = config_data[i]
                                match option:
                                    case 0x01:
                                        print('01')

                                    case 0x02:
                                        print('02')

                                    case 0x03:
                                        print('03')

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
                    for i in range(0, len(dados_bin), 2):
                        match i:
                            case 0:
                                print('Vend Request')
                            case 2:
                                item_price = [dados_bin[i], dados_bin[i+2]]
                                print(int.from_bytes(item_price, byteorder="little"))

                            case 6:
                                item_number = [dados_bin[i], dados_bin[i+2]]
                                print(int.from_bytes(item_number, byteorder="little"))

                #Vend Cancel
                case 0x01:
                    print("Vend Cancel")
                    print('Vend Denied')

                #Vend Sucess
                case 0x02:
                    print('Vend Sucess')
                    item_number = [dados_bin[2], dados_bin[4]]
                    print(int.from_bytes(item_number, byteorder="little"))

                #Vend Failure
                case 0x03:
                    print('Vend Failure')

                #Session Complete
                case 0x04:
                    print("Session complete")

                #Cash Sale
                case 0x05:
                    for i in range(0, len(dados_bin), 2):
                        match i:
                            case 0:
                                print("Cash Sale")
                            case 2:
                                item_price = [dados_bin[i], dados_bin[i+2]]
                                print(int.from_bytes(item_price, byteorder="little"))

                            case 6:
                                item_number = [dados_bin[i], dados_bin[i+2]]
                                print(int.from_bytes(item_number, byteorder="little"))

                #Negative Vend Request
                case 0x06:

                    for i in range(0, len(dados_bin), 2):
                        match i:
                            case 0:
                                print("Negative Vend Request")
                            case 2:
                                item_value = [dados_bin[i], dados_bin[i+2]]
                                print(int.from_bytes(item_value, byteorder="little"))

                            case 6:
                                item_number = [dados_bin[i], dados_bin[i+2]]
                                print(int.from_bytes(item_number, byteorder="little"))

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
                    print('Data Entry Response')
                    print('Data entry data:')
                    print(ascii(dados_bin[2:]))


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
    global ultimo_dados

    #separação
    print("\n______RESPOSTA______")

    exibir_dados(linha, data, hora, dados_bin, tam, control_bytes)

    #mostramos a resposta do device
    print("Resposta para o ultimo comando: ", end="")

    match ultimo_comando:
        #caso Reset
        case 0x10 | 0x60:
            print("Reset")

        #caso Setup
        case 0x11 | 0x61:
            subcomando = ultimo_dados[2]
            config_data = dados_bin
            match subcomando:
                case 0x00:
                    print("Config data:")
                    for i in range(0, len(config_data), 2):

                        match i:
                            case 2: #Z2
                                match config_data[i]:
                                    case 0x01:
                                        print("Reader Feature Level: 01")

                                    case 0x02:
                                        print("Reader Feature Level: 02")

                                    case 0x03:
                                        print("Reader Feature Level: 03")

                            case 4: #Z3-Z4
                                print("Country/ Currency code: ", end='')
                                codigo_ISO = binascii.hexlify(bytearray([config_data[i], config_data[i+2]])).decode()
                                match codigo_ISO[0]:
                                    #fiquei na dúvida como realmente podemos comparar esse valor
                                    case '0':
                                        print('International Telephone Code --', codigo_ISO[1:])
                                    case '1':
                                        print('Latest version of the ISO 4217 --', codigo_ISO[1:])
                            case 6: #Z5
                                print("Scale Factor:", config_data[i])

                            case 10: #Z6
                                print("Decimal Places:", config_data[i])
                            case 12: #Z7
                                print("Application Maximum Response Time - seconds:", config_data[i])
                            case 14: #Z8
                                print("Miscellaneous Options:")
                                misce_options =bin(config_data[i])
                                misce_options = misce_options[::-1]
                                for i in range(len(misce_options[2:])):
                                    match i:
                                        #b0
                                        case 0:
                                            match misce_options[i]:
                                                case '0':
                                                    print('The payment media reader is NOT capable of restoring funds to the user’s payment media or account. Do not request refunds.')

                                                case '1':
                                                    print('The payment media reader is capable of restoring funds to the; user’s payment media or account. Refunds may be requested')
                                        #b1
                                        case 1:
                                            match misce_options[i]:
                                                case '0':
                                                    print('The payment media reader is NOT multivend capable. Terminate session after each vend.')

                                                case '1':
                                                    print('The payment media reader is multivend capable. Multiple items may be purchased within a single session.')
                                        #b2
                                        case 2:
                                            match misce_options[i]:
                                                case '0':
                                                    print('The payment media reader does NOT have a display.')

                                                case '1':
                                                    print('The payment media reader does have its own display.')
                                        #b3
                                        case 3:
                                            match misce_options[i]:
                                                case '0':
                                                    print('The payment media reader does NOT support the VEND/CASH SALE subcommand.')

                                                case '1':
                                                    print('The payment media reader does support the VEND/CASH SALE subcommand.')

        #caso Poll
        case 0x12 | 0x62:
            resp = dados_bin[0]
            config_data = dados_bin
            match resp:
                #Just Reset
                case 0x00:
                    print("Just Reset")

                #Reader Config Data
                case 0x01:
                    print('Config data', config_data)
                    print("Reader Config Data")
                    for i in range(0, len(config_data), 2):

                        match i:
                            case 2: #Z2
                                match config_data[i]:
                                    case 0x01:
                                        print("Reader Feature Level: 01")

                                    case 0x02:
                                        print("Reader Feature Level: 02")

                                    case 0x03:
                                        print("Reader Feature Level: 03")

                            case 4: #Z3-Z4
                                print("Country/ Currency code: ", end='')
                                codigo_ISO = binascii.hexlify(bytearray([config_data[i], config_data[i+2]])).decode()
                                match codigo_ISO[0]:
                                    #fiquei na dúvida como realmente podemos comparar esse valor
                                    case '0':
                                        print('International Telephone Code --', codigo_ISO[1:])
                                    case '1':
                                        print('Latest version of the ISO 4217 --', codigo_ISO[1:])
                            case 6: #Z5
                                print("Scale Factor:", config_data[i])

                            case 10: #Z6
                                print("Decimal Places:", config_data[i])
                            case 12: #Z7
                                print("Application Maximum Response Time - seconds:", config_data[i])
                            case 14: #Z8
                                print("Miscellaneous Options:")
                                misce_options =bin(config_data[i])
                                misce_options = misce_options[::-1]
                                for i in range(len(misce_options[2:])):
                                    match i:
                                        #b0
                                        case 0:
                                            match misce_options[i]:
                                                case '0':
                                                    print('The payment media reader is NOT capable of restoring funds to the user’s payment media or account. Do not request refunds.')

                                                case '1':
                                                    print('The payment media reader is capable of restoring funds to the; user’s payment media or account. Refunds may be requested')
                                        #b1
                                        case 1:
                                            match misce_options[i]:
                                                case '0':
                                                    print('The payment media reader is NOT multivend capable. Terminate session after each vend.')

                                                case '1':
                                                    print('The payment media reader is multivend capable. Multiple items may be purchased within a single session.')
                                        #b2
                                        case 2:
                                            match misce_options[i]:
                                                case '0':
                                                    print('The payment media reader does NOT have a display.')

                                                case '1':
                                                    print('The payment media reader does have its own display.')
                                        #b3
                                        case 3:
                                            match misce_options[i]:
                                                case '0':
                                                    print('The payment media reader does NOT support the VEND/CASH SALE subcommand.')

                                                case '1':
                                                    print('The payment media reader does support the VEND/CASH SALE subcommand.')

                #Display Request
                case 0x02:
                    print("Display Request")
                    for i in range(0, len(config_data), 2):
                        match i:
                            case 2:
                                print('Display time:', config_data[i])

                            case 4:
                                print('Display Data - ASCII')
                                display_data = config_data[4:]
                                print(display_data)

                #Begin Session
                case 0x03:
                    print("Begin Session")
                    print('Founds Avaliable: ', end='')
                    founds_av = [dados_bin[2], dados_bin[4]]
                    match founds_av:
                        case [255, 254]:
                            print("Lesser of the user’s payment media or account balance or FFFEh units.")

                        case [ 255, 255]:
                            print('Not yet determined - FFFFh. (Allows selection without displaying balance)')

                #Session Cancel Request
                case 0x04:
                    print("Session Cancel Request")

                #Vend Aproved
                case 0x05:
                    print("Vend Approved")
                    print('Vend Amount: ', end='')
                    vend_amount = [dados_bin[2], dados_bin[4]]
                    print(int.from_bytes(vend_amount, byteorder="little"))

                #Vend Denied
                case 0x06:
                    print("Vend Denied")

                #End Session
                case 0x07:
                    print("End Session")

                #Cancelled
                case 0x08:
                    print("Cancelled")

        #caso Vend
        case 0x13 | 0x63:
            subcommand = ultimo_dados[2]
            print("Vend")
            match subcommand:
                case 0x00:
                    match dados_bin[0]:
                        #Vend Approved
                        case 0x05:
                            print('Vend Approved')
                            print('Vend Amount: ', end='')
                            vend_amount = [dados_bin[2], dados_bin[4]]
                            print(int.from_bytes(vend_amount, byteorder="little"))

                        case 0x06:
                            print('Vend Denied')

                #Vend Cancel
                case 0x01:
                    print('Vend Cancel')
                    print('Vend Denied')

                #Vend Sucess
                case 0x02:
                    print('Vend Sucess')

                #Vend Failure
                case 0x03:
                    print('Vend Failure')

                #Session Complete
                case 0x04:
                    print('Session Complete')
                    print('End Session')

                #Cash Sale
                case 0x05:
                    print('Cash Sale')

                #Negative Vend Request
                case 0x06:
                    print('Negative Vend Request')
                    match dados_bin[0]:
                        #vend Aproved
                        case 0x05:
                            print('Vend Approved')
                            print('Vend Amount: ', end='')
                            vend_amount = [dados_bin[2], dados_bin[4]]
                            print(int.from_bytes(vend_amount, byteorder="little"))

                        #vend Denied
                        case 0x06:
                            print('Vend Denied')

        #caso Reader
        case 0x14 | 0x64:
            subcommand = ultimo_dados[2]
            print("Reader")
            match subcommand:
                #Reader Disable
                case 0x00:
                    print('#Reader Disable')

                #Reader Enable
                case 0x01:
                    print('#Reader Enable')

                #Reader Cancel
                case 0x02:
                    print('#Reader Cancel')
                    print('Canceled')

                #Data Entry Response
                case 0x03:
                    print('#Data Entry Response')

        #caso Revalue
        case 0x15 | 0x65:
            subcommand = ultimo_dados[2]
            print("Revalue")
            match subcommand:

                #Revalue Request
                case 0x00:
                    print('Revalue Request')
                    match dados_bin[0]:
                        #Revalue Aproved
                        case 0x0D:
                            print('Revalue Aproved')

                        #Revalue Danied
                        case 0x0E:
                            print('Revalue Denied')

                #Revalue Limit Request
                case 0x01:
                    print('Revalue limit Request')
                    match dados_bin[0]:
                        #Revalue Limit Amount
                        case 0x0F:
                            print('Revalue Limit Amount: ', end='')
                            revalue_limit_amount = [dados_bin[2], dados_bin[4]]
                            print(int.from_bytes(revalue_limit_amount, byteorder="little"))
                        case 0x0E:
                            print('Revalue Denied')

        #caso Expansion
        case 0x17 | 0x67:
            subcommand = ultimo_dados[0]
            print("Caso Expansion")
            match subcommand:
                #Request Id
                case 0x00:
                    print('Request Id')
                    print('Peripheral Id')

                #Read User File
                case 0x01:
                    print('Read User File')
                    for i in range(0, len(dados_bin), 2):
                        match i:
                            #User File Data
                            case 0:
                                print('User File Data')

                            #Number of User File
                            case 2:
                                print('Number of the user file: ', end='')

                            #Length of user File
                            case 3:
                                print('Length of user File')

                            #user Data
                            case 4:
                                print('User data:')

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