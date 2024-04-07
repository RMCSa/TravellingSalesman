import random, math 

# Criação da matriz de distâncias a partir dos dados obtidos no arquivo
distance = {}
with open('src/arquivo.txt', 'r') as arquivo:
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

def random_solution(cities: list) -> list:
    solution = cities[:]
    random.shuffle(solution)
    return solution

def two_opt(solution: list) -> list:
    improved = True
    while improved:
        improved = False
        for i in range(1, len(solution) - 2):
            for j in range(i + 1, len(solution)):
                if j - i == 1:
                    continue  # No point in reversing two adjacent edges
                new_solution = solution[:]
                new_solution[i:j] = solution[j - 1:i - 1:-1]  # Two opt swap
                if get_total_distance(new_solution) < get_total_distance(solution):
                    solution = new_solution
                    improved = True
        if improved:
            break
    return solution

def multiple_traveling_salesmen(nCities: int, numSalesmen: int) -> list:
    citiesPerSalesman = [[] for _ in range(numSalesmen)]
    cities = list(range(nCities))
    numberCitiesPerSalesman = (nCities -1)//numSalesmen
    for i in range(nCities):
        city = random.choice(cities)
        citiesPerSalesman[i % numSalesmen].append(city)
        cities.remove(city)
        
    paths = []
    #Heuristica do Vizinho mais proximo para cada caixeiro
    for citiesForSalesman in citiesPerSalesman:
        path = random_solution(citiesForSalesman)
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
paths = multiple_traveling_salesmen(n_cities,numSalesmen)
for i in paths:
    i = two_opt(i)
    print(i,"\n", get_total_distance(i))
