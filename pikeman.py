# pikeman.py
from guerrier import Guerrier
from knight import Knight

class Pikeman(Guerrier):
    def __init__(self, x=0.0, y=0.0):
        super().__init__(
            hp=55, attaque=4, armor=0, pierceArmor=0, range=0, lineOfSight=4, speed=1,
            buildTime=22, reloadTime=3,
            shockInfantry=1, standardBuildings=1, elephants=25, baseMelee=4, mountedUnits=22, ships=16,
            camels=18, mamelukes=7, fishingShips=16, allArchers=0,
            spearUnits=0, infantry=0, baseMeleeDefense=0, basePierce=0, obsoleteDefense=0,
            cooldown=0,
            x=x, y=y
        )

    def calculer_degats(self, cible, k_elev: float = 1.0) -> float:
        damage = float(self.baseMelee if self.baseMelee is not None else self.attaque) \
                 - float(getattr(cible, "armor", 0))
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

    def attaquer(self, target, distance, k_elev=1.0):
        ok, why = self.can_strike(distance, target)
        if not ok:
            if why == "out_of_range":
                print("The target is too far!")
            elif why == "cooldown":
                print("The pikeman must reload!")
            elif why == "target_dead":
                print("The target is already dead!")
            return 0

        allDamage = self.calculer_degats(target, k_elev)
        self.apply_damage(target, allDamage)
        self.start_cooldown()

        if target.hp <= 0:
            print(f"The {target.__class__.__name__} is destroyed!")
        else:
            print(f"{target.__class__.__name__} has {target.hp:.1f} HP remaining")
        return allDamage
    """
    def se_deplacer(self, dx: float, dy: float):
        # On réutilise la logique générique + message spécifique
        super().se_deplacer(dx, dy)
        print(f"The pikeman moves to ({self.x:.2f}, {self.y:.2f})")
    """
