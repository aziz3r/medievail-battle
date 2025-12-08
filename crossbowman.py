# crossbowman.py
import random
from guerrier import Guerrier
from pikeman import Pikeman  # pour l'exemple de bonus vs spears si tu en veux un

class Crossbowman(Guerrier):
    def __init__(self, x=0.0, y=0.0):
        super().__init__(
            hp=35, attaque=0, armor=0, pierceArmor=0, range=5, lineOfSight=7, speed=0.96,
            buildTime=27, reloadTime=2.0, cooldown=0,
            basePierceAttack=5, accuracy=85, spearUnits=3,
            x=x, y=y
        )

    def calculer_degats(self, cible, k_elev: float = 1.0) -> float:
        # tir perçant → compare au pierceArmor
        base = float(getattr(self, "basePierceAttack", 0))
        damage = base - float(getattr(cible, "pierceArmor", 0))

        # (optionnel) petit bonus vs piquier
        if isinstance(cible, Pikeman):
            damage += float(getattr(self, "spearUnits", 0))

        damage = max(1.0, float(k_elev) * damage)
        return round(damage, 2)

    def attaquer(self, target, distance, k_elev=1.0):
        ok, why = self.can_strike(distance, target)
        if not ok:
            if why == "out_of_range":
                print("The target is too far!")
            elif why == "cooldown":
                print("The crossbowman must reload!")
            elif why == "target_dead":
                print("The target is already dead!")
            return 0

        # jet de précision
        acc = float(getattr(self, "accuracy", 100))
        if random.randint(1, 100) > acc:
            self.start_cooldown()
            print("The crossbowman misses the target!")
            return 0

        allDamage = self.calculer_degats(target, k_elev)
        self.apply_damage(target, allDamage)
        self.start_cooldown()

        if target.hp <= 0:
            print(f"The {target.__class__.__name__} is destroyed!")
            target.hp = 0
        else:
            print(f"{target.__class__.__name__} has {target.hp:.1f} HP remaining")
        return allDamage

"""
    def se_deplacer(self, dx: float, dy: float):
        super().se_deplacer(dx, dy)
        print(f"The crossbowman moves to ({self.x:.2f}, {self.y:.2f})")
"""
