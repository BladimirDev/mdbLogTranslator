with open("mdb/cashless.mdb") as f:
    lines = f.readlines()

print(lines[2])

# Data: 2026/08/17 15:55:19
# Tamanho: 18
# Opcode: F1 (Dados recebidos do MDB)
# Dados MDB: 13 01 00 00 02 00 4E 00 00 00 0D 00 70 00
# Bytes controle: 08 01 DB

# 2026/08/17 06:20:19 : MDB msg: (T:8 B: F1 12 01 12 00 00 00 16 )

def separate_line(ls):
    for line in ls:
        timestamp, message = line.split(" : ", 1)

        if message.startswith("MDB msg:"):
            tamanho, message = message.split("T:", 1)
            print("tamanho", tamanho)
            print(timestamp, "É MDB: ", message)

        else:
            print(timestamp, "Nullaw" , message)



print(separate_line(lines))
print(lines[2])