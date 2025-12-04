# pikeman.py
from Entity.Unit.guerrier import Guerrier
from Entity.Unit.knight import Knight   # pour le bonus cavalerie

class Pikeman(Guerrier):
	def __init__(self):
		super().__init__(
			hp=55, attaque=4, armor=0, pierceArmor=0, range=0, lineOfSight=4, speed=1,
			buildTime=22, reloadTime=3,
			shockInfantry=1, standardBuildings=1, elephants=25, baseMelee=4, mountedUnits=22, ships=16,
			camels=18, mamelukes=7, fishingShips=16, allArchers=0,
			spearUnits=0, infantry=0, baseMeleeDefense=0, basePierce=0, obsoleteDefense=0,
			cooldown=0
		)

	
	def _calculate_damage(self, target):
		k_elev = 1.0 #No elevation for the moment
		damage = k_elev * (self.baseMelee - target.armor)

		if isinstance(target, Knight):
			damage += self.mountedUnits
	
		target_name = target.__class__.__name__.lower()
		
		if "camel" in target_name:
			damage += self.camels
		if "elephant" in target_name:
			damage += self.elephants
			
		return max(1, damage)
	
