'''
@author Jay Banerji
43312942
COMP329 Assignment 2 Genetic Algorithms File
Acknowledgements:
    https://www.saltycrane.com/blog/2007/09/how-to-sort-python-dictionary-by-keys/
    https://stackoverflow.com/questions/10324015/fitness-proportionate-selection-roulette-wheel-selection-in-python
    http://www.keithschwarz.com/darts-dice-coins/
    http://www.edc.ncl.ac.uk/highlight/rhjanuary2007g04.php
    http://www.edc.ncl.ac.uk/highlight/rhjanuary2007g03.php
    http://www.edc.ncl.ac.uk/highlight/rhjanuary2007g02.php/
    http://www.edc.ncl.ac.uk/highlight/rhjanuary2007g01.php/
    https://stackoverflow.com/questions/6660069/linear-fitness-scaling-in-genetic-algorithm-produces-negative-fitness-values
    https://wordforge.net/index.php?threads/tit-for-tat-axelrods-simulation-of-competition-and-cooperation.45019/
    https://www.iitk.ac.in/kangal/seminar/shashi.pdf
    https://www.cs.umd.edu/users/golbeck/downloads/JGolbeck_prison.pdf
'''

from axelrod.action import Action
from axelrod.player import Player
from axelrod import lookerup
import itertools, axelrod as axl, random

C, D = Action.C, Action.D

#have these global just to be sure
global  initHistoryPlayer, popCount

#define memory depth and population size
memorydepth = 2
popCount = 100


def stringGenerator():
    '''
    This function generates the string from which the random binary is converted into action sequences
    '''
    global initHistoryPlayer
    initStr = randomiser()
    initInd = initStr[:pow(4,memorydepth)]
    initVec = initStr[pow(4,memorydepth):]
    initVector = ''
    for q in initVec:
        if q =='0':
            initVector = initVector + 'C'
        elif q=='1':
            initVector = initVector + 'D'
    #initHistories = list([i+j for i,j in zip(initVector[::2], initVector[1::2])])
    initHistoryPlayer = initVector
    #print(initHistoryPlayer)
    #print(initHistoryOpponent)
    possiblePlays = ['CC','CD','DC','DD']
    stratCombs = itertools.product(possiblePlays,repeat=memorydepth)
    stratList = []
    for n in stratCombs:
        stratList = stratList + [n]
    stratString = ""
    for z in initInd:
        if z =='0':
            stratString = stratString + "C"
        elif z=='1':
            stratString = stratString + "D"
    dictPlays = dict(zip(stratList,stratString))
    #print(''.join(dictPlays.values()))
    print(dictPlays)
    return dictPlays

def randomiser():
    '''
    This function generates the random bit string
    '''
    stringlength = pow(4,memorydepth) + memorydepth
    mystring = ""
    for i in range(0,stringlength):
        bit = str(random.randint(0,1))
        mystring = mystring + bit
    return mystring
    
def initialisePopulation(testpoplist=[]):
    '''
    This function creates the initial population to be evolved
    '''
    global initPopulation, initHistoryPlayer, popCount
    stratList = []
    while len(stratList) != popCount:
        stratString = ''.join(stringGenerator().values())
        stratString = initHistoryPlayer + stratString
        if stratString not in stratList:
            stratList = stratList + [stratString]
            #using LookerUp constructor
            testpoplist = testpoplist + [
                axl.LookerUp(initial_actions=axl.action.str_to_actions(stratString[:memorydepth]), 
                        pattern= stratString[memorydepth:], 
                        parameters=lookerup.Plays(self_plays=2, op_plays=2, op_openings=0))
                ]
    return testpoplist

def playTournament(populations):
    '''
    This function runs the tournament and returns a dictionary of strategyStrings:fitnessVals
    '''
    players = populations
    tournament = axl.Tournament(players, turns=5, repetitions=1)
    #results = tournament.play()
    results = tournament.play(keep_interactions=True)
    #create score dictionary of string sequence and initialize to 0
    midlist =[]
    for n in tournament.players:
        valslist = ''
        for x in n.initial_actions:
            valslist = valslist + str(x)
        for l in n.lookup_dict.values():
            valslist = valslist + str(l)
        midlist = midlist + [valslist]
    scoredict = {el:[0,0] for el in midlist}
    #from axelrod test file
    for index_pair, interaction in sorted(results.interactions.items()):
        player1 = tournament.players[index_pair[0]]
        player2 = tournament.players[index_pair[1]]
        #create keys to access scoredict
        keylist =[]
        for n in (player1, player2):
            valslist = ''
            for x in n.initial_actions:
                valslist = valslist + str(x)
            for l in n.lookup_dict.values():
                valslist = valslist + str(l)
            keylist = keylist + [valslist]
        #print('%s vs %s: %s' % (player1, player2, interaction[0]))
        match = axl.Match([player1, player2], turns=5)
        match.result = interaction[0]
        #print('%s vs %s: %s' % (player1, player2, match.result))
        #print('....... Scores:      %s' % ( match.scores()))
        player1scores = 0
        player2scores = 0
        for x in match.scores():
            player1scores = player1scores + x[0]
            player2scores = player2scores + x[1]
        #add scores to scoredict to keep track
        scoredict[keylist[0]][0] += player1scores #player score
        scoredict[keylist[0]][1] += player2scores #enemy score
        scoredict[keylist[1]][0] += player2scores #player score
        scoredict[keylist[1]][1] += player1scores #enemy score
        #print('"%s | %s" : %s | %s' % (keylist[0], keylist[1], player1scores, player2scores))
    
    
    dictFitness = fitnessFunction(scoredict)
    return dictFitness

