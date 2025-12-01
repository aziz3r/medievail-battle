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
        

       
    def _calculate_damage(self, cible):
        """calcul des dégats pour Crossbowman"""
    
