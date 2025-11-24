from general import *

class MajorDaft(General):
    def __init__(self):
        super().__init__(nom="Major DAFT")

    def strategie(troupe,i,j,k,Map): #Violent AI: basic attack and movement in a straight line towards the enemy (Basic AI)
        if troupe[1].cooldown<0:
            cible1=super().attaque(troupe,i,j,Map)
            if cible1==(-1,-1,-1): #if there is NO enemy in its attack range (then it will try to get closer to one)
                cible2=super().trouvecible(troupe,i,j,Map)
                if cible2!=(-1,-1,-1): #if he sees an enemy
                    objectif=super().direction(troupe,i,j,cible2) #find the best path
                    Map = super().marche(troupe,i,j,k,objectif,Map) #go forward
                    troupe[1].cooldown+=1/troupe[1].speed #add delay to the troop before its next action
                    print(f"{troupe} se déplace")
            else:    
                Map[cible1[0]][cible1[1]][cible1[2]][1].hp-=troupe[1].attaque #if there was an enemy in its attack range, attack the enemy
                troupe[1].cooldown+=troupe[1].reloadTime + troupe[1].attackDelay #add delay to the troop before its next action
                print(f"{troupe} attaque {cible1} ")
                if Map[cible1[0]][cible1[1]][cible1[2]][1].hp <=0:
                    Map=Map[cible1[0]][cible1[1]][:cible1[2]] + Map[cible1[0]][cible1[1]][cible1[2]+1:] # if the enemy is dead, remove it from the map 
        else:
            troupe[1].cooldown-= 1 # if the troop did nothing, reduce its delay
        return Map
