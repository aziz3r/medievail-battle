# guerrier.py
from abc import ABC, abstractmethod
from typing import Tuple

class Guerrier(ABC):
    def __init__(self, *, hp, attaque, armor, pierceArmor, range, lineOfSight,
                 speed, buildTime, reloadTime, cooldown=0, x=0.0, y=0.0, **kwargs):
        # Stats de base
        self.hp = float(hp)
        self.attaque = float(attaque)
        self.armor = float(armor)
        self.pierceArmor = float(pierceArmor)
        self.range = float(range)
        self.lineOfSight = float(lineOfSight)
        self.speed = float(speed)
        self.buildTime = float(buildTime)
        self.reloadTime = float(reloadTime)
        self.cooldown = float(cooldown)
        self.intent = None     # mémorise le dernier ordre reçu
        
        # Position (simple, utilisable avec la map)
        self.x = float(x)
        self.y = float(y)

        # stocke aussi tout ce que tu passes en plus (baseMelee, mountedUnits, etc.)
        for k, v in kwargs.items():
            setattr(self, k, v)

    # --- État de vie ---

    def est_vivant(self) -> bool:
        return self.hp > 0

    # --- Gestion du temps / cooldown ---

    def tick(self, dt: float):
        """Fait passer le temps → réduit le cooldown."""
        self.cooldown = max(0.0, (self.cooldown or 0.0) - float(dt))

    # --- Portée d'attaque ---

    def get_reach(self) -> float:
        """Portée effective: si range==0 (mêlée), autorise ~1.0 tuile."""
        return 1.0 if (self.range is None or self.range == 0) else float(self.range)

    def in_range(self, distance: float) -> bool:
        return float(distance) <= self.get_reach()

    # --- Vérifications avant attaque ---

    def can_strike(self, distance: float, target) -> Tuple[bool, str]:
        """Vérifs standard: portée, cooldown, cibles vivantes."""
        if not self.est_vivant():
            return False, "attacker_dead"
        if not hasattr(target, "hp") or target.hp <= 0:
            return False, "target_dead"
        if not self.in_range(distance):
            return False, "out_of_range"
        if (self.cooldown or 0.0) > 0.0:
            return False, "cooldown"
        return True, "ok"

    def start_cooldown(self):
        self.cooldown = float(self.reloadTime or 0.0)

    # --- Dégâts ---

    def apply_damage(self, target, dmg: float) -> float:
        """Applique les dégâts (et clamp à 0). Retourne les dégâts appliqués."""
        real = max(0.0, float(dmg))
        target.hp = max(0.0, float(target.hp) - real)
        return real

    

    # --- Méthodes à spécialiser ---

    @abstractmethod
    def calculer_degats(self, cible, k_elev: float = 1.0) -> float:
        ...

    @abstractmethod
    def attaquer(self, target, distance, k_elev: float = 1.0):
        ...
