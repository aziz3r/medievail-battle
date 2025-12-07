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
        self.position = (0.0, 0.0)      # position sur la map
        self.lastAttackTime = 0.0     # temps de la dernière attaque

    def seDeplacer(self, destination: tuple, delta_t: float = 1.0): 
        """
        Déplace le guerrier vers la destination en fonction de sa vitesse.
        delta_t = durée du "tick" (en secondes)
        """
        if self.hp<=0:
            return #verifier si le guerrier est vivant

        x, y = self.position
        dx = destination[0] - x
        dy = destination[1] - y
        distance = math.sqrt(dx**2 + dy**2)

        step = self.speed * delta_t

        if (distance == 0 or distance<=step):
            self.position = destination
            self.destination = None
            return  # deja à la destination

    
        else:
            ratio = step / distance
            new_x= x + dx * ratio
            new_y= y + dy * ratio
            self.position = (new_x, new_y)

        print(f"{type(self).__name__} se déplace vers {self.position}")


    def calculerDistance(self, cible):
        dx = self.position[0] - cible.position[0]
        dy = self.position[1] - cible.position[1]
        return math.sqrt(dx**2 + dy**2)

        
    def attaquer(self, cible, currentTime):
        """
        Attaque une cible selon la formule de AoE2
        """
        #verifie si la cible et le guerrier sont vivants
        if self.hp <= 0 or cible.hp <= 0:
            return False
        # verifie le temps entre les attaques
        if currentTime - self.lastAttackTime < self.reloadTime:
            return False
        
        distance = self.calculerDistance(cible)
        if distance > self.range:
            return False
        
        dommage = self.calculerDommage(cible)

        #apllique les dommages à la cible
        cible.hp -= dommage
        #met à jour le temps de la dernière attaque
        self.lastAttackTime = currentTime

        if cible.hp <= 0:
            cible.hp = 0
        
        return True
    
    @abstractmethod
    def calculerDommage(self, cible):
        """Chaque unité a sa formule spécifique de dégâts"""
        pass