# knight.py
from guerrier import Guerrier

class Knight(Guerrier):
    def __init__(self, x=0.0, y=0.0):
        super().__init__(
            hp=100, attaque=10, armor=2, pierceArmor=2, range=0, lineOfSight=4, speed=1.35,
            buildTime=30, reloadTime=1.8, cooldown=0,
            x=x, y=y
        )

    def calculer_degats(self, cible, k_elev: float = 1.0) -> float:
        damage = float(self.attaque) - float(getattr(cible, "armor", 0))
        damage = max(1.0, float(k_elev) * damage)
        return round(damage, 2)

    def attaquer(self, target, distance, k_elev=1.0):
        ok, why = self.can_strike(distance, target)
        if not ok:
            if why == "out_of_range":
                print("The target is too far!")
            elif why == "cooldown":
                print("The knight must reload!")
            elif why == "target_dead":
                print("The target is already dead!")
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
        print(f"The knight moves to ({self.x:.2f}, {self.y:.2f})")
    """
