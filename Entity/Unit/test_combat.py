# test_units.py
import pytest
from unittest.mock import patch
from pikeman import Pikeman
from knight import Knight
from crossbowman import Crossbowman


class TestPikeman:
    """Tests for the Pikeman class"""
    
    def setup_method(self):
        """inialise a Pikeman and a Knight before each test"""
        self.pikeman = Pikeman()
        self.knight = Knight()
    
    def test_init_values(self):
        """verify correct initialization of stats"""
        assert self.pikeman.hp == 55
        assert self.pikeman.baseMelee == 4
        assert self.pikeman.mountedUnits == 22
        assert self.pikeman.reloadTime == 3
        assert self.pikeman.cooldown == 0
    
    def test_melee_reach(self):
        """verify melee reach calculation"""
        assert self.pikeman._melee_reach() == 1.0
    
    def test_calculate_damage_vs_knight(self):
        """verify damage calculation against a Knight"""
        damage = self.pikeman._calculate_damage(self.knight)
        # baseMelee (4) - armor (2) + mountedUnits bonus (22) = 24
        assert damage == 24.0
    
    def test_calculate_damage_minimum(self):
        """verify minimum damage is 1"""
        high_armor_target = Knight()
        high_armor_target.armor = 100  # excessive armor
        damage = self.pikeman._calculate_damage(high_armor_target)
        assert damage == 1.0
    
    def test_attaquer_success(self):
        """verify a successful attack"""
        initial_hp = self.knight.hp
        damage = self.pikeman.attaquer(self.knight, distance=0.5)
        
        assert damage == 24.0
        assert self.knight.hp == initial_hp - 24.0
        assert self.pikeman.cooldown == 3  # Cooldown activé
    
    def test_attaquer_out_of_range(self):
        """verify cannot attack out of range"""
        damage = self.pikeman.attaquer(self.knight, distance=5.0)
        assert damage == 0
        assert self.pikeman.cooldown == 0  # Pas de cooldown si pas d'attaque
    
    def test_attaquer_on_cooldown(self):
        """verify cannot attack while on cooldown"""
        # first attack
        self.pikeman.attaquer(self.knight, distance=0.5)
        initial_hp = self.knight.hp
        
        # immediate second attack(has to fail)
        damage = self.pikeman.attaquer(self.knight, distance=0.5)
        assert damage == 0
        assert self.knight.hp == initial_hp  # HP inchanged
    
    def test_attaquer_dead_target(self):
        """verify cannot attack a dead target"""
        self.knight.hp = 0
        damage = self.pikeman.attaquer(self.knight, distance=0.5)
        assert damage == 0
    
    def test_tick_reduces_cooldown(self):
        """verify tick reduces cooldown correctly"""
        self.pikeman.cooldown = 3.0
        self.pikeman.tick(1.0)
        assert self.pikeman.cooldown == 2.0
        
        self.pikeman.tick(1.5)
        assert self.pikeman.cooldown == 0.5
        
        self.pikeman.tick(1.0)
        assert self.pikeman.cooldown == 0.0  # does not go negative
    
    def test_attaquer_kills_target(self):
        """Vérifie que l'attaque tue la cible si HP <= 0"""
        self.knight.hp = 20  # less than damage
        self.pikeman.attaquer(self.knight, distance=0.5)
        assert self.knight.hp == 0


class TestKnight:
    """tests for the Knight class"""
    
    def setup_method(self):
        """inialise a Knight and a Pikeman before each test"""
        self.knight = Knight()
        self.target = Pikeman()
        self.knight.position = (0, 0)
        self.target.position = (0, 0)
    
    def test_init_values(self):
        """verify correct initialization of stats"""
        assert self.knight.hp == 100
        assert self.knight.baseMelee == 10
        assert self.knight.armor == 2
        assert self.knight.reloadTime == 1.8
        assert self.knight.isAlive == True
    
    def test_calculate_distance_same_position(self):
        """verify distance calculation for same positions"""
        distance = self.knight._calculate_distance(self.target)
        assert distance == 0.0
    
    def test_calculate_distance_different_positions(self):
        """verify distance calculation for different positions"""
        self.target.position = (3, 4)  # Triangle 3-4-5
        distance = self.knight._calculate_distance(self.target)
        assert distance == 5.0
    
    def test_calculate_damage_vs_pikeman(self):
        """verify damage calculation against a Pikeman"""
        damage = self.knight._calculate_damage(self.target)
        # baseMelee (10) - armor (0) = 10
        assert damage == 10.0
    
    def test_calculate_damage_minimum(self):
        """verify minimum damage is 1"""
        high_armor_target = Pikeman()
        high_armor_target.armor = 100
        damage = self.knight._calculate_damage(high_armor_target)
        assert damage == 1.0
    
    def test_attaquer_success(self):
        """verify a successful attack"""
        initial_hp = self.target.hp
        result = self.knight.attaquer(self.target, currentTime=2.0)
        
        assert result == True
        assert self.target.hp == initial_hp - 10.0
        assert self.knight.lastAttackTime == 2.0
    
    def test_attaquer_on_cooldown(self):
        """verify cannot attack during cooldown"""
        self.knight.attaquer(self.target, currentTime=0)
        initial_hp = self.target.hp
        
        # Attempt at 1 second (cooldown = 1.8s)
        result = self.knight.attaquer(self.target, currentTime=1.0)
        assert result == False
        assert self.target.hp == initial_hp  # HP inchanged
    
    def test_attaquer_after_cooldown(self):
        """verify can attack after cooldown"""
        self.knight.attaquer(self.target, currentTime=0)
        
        # attack after 2seconds  (> 1.8s cooldown)
        result = self.knight.attaquer(self.target, currentTime=2.0)
        assert result == True
    
    def test_attaquer_kills_target(self):
        """verify attack kills target if HP <= 0"""
        self.target.hp = 5  # Moins que les dégâts
        self.knight.attaquer(self.target, currentTime=2)
        
        assert self.target.hp <= 0
        assert self.target.isAlive == False
    
    def test_attaquer_dead_attacker(self):
        """verify a dead Knight cannot attack"""
        self.knight.isAlive = False
        result = self.knight.attaquer(self.target, currentTime=0)
        assert result == False
    
    def test_attaquer_dead_target(self):
        """verify cannot attack a dead target"""
        self.target.isAlive = False
        result = self.knight.attaquer(self.target, currentTime=0)
        assert result == False


