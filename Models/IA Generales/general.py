from abc import ABC, abstractmethod
import string

class General(ABC):
    def __init__(self, nom: string = None):
        self.nom = nom

    """à implémenter plus tard selon le général"""
    @abstractmethod
    def strategie(self):  
        pass


## Fonctions basique d attaque / déplacement

def attaque(troupe,i,j,Map): #troupe en position i,j sur la map . cherche un ennemie a attaquer
    portee=troupe[1].range
    for i1 in range (i-portee-1,i+portee+2):
        for j1 in range(j-portee-1,j+portee+2):
            for k1 in range(len(Map[i1][j1])):
                if Map[i1][j1][k1][0]!=troupe[0]: #si la troupe visée est dans une equipe differente de la troupe qui recherche
                    return (i1,j1,k1) #retourne la position exact de la troupe visée
    return False

def trouvecible (troupe,i,j,Map): #troupe en position i,j sur la map . cherche un ennemi a se rapprocher
    vision=troupe[1].lineOfSight
    cible=(-1,-1,-1)
    distancemax=-1
    for i1 in range(i-vision-1,i+vision+2):
        for j1 in range(j-vision-1,j+vision+1):
            for k1 in range(len(Map[i1][j1])):
                if Map[i1][j1][k1][0]!=troupe[0]:
                    distance=(abs(i-i1)**2+abs(j-j1)**2)**0.5 #Pythagore
                    if distance<distancemax or distancemax==-1:
                        distancemax=distance
                        cible=(i1,j1,k1) 
    return cible #retourne la position exact de la troupe visée


def direction(troupe,i,j,cible): #troupe en position i,j sur la map . Cherche le meilleur chemin a prendre pour se rapprocher de la troupe la plus proche
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
 
def marche(troupe,i,j,k,objectif,Map): #troupe en position i,j sur la map . Se deplace d'une case sur le meilleur chemin
    troupe1=troupe
    Map[i][j]=Map[i][j][:k]+Map[i][j][k+1:]
    Map[objectif[0],objectif[1]].append(troupe1)
    return Map