from guerrier import Guerrier
from pikeman import Pikeman 
import random


class Crossbowman(Guerrier):
    def __init__(self):
        super().__init__(hp=35, attaque=5, armor=0, pierceArmor=0, range=5, lineOfSight=7, speed=0.96, buildTime=27,
                        reloadTime=2, frameDelay=15, attackDelay=0.35, accuracy=85,
                        spearUnits=3, basePierceAttack=5, standardBuildings=0, stoneDefenseHarbors=0, 
                        highPierceArmorSiegeUnits=0,
                        allArchers=0, baseMeleeDefense=0, basePierce=0, obsoleteDefense=0, cooldown=0)
        

    def se_deplacer(self):
        print("The crossbowman moves")

    def attaquer(self, target,distance,k_elev=1.0):
        precision= random.randint(1, 100)

        if distance > self.range:
            print ("The target is too far!")
            return 0
        
        if precision > self.accuracy:
            print ("The Crossbowman misses the target!")
            return 0
        
        degats = self.basePierceAttack - target.pierceArmor

        if isinstance(target, Pikeman):  
            degats += self.spearUnits

        allDamage = max(1, k_elev * degats)
        
        
        target.hp -= allDamage
                
        if target.hp <= 0:
            print(f"The {target.__class__.__name__} is destroyed!")
            target.hp = 0
        
        return allDamage
    def attaquer(self):
        print("The crossbowman attacks")
