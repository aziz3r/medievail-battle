# crossbowman.py
import random
from guerrier import Guerrier
from pikeman import Pikeman

class Crossbowman(Guerrier):
    def __init__(self, x=0.0, y=0.0):
        super().__init__(
            hp=35, attaque=0, armor=0, pierceArmor=0, range=5, lineOfSight=7, speed=0.96,
            buildTime=27, reloadTime=2.0, cooldown=0,
            basePierceAttack=5, accuracy=85, spearUnits=3,
            x=x, y=y
        )

    def calculer_degats(self, cible, k_elev: float = 1.0) -> float:
        base = float(getattr(self, "basePierceAttack", 0))
        damage = base - float(getattr(cible, "pierceArmor", 0))

        if isinstance(cible, Pikeman):
            damage += float(getattr(self, "spearUnits", 0))

        damage = max(1.0, float(k_elev) * damage)
        return round(damage, 2)

    def attaquer(self, target, distance, k_elev=1.0):
        ok, why = self.can_strike(distance, target)
        if not ok:
            return 0

        acc = float(getattr(self, "accuracy", 100))
        if random.randint(1, 100) > acc:
            self.start_cooldown()
            return 0

        dmg = self.calculer_degats(target, k_elev)
        self.apply_damage(target, dmg)
        self.start_cooldown()
        return dmg
