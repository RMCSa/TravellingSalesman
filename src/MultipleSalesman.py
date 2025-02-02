import random, math 

# Criação da matriz de distâncias a partir dos dados obtidos no arquivo
distance = {}
with open('resources/mTSP-n83-m5.txt', 'r') as arquivo:
    # Use um loop para ler linha por linha
    for linha in arquivo:
        distance[int(linha[0:3])] = (int(linha[3:7]),int(linha[7:10]))

## Calculo da distancia euclidiana
def getEuclideanDistance(city1, city2) -> int:
    x1, y1 = distance[city1]
    x2, y2 = distance[city2]
    return int(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

## Criação da matriz de distâncias
def makeMatriz() -> list:
    matriz = []
    for i in range(len(distance)):
        matriz.append([])
        for j in range(len(distance)):
            matriz[i].append(getEuclideanDistance(i, j))
    return matriz
 
def nearest_neighbor_heuristic(cities: list) -> list:
    unvisited = cities[:]
    tour = []
    
    start_city = unvisited[0]
    tour.append(start_city)
    unvisited.remove(start_city)

    while unvisited:
        nearest_city = min(unvisited, key=lambda city: matriz[tour[-1]][city])
        tour.append(nearest_city)
        unvisited.remove(nearest_city)

    return tour

def multiple_traveling_salesmen(nCities: int, numSalesmen: int) -> list:
    citiesPerSalesman = [[] for _ in range(numSalesmen)]
    cities = list(range(nCities))
    numberCitiesPerSalesman = (nCities -1)//numSalesmen;
    tourCity = nearest_neighbor_heuristic(cities) # Tour inicial com todas as cidades
    if numSalesmen == 1: # Se houver apenas um caixeiro viajante, retorna o tour inicial
        return [tourCity]
    tourCity.pop() 

    # Divide as cidades entre os caixeiros viajantes a partir do tour inicial
    indice = 0 # Variavel criada para controle de indice
    # Para cada caixeiro viajante, adiciona as cidades ao seu tour até que ele tenha o número de cidades desejado:
    for _ in range(numSalesmen):
        while indice == _ :
            if len(citiesPerSalesman[indice]) < numberCitiesPerSalesman and tourCity:
                citiesPerSalesman[indice].append(tourCity.pop(0))
            else:
                indice += 1

    paths = []
    #Heuristica do Vizinho mais proximo para cada caixeiro
    for citiesForSalesman in citiesPerSalesman:
        path = nearest_neighbor_heuristic(citiesForSalesman)
        paths.append(path)

    for i in range(len(paths)):
        paths[i].append(paths[i][0])

    return paths

def get_total_distance(tour: list) -> int:
    total_distance = 0
    n_cities = len(tour)

    for i in range(n_cities - 1):
        total_distance += matriz[tour[i]][tour[i+1]]
    
    return total_distance
    
matriz = makeMatriz()
n_cities = len(matriz)
numSalesmen = 1
paths = multiple_traveling_salesmen(n_cities,numSalesmen)
for i in paths:
     print(i, get_total_distance(i))
