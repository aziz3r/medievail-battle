from general import *

class MajorDaft(General):
    def __init__(self):
        super().__init__(nom="Major DAFT")

    def strategie(troupe,i,j,k,Map): #IA Violente : attaque basique et se deplacement en ligne droite sur l'ennemie  (IA Basique)
        if troupe[1].cooldown<0:
            cible1=super().attaque(troupe,i,j,Map)
            if cible1==(-1,-1,-1): #si il y a PAS un ennemie dans sa zone d attaque ( alors il va essayer de se rapprocher d'un )
                cible2=super().trouvecible(troupe,i,j,Map)
                if cible2!=(-1,-1,-1): #si il voit un ennemie
                    objectif=super().direction(troupe,i,j,cible2) #trouve le meilleur chemin
                    Map = super().marche(troupe,i,j,k,objectif,Map) #avance 
                    troupe[1].cooldown+=1/troupe[1].speed # ajoute du delay a la troupe avant sa prochaine action 
                    print(f"{troupe} se déplace")
            else:    
                Map[cible1[0]][cible1[1]][cible1[2]][1].hp-=troupe[1].attaque # si il y avait un ennemi dans sa zone d attaque , attaque l ennemie
                troupe[1].cooldown+=troupe[1].reloadTime + troupe[1].attackDelay # ajoute du delay a la troupe avant sa prochaine action
                print(f"{troupe} attaque {cible1} ")
                if Map[cible1[0]][cible1[1]][cible1[2]][1].hp <=0:
                    Map=Map[cible1[0]][cible1[1]][:cible1[2]] + Map[cible1[0]][cible1[1]][cible1[2]+1:] # si l'ennemie est mort , le supprimer de la carte 
        else:
            troupe[1].cooldown-= 1 # si la troupe a rien fait , réduit son delai
        return Map
