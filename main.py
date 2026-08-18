with open("mdb/cashless.mdb") as f:
    lines = f.readlines()

print(lines[2])

# def ler_documento(caminho):
#     with open(caminho) as arquivo:
#         return arquivo.readlines()


def separate_line(lines):
    for line in lines:
        timestamp, message = line.split(" : ", 1)

        if message.startswith("MDB msg:"):
            print(timestamp, "É MDB: ", message)
        else:
            print(timestamp, "Nullaw" , message)

print(separate_line(lines))