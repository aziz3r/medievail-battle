# pikeman.py
from guerrier import Guerrier
from knight import Knight

class Pikeman(Guerrier):
    def __init__(self, x=0.0, y=0.0):
        super().__init__(
            hp=55, attaque=4, armor=0, pierceArmor=0, range=1, lineOfSight=4, speed=1.1,
            buildTime=22, reloadTime=3.0, cooldown=0,
            baseMelee=4, shockInfantry=1, elephants=25,
            x=x, y=y
        )

    def calculer_degats(self, cible, k_elev: float = 1.0) -> float:
        dmg = float(getattr(self, "baseMelee", 0)) - float(getattr(cible, "armor", 0))
        if isinstance(cible, Knight):
            dmg += 8
        dmg = max(1.0, dmg)
        return round(float(k_elev) * dmg, 2)

    def attaquer(self, target, distance, k_elev=1.0):
        ok, why = self.can_strike(distance, target)
        if not ok:
            return 0
        dmg = self.calculer_degats(target, k_elev)
        self.apply_damage(target, dmg)
        self.start_cooldown()
        return dmg
