from Entity.Unit.guerrier import Guerrier
from Entity.Unit.pikeman import Pikeman
import random


class Crossbowman(Guerrier):
    def __init__(self):
        super().__init__(hp=35, attaque=5, armor=0, pierceArmor=0, range=5, lineOfSight=7, speed=0.96, buildTime=27,
                        reloadTime=2, frameDelay=15, attackDelay=0.35, accuracy=85, equipe = None,
                        spearUnits=3, basePierceAttack=5, standardBuildings=0, stoneDefenseHarbors=0, 
                        highPierceArmorSiegeUnits=0,
                        allArchers=0, baseMeleeDefense=0, basePierce=0, obsoleteDefense=0, cooldown=0)
        

    def calculerDommage(self, target):
        precisionRoll = random.randint(1, 100)
        if precisionRoll > self.accuracy:
            return 0 
        

        kElev = 1.0 #Pas d'élévation pour le moment
        dommage = kElev * (self.basePierceAttack - target.pierceArmor)

        if isinstance(target, Pikeman):
            dommage += self.spearUnits  
        
        return max(1, dommage)
    