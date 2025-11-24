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

