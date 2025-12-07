from abc import ABC, abstractmethod
import string

class General(ABC):
    def __init__(self, nom: string = None):
        self.nom = nom

    """à implémenter plus tard selon le général"""
    @abstractmethod
    def strategie(self):  
        pass


## Fonctions bases pour les IA

def attaque(troupe,i,j,Map): #Troupe en position i,j sur la carte. Recherche d'un ennemi à attaquer.
    Map1=Map.to_matrix()
    portee=troupe[1].range
    for i1 in range (i-portee-1,i+portee+2):
        for j1 in range(j-portee-1,j+portee+2):
            for k1 in range(len(Map[i1][j1])):
                if Map1[i1][j1][k1][0]!=troupe[0]: #si la troupe ciblée appartient à une équipe différente de celle qui effectue la recherche
                    return (i1,j1,k1) #renvoyer la position exacte de la troupe ciblée
    return False

def trouverCible (troupe,i,j,Map): #Troupe en position i,j sur la carte. Recherche d'un ennemi à approcher.
    Map1=Map.to_matrix()
    vision=troupe[1].lineOfSight
    cible=(-1,-1,-1)
    distanceMax=-1
    for i1 in range(i-vision-1,i+vision+2):
        for j1 in range(j-vision-1,j+vision+1):
            for k1 in range(len(Map[i1][j1])):
                if Map1[i1][j1][k1][0]!=troupe[0]:
                    distance=(abs(i-i1)**2+abs(j-j1)**2)**0.5 #Pythagore
                    if distance<distanceMax or distanceMax==-1:
                        distanceMax=distance
                        cible=(i1,j1,k1) 
    return cible #renvoyer la position exacte de la troupe ciblée


def direction(troupe,i,j,cible): #Troupe située en position i,j sur la carte. Recherche du meilleur chemin pour se rapprocher de la troupe la plus proche.
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
 
def marche(troupe,i,j,k,objectif,Map): #Déplacez la troupe en position i,j sur la carte d'une case en empruntant le meilleur chemin.
    Map.removeUnit(Map,i,j,troupe[0],troupe[1])
    Map.addUnit(Map,objectif[0],objectif[1],troupe[0],troupe[1])
    return Map
