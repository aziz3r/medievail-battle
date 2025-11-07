## test pour véfirier si les fonctions fonctionnent
## j'ai utiliser une liste de 2 element (equipre , type d'unité) pour chaque unité

from knight import Knight
from projet import *

chevalier1 = Knight()
a = ['r' , chevalier1]
chevalier2 = Knight()
b = ['r' , chevalier2]
chevalier3 = Knight()
c = ['b' , chevalier3]

Map = [[[],[],[],[],[]],
       [[],[],[],[],[]],
       [[],[],[],[],[]],
       [[],[],[],[],[]],
       [[],[],[],[],[]]]

Map1 = [[[],[],[],[],[]],
        [[],[a],[],[b],[]],
        [[],[],[],[],[]],
        [[],[c],[],[],[]],
        [[],[],[],[],[]]]


print(Simulation(Map1,Violent,Braindead))
