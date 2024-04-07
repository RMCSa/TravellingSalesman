import random
import math 

# Criação da matriz de distâncias a partir dos dados obtidos no arquivo
distancesDict = {}
with open('src/arquivo.txt', 'r') as arquivo:
    for linha in arquivo:
        distancesDict[int(linha[0:3])] = (int(linha[3:7]), int(linha[7:10]))

# Calculo da distancia euclidiana
def getEuclideanDistance(city1, city2) -> int:
    x1, y1 = distancesDict[city1]
    x2, y2 = distancesDict[city2]
    return int(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

# Criação da matriz de distâncias
def makeDistanceMatriz() -> list:
    distanceMatriz = []
    for i in range(len(distancesDict)):
        distanceMatriz.append([])
        for j in range(len(distancesDict)):
            distanceMatriz[i].append(getEuclideanDistance(i, j))
    return distanceMatriz

# Heurística de inserção mais barata
def cheapest_insertion_heuristic(cities: list) -> list:
    unvisited = cities[:]
    tour = []
    
    # Inicia o tour com uma cidade aleatória
    start_city = 0 #random.choice(unvisited)
    tour.append(start_city)
    unvisited.remove(start_city)
    
    while unvisited:
        minDistance = float('inf')
        bestCityToInsert = None
        bestPositionToInsert = None
        for i, city in enumerate(tour):
            for j, nextCity in enumerate(unvisited):
                # Calcula o custo de inserir nextCity entre city e a próxima cidade no tour
                nextTour = tour[:i+1] + [nextCity] + tour[i+1:]
                distance = get_total_distance(nextTour)
                if distance < minDistance:
                    minDistance = distance
                    bestCityToInsert = nextCity
                    bestPositionToInsert = i + 1
        
        # Insere a cidade não visitada com menor custo na posição ótima no tour
        tour.insert(bestPositionToInsert, bestCityToInsert)
        unvisited.remove(bestCityToInsert)

    tour.append(tour[0])
    return tour

def multiple_traveling_salesmen(nCities: int, numSalesmen: int) -> list:
    citiesPerSalesman = [[0] for _ in range(numSalesmen)]
    numberCitiesPerSalesman = (nCities -1)//numSalesmen;
    for i in range(1,nCities):
        citiesPerSalesman[i % numSalesmen].append(i)

    paths = []
    for citiesForSalesman in citiesPerSalesman:
        path = cheapest_insertion_heuristic(citiesForSalesman)
        paths.append(path)

    return paths

def get_total_distance(tour: list) -> int:
    total_distance = 0
    n_cities = len(tour)

    for i in range(n_cities - 1):
        total_distance += distanceMatriz[tour[i]][tour[i+1]]

    total_distance = total_distance + distanceMatriz[tour[-1]][tour[0]]
    
    return total_distance

distanceMatriz = makeDistanceMatriz()
n_cities = len(distanceMatriz)
numSalesmen = 5
paths = multiple_traveling_salesmen(n_cities, numSalesmen)
for i in paths:
     print(i, get_total_distance(i))
