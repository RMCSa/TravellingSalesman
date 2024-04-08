import random
import math

# Criação da matriz de distâncias a partir dos dados obtidos no arquivo
distance = {}
with open('resources/mTSP-n13-m1.txt', 'r') as arquivo:
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

def farthest_neighbor_heuristic(cities: list) -> list:
    unvisited = cities[:]
    tour = []

    start_city = random.choice(unvisited)
    tour.append(start_city)
    unvisited.remove(start_city)

    while unvisited:
        farthest_city = max(unvisited, key=lambda city: matriz[tour[-1]][city])
        tour.append(farthest_city)
        unvisited.remove(farthest_city)

    return tour

def multiple_traveling_salesmen(nCities: int, numSalesmen: int) -> list:
    citiesPerSalesman = [[] for _ in range(numSalesmen)]
    numberCitiesPerSalesman = (nCities -1)//numSalesmen;
    for i in range(nCities):
        citiesPerSalesman[i % numSalesmen].append(i)
     #Fazer logicas para dividir as cidades entre os caixeiros aleatoriamente

    paths = []
    #Heuristica do Vizinho mais distante para cada caixeiro
    for citiesForSalesman in citiesPerSalesman:
        path = farthest_neighbor_heuristic(citiesForSalesman)
        paths.append(path)
    for i in range(len(paths)):
        paths[i].append(paths[i][0])

    return paths

def get_total_distance(tour: list) -> int:
    total_distance = 0
    n_cities = len(tour)

    for i in range(n_cities - 1):
        total_distance += matriz[tour[i]][tour[i+1]]

    total_distance = total_distance + matriz[tour[-1]][tour[0]]
    
    return total_distance
    
matriz = makeMatriz()
n_cities = len(matriz)
numSalesmen = 2
paths = multiple_traveling_salesmen(n_cities,numSalesmen)
for i in paths:
     print(i, get_total_distance(i))
