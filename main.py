with open("mdb/cashless.mdb") as f:
    lines = f.readlines()

print(lines[2])

#linha = lines[2]

#tms = linha[0:19]
#tamanho = linha[32:35]
#opencode = linha[39:53]
#dados_mdb = linha[42:62]
#control_bytes = linha[54:62]

#print("Time: ", tms)
#print("Tamanho: ", tamanho)
#print("Opencode: ", opencode)
#print("Dados MDB: ", dados_mdb)
#print("Control Bytes:", control_bytes)
#for line in lines:
    #print(line)