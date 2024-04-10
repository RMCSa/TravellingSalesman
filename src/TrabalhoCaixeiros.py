
import math
import random


#funcao para calcular a distancia entre duas cidades(sera usada na funcao de leitura do arquivo)
def CalcularDistanciaPorCordenadas(cordenadas1, cordenadas2):
    x1 = cordenadas1[0]
    y1 = cordenadas1[1]
    x2 = cordenadas2[0]
    y2 = cordenadas2[1]
    #calculo para pegar a distancia entre duas cordenadas
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return  int (distancia)

#lista das cordenadas recebidas pelo arquivo txt
ListaCordenadas = []

#lista das distancias entre as cidades (formato de matriz)
listaDistancias = []
cities = list(range(len(listaDistancias)))


with open('resources/mTSP-n91-m5.txt', 'r') as arquivo:
    #pegara cada linha do arquivo e inserirá na posicao do vetor correspondente as cordenadas X e Y

    for line in arquivo:              #posicao         #X              #Y
        ListaCordenadas.insert(int (line[0:3]), (int (line[3:7]), int (line[7:10])))


    #para cada cordenada, calcular a distancia entre ela e todas as outras cordenadas
    for i in range(len(ListaCordenadas)):

        #criar uma lista para a distancia de cada cidade em relacao as outras
        listaDistancias.append([])

        for x in range(len(ListaCordenadas)):

            listaDistancias[i].append(CalcularDistanciaPorCordenadas(ListaCordenadas[i], ListaCordenadas[x]))


#lista de cidades
cities = list(range(len(listaDistancias)))


# Lista de caixeiros com suas rotas
ListaCidadesDosCaixeiros = []

#funcao que divide as cidades entre os caixeiros
def DividirEntreCaixeiros(caixeiros: int):
    #clonagem de cities
    Cidades = cities[:]

    #cria uma lista para cada caixeiro
    for i in range(caixeiros):
        ListaCidadesDosCaixeiros.append([])

    #adiciona uma cidade no caixeiro 1, depois no 2, depois no 3... e assim por diante até que o chege na posicao final
    indice = 0
    for x in range(len(Cidades)):
        #se x for impar, muda o caixeiro
        if x % 2 != 0:
            indice += 1
        #se o indice for igual ao numero de caixeiros, volta para o primeiro caixeiro
        if indice == caixeiros:
                indice = 0
        
        #escollhe uma cidade aleatoria e adiciona no caixeiro
        cidade = random.choice(Cidades)
        ListaCidadesDosCaixeiros[indice].append(cidade)
        #remove a cidade da lista de cidades para que ela nao seja adicionada novamente
        Cidades.remove(cidade)

    #funcao que pega as cidade mais proximas e as ordena dentro de uma rota
def nearest_neighbor_heuristic(cities: list):

    #clone das cidades
    unvisited = cities[:]
    #separará as cidades de forma aleatoria entre os caixeiros
    cidadeInicial = random.choice(unvisited)
    #para comecar a rota pela cidade inicial
    Rota = [cidadeInicial]
    #remove a cidade inicial da lista de cidades nao visitadas
    unvisited.remove(cidadeInicial)

    
    #While que pega a distancia minima entre a ultima cidade visitada e a proxima cidade
    while(unvisited):    
        #candidate eh cada valor detro de unvisited, essa func lambda percorre cada cidade de unvisited e pega a distancia minima, ou seja, cidade mais proxima
        next = min(unvisited, key= lambda candidate: listaDistancias[Rota[-1]][candidate])
        #adiciona a cidade mais proxima na rota
        Rota.append(next)
        #remove a cidade mais proxima da lista unvisited
        unvisited.remove(next)
    
    #adiciona na ultima posicao a cidade inicial para q o caixeiro volte para ela no final do percurso
    Rota.append(cidadeInicial)
    return Rota;


#funcao para pegar a distancia total de uma rota
def get_total_distance(Rota: list):
    total_distance = 0
    
    #para cada cidade na rota, pegar a distancia entre ela e a proxima cidade
    for i in range(len(Rota)-1):
        total_distance += listaDistancias[Rota[i]][Rota[i+1]]

    #pegar a distancia entre a ultima cidade e a primeira
    total_distance = total_distance + listaDistancias[Rota[-1]][Rota[0]]
    
    return total_distance


def MultiplosCaixeiros():
    DividirEntreCaixeiros(1)
    
    for i in range(len(ListaCidadesDosCaixeiros)):
        Rota = nearest_neighbor_heuristic(ListaCidadesDosCaixeiros[i])
        print(f"caixeiro{i+1}: {Rota} Distancia total:  {get_total_distance(Rota)}")
    



MultiplosCaixeiros()

    



