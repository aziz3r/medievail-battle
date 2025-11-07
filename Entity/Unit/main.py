from knight import Knight
from pikeman import Pikeman
from crossbowman import Crossbowman

chevalier1 = Knight()
archer1 = Crossbowman()
pikeman1 = Pikeman()

print(f"chevalier1 HP : {chevalier1.hp}")
print(f"archer1 HP : {archer1.hp}")
print(f"pikeman1 HP : {pikeman1.hp}")

###### Création des différentes unités (avec un nombre donné et une équipe)

def creationCrossbowmans (nb, equipe_choix):
    n = nb
    crossbowmans = {f'crossbowman{i}': Crossbowman() for i in range(1, n + 1)}
    for i in range(1, n + 1):
        crossbowmans[f'crossbowman{i}'].equipe = equipe_choix
    return crossbowmans

def creationPikemans (nb, equipe_choix):
    n = nb
    pikemans = {f'pikeman{i}': Pikeman() for i in range(1, n + 1)}
    for i in range(1, n + 1):
        pikemans[f'pikeman{i}'].equipe = equipe_choix
    return pikemans

def creationKnights (nb, equipe_choix):
    n = nb
    knights = {f'knight{i}': Knight() for i in range(1, n + 1)}
    for i in range(1, n + 1):
        knights[f'knight{i}'].equipe = equipe_choix
    return knights

crossbowmans = creationCrossbowmans(10, "Equipe rouge")
pikemans = creationPikemans(10, "Equipe bleue")
knights = creationKnights(10, "Equipe bleue")

print(crossbowmans['crossbowman10'].hp)
print(crossbowmans['crossbowman10'].equipe)

print(pikemans['pikeman10'].hp)
print(pikemans['pikeman10'].equipe)

print(knights['knight10'].hp)
print(knights['knight10'].equipe)
