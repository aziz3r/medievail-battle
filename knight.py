# knight.py
from guerrier import Guerrier

class Knight(Guerrier):
    def __init__(self, x=0.0, y=0.0):
        super().__init__(
            hp=100, attaque=8, armor=2, pierceArmor=1, range=1, lineOfSight=4, speed=1.6,
            buildTime=30, reloadTime=1.8, cooldown=0,
            baseMelee=8, x=x, y=y
        )

    def calculer_degats(self, cible, k_elev: float = 1.0) -> float:
        dmg = float(getattr(self, "baseMelee", 0)) - float(getattr(cible, "armor", 0))
        dmg = max(1.0, dmg)
        return round(float(k_elev) * dmg, 2)

    def attaquer(self, target, distance, k_elev=1.0):
        ok, _ = self.can_strike(distance, target)
        if not ok:
            return 0
        dmg = self.calculer_degats(target, k_elev)
        self.apply_damage(target, dmg)
        self.start_cooldown()
        return dmg
