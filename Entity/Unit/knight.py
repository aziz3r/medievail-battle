from guerrier import Guerrier

class Knight(Guerrier):
    def __init__(self):
        super().__init__(hp=100, attaque=10, armor=2, pierceArmor=2, range=0, lineOfSight=4, speed=1.35, buildTime=30,
                         reloadTime=1.8, standardBuildings=0, cavalryResistance=-3, baseMelee=10, allBuildings=0,
                         allArchers=0, skirmishers=0, siegeUnits=0, obsolete=0, mountedUnits=0, baseMeleeDefense=2,
                         basePierce=2, obsoleteDefense=0)
        

    def se_deplacer(self):
        print("The Knight moves")

    def attaquer(self):
        print("The knight attacks")