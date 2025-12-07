from general import *

class MajorDaft(General):
    def __init__(self):
        super().__init__(nom="Major DAFT")

    def strategie(troupe,i,j,k,Map): #AI violente: Attaque de base et déplacement en ligne droite vers l'ennemi (IA de base)
        if troupe[1].cooldown<0:
            cible1=super().attaque(troupe,i,j,Map)
            if cible1==(-1,-1,-1): #s'il n'y a AUCUN ennemi à portée d'attaque (alors il essaiera de se rapprocher d'un ennemi)
                cible2=super().trouverCible(troupe,i,j,Map)
                if cible2!=(-1,-1,-1): #S'il y a un ennemi dans sa zone de vision
                    objectif=super().direction(troupe,i,j,cible2) #Trouve le meilleur chemin pour se rapprocher de l'ennemi le plus proche
                    Map = super().marche(troupe,i,j,k,objectif,Map) #Avance d'une case sur le meilleur chemin
                    troupe[1].cooldown+=1/troupe[1].speed #ajoute du delai a la troupe avant sa prochaine action
                    print(f"{troupe} se déplace")
            else:    
                ennemi = Map.toMatrix[cible1[0]][cible1[1]][cible1[2]][1]
                teamEnemy = Map.toMatrix[cible1[0]][cible1[1]][cible1[2]][0]
                ennemi.hp-=troupe[1].CalculerDommage(troupe[1],ennemi) #S'il y a un ennemi dans sa zone d'attaque, l'attaquer
                troupe[1].cooldown+=troupe[1].reloadTime + troupe[1].attackDelay #ajoute du delai a la troupe avant sa prochaine action
                print(f"{troupe} attaque {ennemi} en {cible1[0]} ,  {cible1[1]}")
                if Map[cible1[0]][cible1[1]][cible1[2]][1].hp <=0:
                    Map.removeUnit(Map, cible1[0] , cible1[1] , teamEnemy, ennemi)
                print(f"{ennemi} {teamEnemy} est mort") 
        else:
            troupe[1].cooldown-= 1 #Si la troupe n'a rien fait, réduit son delai
        return Map
        
