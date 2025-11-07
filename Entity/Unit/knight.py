from guerrier import Guerrier
import math

class Knight(Guerrier):
    def __init__(self):
        super().__init__(hp=100, attaque=10, armor=2, pierceArmor=2, range=0, lineOfSight=4, speed=1.35, buildTime=30,
                         reloadTime=1.8, standardBuildings=0, cavalryResistance=-3, baseMelee=10, allBuildings=0,
                         allArchers=0, skirmishers=0, siegeUnits=0, obsolete=0, mountedUnits=0, baseMeleeDefense=2,
                         basePierce=2, obsoleteDefense=0)

        self.position = (0, 0)  
        self.destination = None  
        self.target = None  
        self.lastAttackTime = 0  
        self.isAlive = True  
                
        

    def se_deplacer(self, destination, dt):
        if not self.isAlive:
            return
    
        dx = destination[0] - self.position[0]
        dy = destination[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)
        
    
        if distance < 0.1:
            self.position = destination
            self.destination = None
        else:
            step = self.speed * dt 
            if step >= distance: 
                self.position = destination
                self.destination = None
            else:
                new_x = self.position[0] + (dx / distance) * step
                new_y = self.position[1] + (dy / distance) * step
                self.position = (new_x, new_y)
        

    def attaquer(self, target, currentTime):
        if not self.isAlive or not target.isAlive:
            return False
        
        if currentTime - self.lastAttackTime < self.reloadTime:
            return False  
        
        distance_to_target = self._calculate_distance(target)

        if distance_to_target > 1.0:
            return False
        else:
            damage = self._calculate_damage(target)
            target.hp -= damage
            self.lastAttackTime = currentTime
            if target.hp <= 0:
                target.isAlive = False
            return True
    


    def _calculate_distance(self, target):
        dx = self.position[0] - target.position[0]
        dy = self.position[1] - target.position[1]
        return math.sqrt(dx**2 + dy**2)
    

    def _calculate_damage(self, target):
        k_elev = 1.0
        damage = self.baseMelee
        damage -= target.armor
        damage = k_elev * damage
        damage = max(1, damage)
        return damage
    
