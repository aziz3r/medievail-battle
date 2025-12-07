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

	
	def calculerDommage(self, cible):
		kElev = 1.0 #Pas d'élévation pour le moment
		dommage = kElev * (self.baseMelee - cible.armor)

		if isinstance(cible, Knight):
			dommage += self.mountedUnits
	
		cible_name = cible.__class__.__name__.lower()
		
		if "camel" in cible_name:
			dommage += self.camels
		if "elephant" in cible_name:
			dommage += self.elephants
			
		return max(1, dommage)
	
