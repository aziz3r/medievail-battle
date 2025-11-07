from general import *

class CapitainBraindead(General):
    def __init__(self):
        super().__init__(nom="Capitain BRAINDEAD")

    def strategie(troupe,i,j,k,Map): #IA Braindead : attaque basique seulement (IA Basique)
        if troupe[1].cooldown<0: # si la troupe a asser attendu avant sa derniere action
            cible1=super().attaque(troupe,i,j,Map)
            if cible1!=(-1,-1,-1): #si il y a un ennemie dans sa zone d attaque
                Map[cible1[0]][cible1[1]][cible1[2]][1].hp-=troupe[1].attaque # attaque l ennemie
                troupe[1].cooldown+=troupe[1].reloadTime + troupe[1].attackDelay # ajoute du delay a la troupe avant sa prochaine action
                print(f"{troupe} attaque {cible1} ")
                if Map[cible1[0]][cible1[1]][cible1[2]][1].hp <=0: # si l'ennemie est mort , le supprimer de la carte
                    Map=Map[cible1[0]][cible1[1]][:cible1[2]] + Map[cible1[0]][cible1[1]][cible1[2]+1:]
        else:
            troupe[1].cooldown -= 1 # si la troupe a rien fait , réduit son delai
        return Map