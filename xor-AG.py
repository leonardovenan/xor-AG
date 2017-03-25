import numpy as np

MAX_GEN = 10000
TAM_POP = 30
TAM_CROM = 15
TX_CROSS = 0.8
TX_MUT = 0.1

def GeraPop():                       #linha   coluna 
    return (np.random.randint(0,20, [TAM_POP,TAM_CROM])-10) # gera uma populacao de crom de pesos aleatorios
    # entre -10 a 10 com 15 pesos 
    
def sigmoid(x): #retorna sigmoide de um valor , tive que fazer pq no python nao tem  
    return 1 / (1 + np.exp(-x)) # usei pra fazer testes antes da tanh 
    
def CalculaRede(pesos, x1, x2): # pesos - valores gerados em GeraPop , x1 entrada 0 ou 1, x2 0 e 1 tbm
    y0b = np.tanh(x1*pesos[1] + x2*pesos[3] + pesos[10])  #calculo da rede
    y0a = np.tanh(x1*pesos[0] + x2*pesos[2] + pesos[11])
    y1b = np.tanh(y0a*pesos[5] + y0b*pesos[7] + pesos[12])
    y1a = np.tanh(y0a*pesos[4] + y0b*pesos[6] + pesos[13])
    y2 = (y1a*pesos[8] + y1b*pesos[9] + pesos[14])
    return sigmoid(y2) #valor de saida

def Aptidao(x):  #funcao de maximizacao
    y1 = abs(CalculaRede(x,0,0)) # erro 1 - |0 - x|
    y2 = abs(1 - CalculaRede(x,0,1)) # erro 2 - |1-x|
    y3 = abs(1 - CalculaRede(x,1,0)) # erro 3 - |1-x|
    y4 = abs(CalculaRede(x,1,1)) # erro 4 - |0-x|
    erro = (y1+y2+y3+y4) #erro total
    return 1/erro #esse erro tem que ir pra 0, ser minimizado 
    
def CalculaAptidoes(pop): #calculo da aptidao da populacao 
    return [Aptidao(x) for x in pop] #retorna uma lista de aptidoes de cada cromossomo 

def SelecaoRoleta(aptidoes):  # reutilizei 
    percentuais = np.array(aptidoes)/float(sum(aptidoes))
    vet = [percentuais[0]]
    for p in percentuais[1:]:
        vet.append(vet[-1]+p)
    r = np.random.random()
    for i in range(len(vet)):
        if r <= vet[i]:
            return i
            
def Cruzamento(pai,mae): 
    r1 = np.random.random() #por porcentagem
    r2 = 1-r1
    filho = (r1*pai + r2*mae)
    filha = (r2*pai + r1*mae)
    return filho, filha
   # corte = np.random.randint(TAM_CROM)  #do professor
   # return (list(pai[:corte])+list(mae[corte:]),list(mae[:corte])+list(pai[corte:]))

def Mutacao(cromossomo):
    r1 = np.random.randint(TAM_CROM) #gera um numero interira aleatoria de 1 a 15 local do vetor
    r2 = np.random.rand()*20 -10  #gera numero real de 0 a 1 multiplica por 20 e sublitrai 10
    cromossomo[r1] = (cromossomo[r1] + r2)/2 #pega o cromossomo na local r1 e vai somar com r2 e dividir por 2
    return cromossomo

pop = GeraPop()

for g in range(MAX_GEN):  # maximo de geracoes  
    aptidoes = CalculaAptidoes(pop)  # Quanto maior melhor 
    print (np.mean(aptidoes)) #media aptidoes 
    nova_pop = [] 
    for c in range(int(TAM_POP/2)): #vai completar ate que o tamanho da populacao nova seja metade da populacao definida 
        pai = pop[SelecaoRoleta(aptidoes)] # por conta dos crossovers 
        mae = pop[SelecaoRoleta(aptidoes)] # gira roleta 
        r = np.random.random() #gera numero aleatorio 
        if r <= TX_CROSS: # se r menor Taxa de cross ha cruzamento 
            filho,filha = Cruzamento(pai,mae) #reaproveitando 
        else:
            filho,filha = pai,mae

        r = np.random.random()
        if r <= TX_MUT:
            filho = Mutacao(filho)
        r = np.random.random()
        if r <= TX_MUT:
            filha = Mutacao(filha)
            
        nova_pop.append(filho) #adiciona na nova_pop 
        nova_pop.append(filha)
    
    pop = np.array(nova_pop) # apenas para padronizar 
    
aptidoes = CalculaAptidoes(pop)

index_solucao = aptidoes.index(max(aptidoes)) #retorna o indice de maior aptidao

print (pop[index_solucao]) #printa o melhores pesos para calcular o xor 

                     #colocar no console 

# 1 - teste = pop[index_solucao]  2 - CalculaRede( pesos, x1, x2)