from abc import ABC, abstractmethod
import string

class General(ABC):
    def __init__(self, nom: string = None):
        self.nom = nom

    """à implémenter plus tard selon le général"""
    @abstractmethod
    def strategie(self):  
        pass


## basic functions for all generals

def attaque(troupe,i,j,Map): #Troop in position i,j on the map. Looking for an enemy to attack
    Map1=Map.to_matrix()
    portee=troupe[1].range
    for i1 in range (i-portee-1,i+portee+2):
        for j1 in range(j-portee-1,j+portee+2):
            for k1 in range(len(Map[i1][j1])):
                if Map1[i1][j1][k1][0]!=troupe[0]: #if the targeted troop is in a different team than the troop that is searching
                    return (i1,j1,k1) #return the exact position of the targeted troop
    return False

def trouvecible (troupe,i,j,Map): #troop in position i,j on the map. Looking for an enemy to approach.
    Map1=Map.to_matrix()
    vision=troupe[1].lineOfSight
    cible=(-1,-1,-1)
    distancemax=-1
    for i1 in range(i-vision-1,i+vision+2):
        for j1 in range(j-vision-1,j+vision+1):
            for k1 in range(len(Map[i1][j1])):
                if Map1[i1][j1][k1][0]!=troupe[0]:
                    distance=(abs(i-i1)**2+abs(j-j1)**2)**0.5 #Pythagore
                    if distance<distancemax or distancemax==-1:
                        distancemax=distance
                        cible=(i1,j1,k1) 
    return cible #return the exact position of the targeted troop


def direction(troupe,i,j,cible): #troop in position i,j on the map. Looking for the best path to get closer to the nearest troop.
    if cible == (-1,-1,-1):
        return (-1,-1)
    idiff=abs(i-cible[0])
    jdiff=abs(j-cible[1])
    if idiff<jdiff:
        if j-cible[1]<0:
            objectif=(i,j+1)
        else:
            objectif=(i,j-1)
    else:
        if i-cible[0]<0:
            objectif=(i+1,j)
        else:
            objectif=(i-1,j)
    return objectif
 
def marche(troupe,i,j,k,objectif,Map): #troop in position i,j on the map. Move one square on the best path.
    Map.remove_unit(Map,i,j,troupe[0],troupe[1])
    Map.add_unit(Map,objectif[0],objectif[1],troupe[0],troupe[1])
    return Map
