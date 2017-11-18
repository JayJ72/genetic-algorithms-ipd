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

import axelrod as axl
from axelrod import Action
from axelrod import lookerup
from axelrod import strategies
from axelrod.strategies.defector import Defector
from axelrod.strategies.titfortat import TitForTat
from axelrod.strategies.forgiver import Forgiver
from axelrod.strategies import Jay_Banerji
from axelrod.strategies.cooperator import Cooperator
C,D = Action.C, Action.D

myplayers={}

#generate the initial random population
'''testdict = lookerup.LookupTable.from_pattern(pattern=axl.action.str_to_actions('CDDDDDDCDCCCCDDD'),
            player_depth=2, op_depth=2, op_openings_depth=0
            )'''
#put the initial population into constructors
players =[
    TitForTat(),
    Defector(),
    Forgiver(),
    Cooperator(),
    Jay_Banerji()
    ]


tournament = axl.Tournament(players, turns=5, repetitions=1)
##results = tournament.play()

results = tournament.play(keep_interactions=True)


    
#print(tournament.players)

for index_pair, interaction in sorted(results.interactions.items()):
    player1 = tournament.players[index_pair[0]]
    player2 = tournament.players[index_pair[1]]


    print('%s vs %s: %s' % (player1, player2, interaction[0]))
    match = axl.Match([player1, player2], turns=5)
    match.result = interaction[0]
    print('%s vs %s: %s' % (player1, player2, match.result))
    print('....... Scores:      %s' % ( match.scores()))
    player1scores = 0
    player2scores = 0
    for x in match.scores():
        player1scores = player1scores + x[0]
        player2scores = player2scores + x[1]
    print('"%s | %s" : %s | %s' % (player1, player2, player1scores, player2scores))
