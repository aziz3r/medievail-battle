from guerrier import Guerrier
from knight import Knight 

class Pikeman(Guerrier):
    def __init__(self):
        super().__init__(hp=55, attaque=4, armor=0, pierceArmor=0, range=0, lineOfSight=4, speed=1, buildTime=22, reloadTime=3,
                    shockInfantry=1, standardBuildings=1, elephants=25, baseMelee=4, mountedUnits=22, ships=16, camels=18,
                    mamelukes=7, fishingShips=16, allArchers=0, 
                    spearUnits=0, infantry=0, baseMeleeDefense=0, basePierce=0, obsoleteDefense=0, cooldown=0)
        

    def se_deplacer(self):
        print("The pikeman moves")

    
    def attaquer(self, target, distance, k_elev=1.0):
        
        #check if the target is within firing range
        if distance > self.range:
            print("The target is too far! ")
            return 0
        
        
       # Base damage calculation (melee attack - target's melee armor)
        degats = self.baseMelee - target.armor
        
       # Attack bonus depending on target type
        bonus = 0
        
        # Bonus against the Knights (mounted cavalry)
        if isinstance(target, Knight):
            bonus = self.mountedUnits  # +22 damage
            degats += bonus
            print(f"Bonus damage against mounted units: +{bonus}")
        
    
        
        allDamage = max(1, k_elev * degats)
        
        # Inflict damage
        target.hp -= allDamage
        
        
        # Check if the target is destroyed
        if target.hp <= 0:
            print(f"The {target.__class__.__name__} is destroyed!")
            target.hp = 0
        else:
            print(f"{target.__class__.__name__} has {target.hp:.1f} HP remaining")
        
        return allDamage

