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

from axelrod.action import Action, actions_to_str
from axelrod.player import Player
import itertools


C, D = Action.C, Action.D


class Jay_Banerji(Player):

    # These are various properties for the strategy
    name = 'Jay Banerji Genetic Algorithm Result'
    classifier = {
        'memory_depth': 2,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }
    memorydepth = classifier['memory_depth']

    def strategy(self, opponent: Player) -> Action:
        chosenStratString = 'CDDCCCDCDDCDDDDDDD'
        initInd = chosenStratString[self.memorydepth:]
        strategyasList=[]
        for z in initInd:
            if z == 'C':
                strategyasList = strategyasList + [C]
            elif z == 'D':
                strategyasList = strategyasList + [D]
        initVec = chosenStratString[:self.memorydepth]
        initasList=[]
        for q in initVec:
            if q == 'C':
                initasList = initasList+ [C]
            elif q == 'D':
                initasList = initasList + [D]
        possiblePlays = ['CC','CD','DC','DD']
        stratCombs = itertools.product(possiblePlays,repeat=self.memorydepth)
        stratList = []
        for n in stratCombs:
            stratList = stratList + [n]
        dictPlays = dict(zip(stratList,strategyasList))
        print('Initial Moves : ' + str(initasList))
        print(dictPlays)
        #print(''.join(dictPlays.values()))
        if not self.history or not opponent.history:
            return initasList[0]
        if len(self.history) < 2 or len(opponent.history) < 2:
            return initasList[1] 
        else:
            first = str(self.history[-1]) + str(opponent.history[-1])
            second = str(self.history[-2]) + str(opponent.history[-2])
            keyaslist = [first, second]
            key = tuple(keyaslist)
            return dictPlays.get(key)
