
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

## Fonctions pour la Simulation ( compléxité très forte )

def Simulation(Map,IA1,IA2,t=0): # IA1 vs IA2 sur la map . temps t en seconde ( nombre d iteration de la simulation)
    if BlueWin(Map):
        return "IA1 a gagnee"
    if RedWin(Map):
        return "IA2 a gagner"
    for i in range(len(Map)):
        for j in range(len(Map[i])):
            for k in range(len(Map[i][j])):
                if Map[i][j][k][0]=='r': # si la troupe est de l equipe rouge , l'IA1 commande ses actions
                    Map=IA1(Map[i][j][k],i,j,k,Map)
                if Map[i][j][k][0]=='b': # si la troupe est de l equipe bleu , l'IA2 commande ses actions
                    Map=IA2(Map[i][j][k],i,j,k,Map)
    if t == 5: #pour eviter une boucle infinie dans les premiers tests
        return None
    print(Map)
    return Simulation(Map,IA1,IA2,t+1)

def RedWin(Map): # vérifie si tout les bleu sont mort
    for i in range(len(Map)):
        for j in range (len(Map[i])):
            for k in range(len(Map[i][j])):
                if Map[i][j][k][0]=='b':
                    return False
    return True

def BlueWin(Map): # verifier si tout les rouges sont mort
    for i in range(len(Map)):
        for j in range (len(Map[i])):
            for k in range(len(Map[i][j])):
                if Map[i][j][k][0]=='r':
                    return False
    return True


## IA avec les fonction basique d attaque / deplacement


def Braindead(troupe,i,j,k,Map): #IA Braindead : attaque basique seulement (IA Basique)
    if troupe[1].cooldown<0: # si la troupe a asser attendu avant sa derniere action
        cible1=attaque(troupe,i,j,Map)
        if cible1!=(-1,-1,-1): #si il y a un ennemie dans sa zone d attaque
            Map[cible1[0]][cible1[1]][cible1[2]][1].hp-=troupe[1].attaque # attaque l ennemie
            troupe[1].cooldown+=troupe[1].reloadTime + troupe[1].attackDelay # ajoute du delay a la troupe avant sa prochaine action
            print(f"{troupe} attaque {cible1} ")
            if Map[cible1[0]][cible1[1]][cible1[2]][1].hp <=0: # si l'ennemie est mort , le supprimer de la carte
                Map=Map[cible1[0]][cible1[1]][:cible1[2]] + Map[cible1[0]][cible1[1]][cible1[2]+1:]
    else:
        troupe[1].cooldown -= 1 # si la troupe a rien fait , réduit son delai
    return Map

def Violent(troupe,i,j,k,Map): #IA Violente : attaque basique et se deplacement en ligne droite sur l'ennemie  (IA Basique)
    if troupe[1].cooldown<0:
        cible1=attaque(troupe,i,j,Map)
        if cible1==(-1,-1,-1): #si il y a PAS un ennemie dans sa zone d attaque ( alors il va essayer de se rapprocher d'un )
            cible2=trouvecible(troupe,i,j,Map)
            if cible2!=(-1,-1,-1): #si il voit un ennemie
                objectif=direction(troupe,i,j,cible2) #trouve le meilleur chemin
                Map =marche(troupe,i,j,k,objectif,Map) #avance 
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

