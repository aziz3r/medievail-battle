from abc import ABC, abstractmethod
import string
import math
import time

class Guerrier(ABC):
    def __init__(self, hp: float = None, attaque: float = None, armor: float = None, pierceArmor: float = None,
                 range: float = None, lineOfSight: float = None, speed: float = None, buildTime: float = None,
                 reloadTime: float = None, shockInfantry: float = None, frameDelay: float = None, attackDelay: float = None,
                accuracy: float = None, cooldown: float =None, equipe: string = None,  standardBuildings: float = None,
                 elephants: float = None, baseMelee: float = None, mountedUnits: float = None, ships: float = None,
                 camels: float = None, mamelukes: float = None, fishingShips: float = None, allArchers: float = None,
                 allBuildings: float = None, cavalryResistance: float = None, siegeUnits: float = None, skirmishers: float = None,
                 basePierceAttack: float = None, highPierceArmorSiegeUnits: float = None, stoneDefenseHarbors: float = None,
                 obsolete: float = None,
                 spearUnits: float = None, infantry: float = None,baseMeleeDefense: float = None, 
                 basePierce: float = None, obsoleteDefense: float = None,
                 mountedUnitsDefense: float = None, ):
        self.hp = hp
        self.attaque = attaque
        self.armor = armor
        self.pierceArmor = pierceArmor
        self.range = range
        self.lineOfSight = lineOfSight
        self.speed = speed
        self.buildTime = buildTime              ## en secondes
        self.reloadTime = reloadTime            ## en secondes
        self.frameDelay = frameDelay
        self.attackDelay = attackDelay          ## en secondes
        self.accuracy = accuracy                ## en %
        self.cooldown = cooldown                ## en secondes
        self.equipe = equipe
        
        """Attaque"""
        self.shockInfantry = shockInfantry
        self.standardBuildings = standardBuildings
        self.elephants = elephants
        self.baseMelee = baseMelee
        self.mountedUnits = mountedUnits
        self.ships = ships
        self.camels = camels
        self.mamelukes = mamelukes
        self.fishingShips = fishingShips
        self.allArchers = allArchers
        self.allBuildings = allBuildings
        self.cavalryResistance = cavalryResistance
        self.siegeUnits = siegeUnits
        self.skirmishers = skirmishers
        self.basePierceAttack = basePierceAttack 
        self.highPierceArmorSiegeUnits = highPierceArmorSiegeUnits
        self.stoneDefenseHarbors = stoneDefenseHarbors
        self.obsolete = obsolete

        
        """Defense"""
        self.spearUnits = spearUnits
        self.infantry = infantry
        self.baseMeleeDefense = baseMeleeDefense
        self.basePierce = basePierce
        self.obsoleteDefense = obsoleteDefense
        self.mountedUnitsDefense = mountedUnitsDefense

        self.position = (0.0, 0.0)      # position on the map
        self.vivant = True              # is the unit alive
        self.last_attack_time = 0.0     # time of the last attack

    """à implémenter plus tard selon le type de guerrier"""
    def se_deplacer(self, destination: tuple, delta_t: float = 1.0): 
        """
        Déplace le guerrier vers la destination en fonction de sa vitesse.
        delta_t = durée du "tick" (en secondes)
        """
        if not self.vivant:
            return

        x, y = self.position
        dx = destination[0] - x
        dy = destination[1] - y
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            return  # already at destination

        max_move = (self.speed or 0) * delta_t

        if distance <= max_move:
            self.position = destination
        else:
            ratio = max_move / distance
            self.position = (x + dx * ratio, y + dy * ratio)

        print(f"{type(self).__name__} se déplace vers {self.position}")
        
    def attaquer(self, cible: "Guerrier", elevation_factor: float = 1.0):
        """
        Attaque une cible selon la formule de AoE2 :
        Damage = max(1, kelev × sum(max(0, Attack_i − Armor_i)))
        """
        if not self.vivant or not cible.vivant:
            return

        # Check range
        dx = cible.position[0] - self.position[0]
        dy = cible.position[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance > (self.range or 1):
            print(f"{type(self).__name__} est hors de portée de {type(cible).__name__}.")
            return

        # Check the time between attacks
        now = time.time()
        if now - self.last_attack_time < (self.reloadTime or 1):
            return  # not ready yet

        # calculate base damage
        base_damage = max(0, (self.attaque or 0) - (cible.armor or 0))

        #apply bonuses for specific target types 
        bonus_total = 0
        for attr in ["mountedUnits", "elephants", "ships", "camels", "mamelukes", "allArchers"]:
            bonus_val = getattr(self, attr, None)
            if bonus_val and getattr(cible, attr + "Defense", None) is not None:
                bonus_total += bonus_val

        total_damage = max(1, elevation_factor * (base_damage + bonus_total))

        #apply damage to target
        cible.vie_restante -= total_damage
        if cible.vie_restante <= 0:
            cible.vivant = False
            cible.vie_restante = 0

        # update last attack time
        self.last_attack_time = now

        print(f"{type(self).__name__} inflige {total_damage:.1f} dégâts à {type(cible).__name__} "
              f"(PV restants : {cible.vie_restante:.1f})")
    
    @abstractmethod
    def _calculate_damage(self, cible):
        """Chaque unité a sa formule spécifique de dégâts"""
        pass
