from Entity.Unit.guerrier import Guerrier
import math

class Knight(Guerrier):
    def __init__(self):
        super().__init__(hp=100, attaque=10, armor=2, pierceArmor=2, range=1, lineOfSight=4, speed=1.35, buildTime=30,
                         reloadTime=1.8, equipe = None, standardBuildings=0, cavalryResistance=-3, baseMelee=10, allBuildings=0,
                         allArchers=0, skirmishers=0, siegeUnits=0, obsolete=0, mountedUnits=0, baseMeleeDefense=2,
                         basePierce=2, obsoleteDefense=0)

        self.position = (0, 0)  
        self.destination = None  
        self.target = None  
        self.lastAttackTime = 0  
        self.isAlive = True  
                
        
   

    def _calculate_damage(self, target): 
        k_elev = 1.0 #No elevation for the moment
        damage = self.baseMelee
        damage -= target.armor
        damage = k_elev * damage
        damage = max(1, damage) #It must have at least one damage
        return damage

    
