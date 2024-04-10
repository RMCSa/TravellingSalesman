'''
    Autores: Rafael Moreira Cavalcante de Souza  - 23333
             Vitor Henrique Paes                 - 23340
    Algoritmo de inserção mais barata feito da nossa forma para o problema dos multiplos caixeiros viajantes
'''
#Bibliotecas utilizadas
import random # Biblioteca para gerar números aleatórios
import math # Biblioteca para funções matemáticas

# Criação de um dicionário de distâncias (x,y) a partir dos dados obtidos no arquivo
# (A obtencão dos dados também poderia ser armazenada em uma lista de tuplas, mas optamos por utilizar um dicionário para facilitar a busca de uma cidade específica)
distancesDict = {}
with open('resources/mTSP-n91-m5.txt', 'r') as arquivo:
    for linha in arquivo:
        distancesDict[int(linha[0:3])] = (int(linha[3:7]), int(linha[7:10]))

# Calculo da distancia euclidiana entre duas cidades
def getEuclideanDistance(city1, city2) -> int:
    x1, y1 = distancesDict[city1] # Coordenadas da cidade 1
    x2, y2 = distancesDict[city2] # Coordenadas da cidade 2
    return int(math.sqrt((x1 - x2)**2 + (y1 - y2)**2)) # Retorna a distância euclidiana em int

# Criação da matriz de distâncias
def makeDistanceMatriz() -> list:
    distanceMatriz = []
    #Para cada cidade i, calcula a distância para todas as outras cidades j e armazena na matriz.
    for i in range(len(distancesDict)): 
        distanceMatriz.append([]) # Adiciona uma lista vazia para cada cidade
        for j in range(len(distancesDict)): 
            distanceMatriz[i].append(getEuclideanDistance(i, j)) #Adiciona as distancias correspondesntes
    return distanceMatriz # Retorna a matriz de distâncias

# Heurística de inserção mais barata, recebendo uma lista de cidades e retornando o tour resultante
def cheapest_insertion_heuristic(cities: list) -> list: 
    unvisited = cities[:] # Cidades não visitadas (cópia da lista de cidades)
    tour = [] # Criacao do tour
    
    # Inicia o tour com a primeira cidade da lista recebida
    start_city = unvisited[0] # Cidade inicial
    tour.append(start_city) # Add na lista de tours
    unvisited.remove(start_city) # Remove da lista de cidades não visitadas

    # Enquanto houver cidades não visitadas, encontra a cidade não visitada com menor custo de inserção e insere ela no tour
    while unvisited:
        minDistance = float('inf') # Significa que o valor é infinito
        bestCityToInsert = None # Melhor cidade para inserir
        bestPositionToInsert = None # Melhor posição para inserir

        # Para cada cidade no tour e para cada cidade não visitada, calcula o custo de inserir a cidade não visitada entre a cidade atual e a próxima cidade no tour
        for i, city in enumerate(tour): 
            for nextCity in unvisited:
                nextTour = tour[:i+1] + [nextCity] + tour[i+1:]
                distance = get_total_distance(nextTour) #Custo de inserir na posição
                # Se o custo for menor que o menor custo encontrado até agora, atualiza o menor custo e a melhor cidade e posição para inserir
                if distance < minDistance: 
                    minDistance = distance
                    bestCityToInsert = nextCity
                    bestPositionToInsert = i + 1
        
        # Insere a cidade não visitada com menor custo na melhor posição no tour e logo após remova ela da lista de unvisited
        tour.insert(bestPositionToInsert, bestCityToInsert)
        unvisited.remove(bestCityToInsert)
    
    tour.append(tour[0]) # Adiciona a primeira cidade no final do tour para fechar o ciclo
    return tour # Retorna o tour

# Função para dividir as cidades entre os múltiplos caixeiros viajantes e encontrar o caminho ideal para cada um:
def multiple_traveling_salesmen(nCities: int, numSalesmen: int) -> list:
    citiesPerSalesman = [[] for _ in range(numSalesmen)] # Gera listas por caixeiro viajante
    cities = list(range(nCities)) # Lista de cidades
    numberCitiesPerSalesman = (nCities -1)//numSalesmen # Número de cidades por caixeiro viajante
    tourCity = cheapest_insertion_heuristic(cities) # Tour inicial com todas as cidades
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

    # A Partir dos tours criados, aplica a heurística de inserção mais barata para cada caixeiro viajante, encontrando o caminho ideal para cada um:
    tour = []
    for index, citiesForSalesman in enumerate(citiesPerSalesman):
        if index == 0:
            citiesForSalesman.append(citiesForSalesman[0])
            tour.append(citiesForSalesman)
            continue;
        path = cheapest_insertion_heuristic(citiesForSalesman)
        tour.append(path)

    return tour # Retorna a lista de tours por vendedor

# Função para calcular a distância total de um tour qualquer
def get_total_distance(tour: list) -> int:
    total_distance = 0
    # Para cada cidade no tour, calcula a distância entre ela e a próxima cidade e soma na distância total
    for i in range(len(tour) -1 ):
        city1 = tour[i]
        city2 = tour[i + 1]
        total_distance += distanceMatriz[city1][city2]

    return total_distance # Retorna a distância total

distanceMatriz = makeDistanceMatriz() # Cria a matriz de distâncias
n_cities = len(distanceMatriz) # Número de cidades
numSalesmen = 1 # Número de caixeiros viajantes
tour = multiple_traveling_salesmen(n_cities, numSalesmen) 
for i in tour:
    print(i, get_total_distance(i)) 


    
