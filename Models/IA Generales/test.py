# Models/IA Generales/test.py

import os
import sys

# === 1) Ajouter la racine du projet dans le PYTHONPATH ===

THIS_DIR = os.path.dirname(__file__)                 # .../Models/IA Generales
MODELS_DIR = os.path.dirname(THIS_DIR)               # .../Models
PROJECT_DIR = os.path.dirname(MODELS_DIR)            # .../python-project-2025-2026-main-2

# On ajoute la racine du projet dans le path
sys.path.append(PROJECT_DIR)

# === 2) Imports des classes ===
# Maintenant on peut utiliser le chemin complet des modules

from Entity.Unit.knight import Knight
from Entity.Unit.pikeman import Pikeman
from Entity.Unit.crossbowman import Crossbowman
from Models.Map.Map import BattleMap   # Map.py -> classe BattleMap
"""
from Models.IA_Generales.captainBraindead import CapitainBraindead
from Models.IA_Generales.general import General
from Models.IA_Generales.majorDraft import MajorDaft
"""

# === 3) Création de la map et des unités ===

if __name__ == "__main__":
    # Map 5x5
    battle_map = BattleMap(rows=5, cols=5)

    # Unités
    k1 = Knight()
    k2 = Knight()
    p1 = Pikeman()
    c1 = Crossbowman()

    # Placement : même format que tu utilisais déjà -> ['r', unit]
    # (ligne, colonne)
    battle_map.add_unit(1, 1, "r", k1)  # Knight rouge
    battle_map.add_unit(1, 3, "r", k2)  # autre Knight rouge
    battle_map.add_unit(3, 1, "b", p1)  # Pikeman bleu
    battle_map.add_unit(2, 2, "b", c1)  # Archer bleu

    print("=== MAP ASCII ===")
    battle_map.print_ascii()

    # Exemple si plus tard tu veux brancher la Simulation :
    # from Models.IA Generales.projet import Simulation, Violent, Braindead
    # Map1 = battle_map.to_matrix()
    # print(Simulation(Map1, Violent, Braindead))

    def creationCrossbowmans (nb, equipe_choix):
        n = nb
        crossbowmans = {f'crossbowman{i}': Crossbowman() for i in range(1, n + 1)}
        for i in range(1, n + 1):
            crossbowmans[f'crossbowman{i}'].equipe = equipe_choix
        return crossbowmans
    
    def creationPikemans (nb, equipe_choix):
        n = nb
        pikemans = {f'pikeman{i}': Pikeman() for i in range(1, n + 1)}
        for i in range(1, n + 1):
            pikemans[f'pikeman{i}'].equipe = equipe_choix
        return pikemans
    
    def creationKnights (nb, equipe_choix):
        n = nb
        knights = {f'knight{i}': Knight() for i in range(1, n + 1)}
        for i in range(1, n + 1):
            knights[f'knight{i}'].equipe = equipe_choix
        return knights
    
    def creer_unites_selon_type(type_unite, nb, equipe):
        if type_unite == "crossbowman":
            return creationCrossbowmans(nb, equipe)
        elif type_unite == "pikeman":
            return creationPikemans(nb, equipe)
        elif type_unite == "knight":
            return creationKnights(nb, equipe)
        else:
            raise ValueError("Type inconnu : utilise 'crossbowman', 'pikeman' ou 'knight'")
    
    def scenario_lanchester(type_unite, N, battlemap: BattleMap):
        """
        Crée un scénario N vs 2N conforme aux lois de Lanchester.
        - type_unite: "crossbowman", "pikeman" ou "knight"
        - N: nombre de soldats de base
        - battlemap: instance de BattleMap
        """
    
        # Armée rouge (A) = N soldats
        army_A = creer_unites_selon_type(type_unite, N, "r")
    
        # Armée bleue (B) = 2*N soldats
        army_B = creer_unites_selon_type(type_unite, 2 * N, "b")
    
        # Placement
        rows = battlemap.rows
        cols = battlemap.cols
    
        # Lignes fixes (face à face)
        row_A = 1
        row_B = rows - 2   # avant-dernière ligne
    
        col_start = 1
    
        # ---- Placement armée A ----
        col = col_start
        for unit in army_A.values():
            battlemap.add_unit(row_A, col, "r", unit)
            col += 1
            if col >= cols - 1:
                col = col_start
                row_A += 1
    
        # ---- Placement armée B ----
        col = col_start
        for unit in army_B.values():
            battlemap.add_unit(row_B, col, "b", unit)
            col += 1
            if col >= cols - 1:
                col = col_start
                row_B -= 1  # bleu avance vers le haut pour rester face aux rouges
    
        return army_A, army_B
    
        print(len(armyB))  # 40
    
    grille = BattleMap(rows=10, cols=15)  # dimensions suffisantes pour placer les unités
    
    armyA, armyB = scenario_lanchester("crossbowman", 15, grille)
    
    print("Nombre d'unités armée A :", len(armyA))  # devrait être 20
    print("Nombre d'unités armée B :", len(armyB))  # devrait être 40
    
    grille.print_ascii()
    
