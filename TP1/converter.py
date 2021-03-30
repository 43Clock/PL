import re
import sys
from functools import reduce

listaNumeros = re.compile(r'^\((\s*[-+]?\s*[0-9]+(\.[0-9]+)?\s*\,)*\s*[-+]?\s*[0-9]+(\.[0-9]+)?\s*\)$')

def stringToList(a): #Transforma uma string numa lista de inteiros/floats
    match = re.search(r'\((.+)\)',a) #Utilizado para obter o que está entre os parentesis
    match_split = re.split(r',',match.group(1)) #Separa cada elemento da string do primeiro grupo de captura pelas virgulas
    nums = []
    for ele in match_split:
        if re.search(r'\.',ele): #Verifica se numero é float
            nums.append(float(ele))
        else:
            nums.append(int(ele))
    return nums

def listOperation(lista,op): #Transforma lista do csv em lista de JSON aplicando a opereção fornecida
    if op == '' or not listaNumeros.search(lista): #Verifica se operação é nula ou se a lista não é só de numeros
        if not listaNumeros.search(lista): #Se não for só de numero transforma numa lista de strings
            lista = re.sub(r'\(',r'["',lista)
            lista = re.sub(r'\)',r'"]',lista)
            lista = re.sub(r',',r'","',lista)
        else: #Senão transforma numa lista de Numeros
            lista = re.sub(r'\(',r'[',lista)
            lista = re.sub(r'\)',r']',lista)
        return lista
    elif op == 'avg': #Se operação for avg, calcula a média dos numeros
        nums = stringToList(lista)
        return str(reduce(lambda a,b:a+b,nums)/len(nums))
    elif op == 'sum': #Se operação for sum, calcula a soma dos numeros
        nums = stringToList(lista)
        return str(reduce(lambda a,b:a+b,nums))
    elif op == 'max': #Se operação for max, calcula o maior dos numeros
        nums = stringToList(lista)
        return str(reduce(lambda a,b: a if a>b else b,nums))
    elif op == 'min': #Se operação for min, calcula o menor dos numeros
        nums = stringToList(lista)
        return str(reduce(lambda a,b: b if a>b else a,nums))
    

def transform(first_line,linha):
    linha = re.split(r';',linha) #Sepera a primeira linha por ;
    for i in range(len(first_line)): #Percorre cada um dos elementos da linha a transformar
        if re.search(r'\*',first_line[i]): #Verifica se é ou não uma lista
            splited_first = re.split(r'\*',first_line[i].strip()) #Separa pelo * para ver as operações a realizar na lista (pode ter multiplas)
            ops = re.split(r',',splited_first[1]) #Separa pela , cada uma das operações
            if listaNumeros.search(linha[i]): #Verifica se parcela tem apenas numeros (para verificar se é possivel fazer operações)
                for j in range(len(ops)): #Percorre cada uma das operações
                    if ops[j] == '': #Se a operação for nula, imprime sem o nome da operação
                        output.write(f"\t\t\"{splited_first[0].strip()}\": {listOperation(linha[i].strip(),ops[j].strip())}")
                    else: #Caso contrario imprime com o nome da operação
                        output.write(f"\t\t\"{splited_first[0].strip()}_{ops[j].strip()}\": {listOperation(linha[i].strip(),ops[j].strip())}")
                    if i == len(first_line)-1 and j == len(ops)-1:
                        output.write("\n")
                    else:
                        output.write(",\n")
            else: # Se tiver operações e a lista não for de apenas numeros, imprime apenas uma vez a lista e sem o nome das operações
                output.write(f"\t\t\"{splited_first[0].strip()}\": {listOperation(linha[i].strip(),'')}")
                if i == len(first_line)-1:
                    output.write("\n")
                else:
                    output.write(",\n")
        else: #Se não for uma lista imprime apenas os valores com os respetivos nomes
            if re.search(r'^\s*[-+]?\s*[0-9]+(\.[0-9]+)?$',linha[i]):
                if re.search(r'\.',linha[i]):
                    output.write(f"\t\t\"{first_line[i].strip()}\": {float(linha[i].strip())}")
                else:
                    output.write(f"\t\t\"{first_line[i].strip()}\": {int(linha[i].strip())}")
            else:
                output.write(f"\t\t\"{first_line[i].strip()}\": \"{linha[i].strip()}\"")
            if i == len(first_line)-1:
                output.write("\n")
            else:
                output.write(",\n")

with open(str(sys.argv[1])) as f:
    linhas = f.readlines()
    first_line = re.split(r';',linhas[0].strip())
    output_name = re.split(r'\.',sys.argv[1])
    output = open(f'{output_name[0]}.json','w') #Abre ficheiro para escrita com nome igual mas com formato json
    output.write("[\n")
    for i in range(1,len(linhas)):
        output.write("\t{\n")
        transform(first_line,linhas[i]) #Executa função de transformação para cada linha do csv
        if i == len(linhas)-1:
            output.write("\t}\n")
        else: 
            output.write("\t},\n")
    output.write("]")
    output.close()