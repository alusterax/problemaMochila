from artigo import Artigo
import random
import numpy
##Para melhores resultados, utilizar o método elitista (nao obtive muito sucesso usando a roleta)
##
volumes = [6,2,1,8,2,3,5,9,8,8,6,2,7,9,7,10,2,9,1,9,3,9,9,2,4]
pesos = [2,9,9,7,2,2,3,4,4,7,7,3,7,7,3,4,10,2,5,8,10,2,8,6,7]
valores = [5,7,8,9,2,6,2,1,8,1,8,10,9,6,2,8,6,5,2,7,8,7,9,5,6]

# Gera os itens
ARTIGOS = [Artigo(volumes[x],pesos[x],valores[x]) for x in range (0,25)]

capTotal = 125
popMax = 100
genMax = 200
doisPontosCorte = True
elitista = False
porcentagemPenalizacao = 1
paisTamanho = 100*0.6*0.8

def fitness(target):
    valor_total = 0
    peso_total = 0
    volume_total = 0
    index = 0
    for i in target:
        if index >= len(ARTIGOS):
            break
        if (i == 1):
            valor_total += ARTIGOS[index].valor
            peso_total += ARTIGOS[index].peso
            volume_total += ARTIGOS[index].volume
        index += 1
    #Para cada ponto que passar da capacidade total, vai reduzir 4% por ponto, do valor_total
    if (peso_total > capTotal) or (volume_total > capTotal):
        return valor_total*0.5
    else:
        return valor_total
    ##ARRUMAR
    ##
    ##    valor_total = valor_total - (valor_total*capTotal-125/100)
    ##if (volume_total > capTotal):
    ##    valor_total = valor_total - (valor_total*volume_total-125/100)
    ##return valor_total

def criaPopulacaoInicial(qtd):
    return [criaIndividuo() for x in range (0,qtd)]

def criaIndividuo():
        return [random.randint(0,1) for x in range (0,len(ARTIGOS))]

def mutacao(target):
    # Mutação simples, troca uma posição do array de 0 pra 1 ou vice-versa
    r = random.randint(0,len(target)-1)
    if target[r] == 1:
        target[r] = 0
    else:
        target[r] = 1

def evolucao(pop):
    porcentagemAleatorio = 0.6
    porcentagemParentes = 0.8
    porcentagemMutacao = 0.03
    parentesAleatorios = 0.05
    parentesIniciais = []

    for p in pop: #Escolhe 60% dos invividuos, independente da sua fitness, para entrar no processo de reprodução
        if (numpy.random.random_sample() < porcentagemAleatorio):
            parentesIniciais.append(p)

    parenteLen = int(porcentagemParentes*len(parentesIniciais))
    if (elitista): # Se for elitista, pega os 80% melhores dos 60% aleatórios escohidos acima pra reproduzir, senão usa a roleta para escolher
        parentes = parentesIniciais[:parenteLen]
    else:
        parentes = []
        totalFitnessPop = sum(fitness(individuo) for individuo in parentesIniciais)
        probIndividuos = [fitness(individuo)/totalFitnessPop for individuo in parentesIniciais]
        escolhidos = numpy.zeros(len(parentesIniciais))
        while len(parentes) < paisTamanho:
            for individuos,x in enumerate(probIndividuos):
                if numpy.random.random_sample() < individuos:
                    escolhidos[int(x)] = 1
                    parentes.append(parentesIniciais[int(x)])
    # Aplica mutação na população
    for p in parentes:
        if porcentagemMutacao > random.random():
            mutacao(p)

    # Reprodução
    filhos = []
    tamanhoDesejadoPop = len(pop) - len(parentes)
    while len(filhos) < tamanhoDesejadoPop :
        pai = pop[random.randint(0,len(parentes)-1)]
        mae = pop[random.randint(0,len(parentes)-1)]
        if (doisPontosCorte):
            first = random.randint(0,25)
            last = random.randint(first,25)
            filho = pai[:int(first)] + mae[int(first):int(last)] + pai[int(last):] #Dois pontos de corte.
        else: #corte ao meio
            half = 12
            filho = pai[:int(half)] + mae[int(half):]
        if porcentagemMutacao > random.random(): #Mutação no filho
            mutacao(filho)
        filhos.append(filho)

    parentes.extend(filhos)
    return parentes

def run():
    gen = 1
    population = criaPopulacaoInicial(popMax)
    for g in range(0,genMax):
        population = sorted(population, key=lambda x: fitness(x), reverse=True)
        best = population[0]
        print(f'G: {gen} - Melhor: {best} - Fitness: {fitness(best)}')
        population = evolucao(population)
        gen += 1

run()
