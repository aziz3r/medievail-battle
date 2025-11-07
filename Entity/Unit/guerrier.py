from abc import ABC, abstractmethod

class Guerrier(ABC):
    def __init__(self, hp: float = None, attaque: float = None, armor: float = None, pierceArmor: float = None,
                 range: float = None, lineOfSight: float = None, speed: float = None, buildTime: float = None,
                 reloadTime: float = None, shockInfantry: float = None, frameDelay: float = None, attackDelay: float = None,
                accuracy: float = None,   standardBuildings: float = None,
                 elephants: float = None, baseMelee: float = None, mountedUnits: float = None, ships: float = None,
                 camels: float = None, mamelukes: float = None, fishingShips: float = None, allArchers: float = None,
                 allBuildings: float = None, cavalryResistance: float = None, siegeUnits: float = None, skirmishers: float = None,
                 basePierceAttack: float = None, highPierceArmorSiegeUnits: float = None, stoneDefenseHarbors: float = None,
                 obsolete: float = None,
                 spearUnits: float = None, infantry: float = None,baseMeleeDefense: float = None, 
                 basePierce: float = None, obsoleteDefense: float = None,
                 mountedUnitsDefense: float = None, cooldown: float =None):
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


    """à implémenter plus tard selon le type de guerrier"""
    @abstractmethod
    def se_deplacer(self):  
        pass

    @abstractmethod
    def attaquer(self):  
        pass
