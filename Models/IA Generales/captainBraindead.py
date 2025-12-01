from general import *

class CapitainBraindead(General):
    def __init__(self):
        super().__init__(nom="Capitain BRAINDEAD")

    def strategie(troupe,i,j,k,Map): #IA Braindead : attaque basique seulement (IA Basique)
        if troupe[1].cooldown<0: # si la troupe a asser attendu avant sa derniere action
            cible1=super().attaque(troupe,i,j,Map)
            if cible1!=(-1,-1,-1): #si il y a un ennemie dans sa zone d attaque
                ennemi = Map.to_matrix[cible1[0]][cible1[1]][cible1[2]][1]
                team_ennemi = Map.to_matrix[cible1[0]][cible1[1]][cible1[2]][0]
                ennemi.hp-=troupe[1].attaque # attaque l ennemie
                troupe[1].cooldown+=troupe[1].reloadTime + troupe[1].attackDelay # ajoute du delay a la troupe avant sa prochaine action
                print(f"{troupe} attaque {ennemi} en {cible1[0]} ,  {cible1[1]}")
                if ennemi.hp <=0: # si l'ennemie est mort , le supprimer de la carte
                    Map.remove_unit(Map, cible1[0] , cible1[1] , team_ennemi, ennemi)
                print(f"{ennemi} {team_ennemi} est mort")
        else:
            troupe[1].cooldown -= 1 # si la troupe a rien fait , réduit son delai
        return Map
