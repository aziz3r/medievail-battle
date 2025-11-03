from guerrier import Guerrier

class Pikeman(Guerrier):
    def __init__(self):
        super().__init__(hp=55, attaque=4, armor=0, pierceArmor=0, range=0, lineOfSight=4, speed=1, buildTime=22, reloadTime=3,
                    shockInfantry=1, standardBuildings=1, elephants=25, baseMelee=4, mountedUnits=22, ships=16, camels=18,
                    mamelukes=7, fishingShips=16, allArchers=0, 
                    spearUnits=0, infantry=0, baseMeleeDefense=0, basePierce=0, obsoleteDefense=0)
        

    def se_deplacer(self):
        print("The pikeman moves")

    def attaquer(self):
        print("The pikeman attacks")