class TestCrossbowman:
    """Tests for the Crossbowman class"""
    
    def setup_method(self):
        """inialise a Crossbowman andthe target before each test"""
        self.crossbowman = Crossbowman()
        self.target = Pikeman()
    
    def test_init_values(self):
        """verify correct initialization of stats"""
        assert self.crossbowman.hp == 35
        assert self.crossbowman.basePierceAttack == 5
        assert self.crossbowman.range == 5
        assert self.crossbowman.accuracy == 85
        assert self.crossbowman.spearUnits == 3  # Bonus vs pikeman
    
    @patch('random.randint', return_value=50)  # Force a hit (50 < 85)
    def test_attaquer_success_vs_pikeman(self, mock_random):
        """verify a successful attack against a Pikeman with bonus"""
        initial_hp = self.target.hp
        damage = self.crossbowman.attaquer(self.target, distance=4.0)
        
        # basePierceAttack (5) - pierceArmor (0) + spearUnits bonus (3) = 8
        assert damage == 8.0
        assert self.target.hp == initial_hp - 8.0
    
    @patch('random.randint', return_value=50)
    def test_attaquer_success_vs_knight(self, mock_random):
        """verify a successful attack against a Knight without bonus"""
        knight = Knight()
        initial_hp = knight.hp
        damage = self.crossbowman.attaquer(knight, distance=4.0)
        
        # basePierceAttack (5) - pierceArmor (2) = 3
        assert damage == 3.0
        assert knight.hp == initial_hp - 3.0
    
    @patch('random.randint', return_value=90)  # Force un miss (90 > 85)
    def test_attaquer_miss(self, mock_random):
        """verify a missed attack does no damage"""
        initial_hp = self.target.hp
        damage = self.crossbowman.attaquer(self.target, distance=4.0)
        
        assert damage == 0
        assert self.target.hp == initial_hp
    
    def test_attaquer_out_of_range(self):
        """verify cannot attack out of range"""
        damage = self.crossbowman.attaquer(self.target, distance=10.0)
        assert damage == 0
    
    @patch('random.randint', return_value=50)
    def test_attaquer_minimum_damage(self, mock_random):
        """verify minimum damge is 1"""
        high_armor_target = Knight()
        high_armor_target.pierceArmor = 100
        damage = self.crossbowman.attaquer(high_armor_target, distance=4.0)
        assert damage == 1.0
    
    @patch('random.randint', return_value=50)
    def test_attaquer_with_elevation(self, mock_random):
        """Verify that k_elev modifies damage"""
        damage_normal = self.crossbowman.attaquer(self.target, distance=4.0, k_elev=1.0)
        
        # Reset target HP
        self.target.hp = 55
        damage_elevated = self.crossbowman.attaquer(self.target, distance=4.0, k_elev=1.5)
        
        assert damage_elevated == damage_normal * 1.5
    
    @patch('random.randint', return_value=50)
    def test_attaquer_kills_target(self, mock_random):
        """Verify that the attack kills the target if HP <= 0"""
        self.target.hp = 5
        self.crossbowman.attaquer(self.target, distance=4.0)
        assert self.target.hp == 0


class TestCombatScenarios:
    """Tests for complete combat scenarios"""
    
    def test_pikeman_vs_knight_full_fight(self):
        """Simulates a full Pikeman vs Knight combat"""
        pikeman = Pikeman()
        knight = Knight()
        
        # The Pikeman attacks (should deal 24 damage)
        damage = pikeman.attaquer(knight, distance=0.5)
        assert knight.hp == 76.0  # 100 - 24
        
        # The Pikeman must wait for his cooldown
        assert pikeman.cooldown == 3.0  # Cooldown should still be active
        for _ in range(6):  # 6 ticks de 0.5s = 3s
            pikeman.tick(0.5)
        
        # The Pikeman can attack again
        damage = pikeman.attaquer(knight, distance=0.5)
        assert knight.hp == 52.0  # 76 - 24
    
    @patch('random.randint', return_value=50)
    def test_crossbowman_vs_pikeman_multiple_shots(self, mock_random):
        """Simule plusieurs tirs du Crossbowman sur un Pikeman"""
        crossbowman = Crossbowman()
        pikeman = Pikeman()
        
        # First shot: 55 - 8 = 47 HP
        crossbowman.attaquer(pikeman, distance=4.0)
        assert pikeman.hp == 47.0
        
        #Second shot : 47 - 8 = 39 HP
        crossbowman.attaquer(pikeman, distance=4.0)
        assert pikeman.hp == 39.0


# Pour exécuter les tests : pytest test_units.py -v