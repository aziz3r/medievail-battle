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

	# ---------- Scrum range ----------
	def _melee_reach(self) -> float:
		"""AoE affiche range=0 en mêlée : on autorise un contact ~1.0."""
		return 1.0 if (self.range is None or self.range == 0) else float(self.range)

	# ---------- Time management ----------
	def tick(self, dt: float):
		"""Fait passer le temps pour pouvoir refrapper (à appeler dans la boucle de jeu)."""
		self.cooldown = max(0.0, (self.cooldown or 0.0) - float(dt))

	# ---------- Damage calculation ----------
	def _calculate_damage(self, cible, k_elev: float = 1.0) -> float:
		"""Calcul des dégâts d'un coup (utile si tu veux l'appeler ailleurs)."""
		damage = float(self.baseMelee if self.baseMelee is not None else self.attaque) - float(getattr(cible, "armor", 0))
		bonus = 0.0

		if isinstance(cible, Knight):
			bonus += float(self.mountedUnits or 0)

		name = cible.__class__.__name__.lower()
		if "camel" in name:
			bonus += float(self.camels or 0)
		if "elephant" in name:
			bonus += float(self.elephants or 0)

		damage += bonus
		damage = max(1.0, float(k_elev) * damage)
		return round(damage, 2)

	
	