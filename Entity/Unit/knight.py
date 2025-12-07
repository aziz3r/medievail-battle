from Entity.Unit.guerrier import Guerrier
import math

class Knight(Guerrier):
    def __init__(self):
        super().__init__(hp=100, attaque=10, armor=2, pierceArmor=2, range=1, lineOfSight=4, speed=1.35, buildTime=30,
                         reloadTime=1.8, equipe = None, standardBuildings=0, cavalryResistance=-3, baseMelee=10, allBuildings=0,
                         allArchers=0, skirmishers=0, siegeUnits=0, obsolete=0, mountedUnits=0, baseMeleeDefense=2,
                         basePierce=2, obsoleteDefense=0)

        
   

    def calculerDommage(self, target): 
        kElev = 1.0 #Pas d'élévation pour le moment
        dommage = kElev * (self.baseMelee - target.armor)
        dommage = max(1, dommage) #Il doit y avoir au moins un dommage
        return dommage
    