def fitnessFunction(dicts):
    '''
    This is my fitness function.
    It is designed so that all value sum to ~ 1
    This then acts as the probability for the roulette wheel
    Based on the following R code
    sim[n,i,4]<-(sim[n,i,2]^2+1500-sim[n,i,3])/(sum(sim[n,1:100,2]^2)-sum(sim[n,1:100,3])+150000)
    '''
    global popCount
    fitnessDict={}
    sumScores = 0
    for n in dicts.keys():
        sumScores = sumScores + pow(dicts[n][0],2)
        #sumEnemy = sumEnemy + scoredict[n][1]
    for n in dicts.keys():
        fitnessDict.update({n:
                ((pow(dicts[n][0],2) + (150000/popCount)) / (sumScores+ 150000))
            })
    return fitnessDict
        
        

def rouletteChoice(population):
    '''
    Simple roulette implementation that picks based on probability from dictionary
    '''
    max = sum(population.values())
    pick = random.uniform(0, max)
    current = 0
    for key, value in population.items():
        current += value
        if current > pick:
            return key

def evolvePopulation(generations, dictFitness):
    '''
    Actual Genetic Algorithm implementation
    '''
    global popCount
    newdict = dictFitness
    #run as many times as specified
    for i in range (0, generations):
        print('*'*72)
        print('Generation: ' + str(i))
        print(newdict)
        stratList = []
        testpoplist = []
        #run until generated a list of same length
        while len(stratList) <= popCount:
            #print('doing GA')
            #create random num for actions
            chance = random.randint(0,100)
            
            #for simple copying, no crossover/mutation
            if chance < 70:
                madeit =0
                while (madeit < 1):
                    #print('doing simple   :    ' + str(madeit) + '   :   ' + str(len(stratList)) + '   :   ' + str(i))
                    stratString = rouletteChoice(newdict)
                    if stratString not in stratList:
                        madeit =1
                        stratList = stratList + [stratString]
                        testpoplist = testpoplist + [
                            axl.LookerUp(initial_actions=axl.action.str_to_actions(stratString[:memorydepth]), 
                                    pattern= stratString[memorydepth:], 
                                    parameters=lookerup.Plays(self_plays=2, op_plays=2, op_openings=0))
                            ]
            #crossover
            elif chance > 70:
                madeit =0
                while (madeit < 2):
                    #print('doing crossover   :    ' + str(madeit))
                    stratString = rouletteChoice(newdict)
                    stratString2 = rouletteChoice(newdict)
                    #ensure cannot breed with self
                    while stratString == stratString2:
                        stratString2 = rouletteChoice(newdict)
                    #get position to split on
                    newinds = crossOver(stratString, stratString2)
                    for i in newinds:
                            if i not in stratList:
                                madeit += 1
                                stratList = stratList + [i]
                                testpoplist = testpoplist + [
                                    axl.LookerUp(initial_actions=axl.action.str_to_actions(i[:memorydepth]), 
                                            pattern= i[memorydepth:], 
                                            parameters=lookerup.Plays(self_plays=2, op_plays=2, op_openings=0))
                                    ]
            #only goes to else if == 70
            #mutation
            else:
                madeit =0
                while (madeit < 1):
                    #print('doing mutation   :   ' + str(madeit))
                    stratString = rouletteChoice(newdict)
                    stratString = mutate(stratString)
                    if stratString not in stratList:
                        madeit =1
                        stratList = stratList + [stratString]
                        testpoplist = testpoplist + [
                            axl.LookerUp(initial_actions=axl.action.str_to_actions(stratString[:memorydepth]), 
                                    pattern= stratString[memorydepth:], 
                                    parameters=lookerup.Plays(self_plays=2, op_plays=2, op_openings=0))
                            ]
        newdict = playTournament(testpoplist)
    return newdict

def crossOver(strat1, strat2):
    '''
    Simple crossover at a random position
    '''
    pos = random.randint(1,len(strat1))
    part1 = strat1[:pos]
    part2 = strat2[pos:]
    child1 = part1 + part2
    part3 = strat2[:pos]
    part4 = strat1[pos:]
    child2 = part3 + part4
    return [child1, child2]
        
        
def mutate(individual):
    '''
    Simple mutation to flip a bit (which in this case are C->D,D->C)
    '''
    idx = random.randint(0,len(individual)-1)
    mutant = ''
    for i,n in enumerate(individual):
        if i == idx:
            if individual[idx] == 'C':
                mutant = mutant + 'D'
            else:
                mutant = mutant + 'C'
        else:
            mutant = mutant + n
    return mutant

'''
Initialise the algorithm
'''
finalstrats = evolvePopulation(100, playTournament(initialisePopulation()))

#order the final strategies by their values
orderedStrats = sorted(finalstrats.items(), key=lambda x:x[1])

#the one i will use for the IPD
chosenOne = orderedStrats[-1]

print(chosenOne)


#('CDDCCCDCDDCDDDDDDD', 0.012127481523025386)