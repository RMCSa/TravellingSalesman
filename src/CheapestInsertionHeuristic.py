import random
import math 

# Criação da matriz de distâncias a partir dos dados obtidos no arquivo
distance = {}
with open('src/arquivo.txt', 'r') as arquivo:
    for linha in arquivo:
        distance[int(linha[0:3])] = (int(linha[3:7]), int(linha[7:10]))

# Calculo da distancia euclidiana
def getEuclideanDistance(city1, city2) -> int:
    x1, y1 = distance[city1]
    x2, y2 = distance[city2]
    return int(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

# Criação da matriz de distâncias
def makeMatriz() -> list:
    matriz = []
    for i in range(len(distance)):
        matriz.append([])
        for j in range(len(distance)):
            matriz[i].append(getEuclideanDistance(i, j))
    return matriz

# Heurística de inserção mais barata
def cheapest_insertion_heuristic(cities: list) -> list:
    unvisited = cities[:]
    tour = []
    
    # Inicia o tour com uma cidade aleatória
    start_city = random.choice(unvisited)
    tour.append(start_city)
    unvisited.remove(start_city)
    
    while unvisited:
        min_cost = float('inf')
        best_city_to_insert = None
        best_position_to_insert = None
        for i, city in enumerate(tour):
            for j, next_city in enumerate(unvisited):
                # Calcula o custo de inserir next_city entre city e a próxima cidade no tour
                next_tour = tour[:i+1] + [next_city] + tour[i+1:]
                cost = get_total_distance(next_tour)
                if cost < min_cost:
                    min_cost = cost
                    best_city_to_insert = next_city
                    best_position_to_insert = i+1
        
        # Insere a cidade não visitada com menor custo na posição ótima no tour
        tour.insert(best_position_to_insert, best_city_to_insert)
        unvisited.remove(best_city_to_insert)
    
    return tour

def multiple_traveling_salesmen(nCities: int, numSalesmen: int) -> list:
    citiesPerSalesman = [[] for _ in range(numSalesmen)]
    numberCitiesPerSalesman = (nCities -1)//numSalesmen;
    for i in range(nCities):
        citiesPerSalesman[i % numSalesmen].append(i)

    paths = []
    for citiesForSalesman in citiesPerSalesman:
        path = cheapest_insertion_heuristic(citiesForSalesman)
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
numSalesmen = 1
total_distance = 0
path = []
paths = multiple_traveling_salesmen(n_cities, numSalesmen)

for i in paths:
     print(i, get_total_distance(i))
