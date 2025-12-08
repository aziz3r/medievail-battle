# scenarios.py

from map import BattleMap
from game import Game
from ai import CaptainBraindead, MajorDaft

from knight import Knight
from pikeman import Pikeman
from crossbowman import Crossbowman


def scenario_simple_vs_braindead() -> Game:
    """
    Scénario 1 :
    - Équipe A : MajorDaft (agressive)
    - Équipe B : CaptainBraindead (statique)
    """
    rows, cols = 20, 20
    battle_map = BattleMap(rows=rows, cols=cols)

    controllers = {
        "A": MajorDaft("A", decision_interval=0.3),        # IA agressive, réfléchit souvent
        "B": CaptainBraindead("B", decision_interval=0.8), # IA lente / passive
    }

    game = Game(battle_map, controllers)

    # ARMÉE A (à gauche)
    for r in range(6, 11):
        game.add_unit(Pikeman(), "A", row=r, col=3)
    for r in range(7, 10):
        game.add_unit(Knight(), "A", row=r, col=2)
    for r in range(6, 11, 2):
        game.add_unit(Crossbowman(), "A", row=r, col=1)

    # ARMÉE B (à droite)
    for r in range(6, 12):
        game.add_unit(Pikeman(), "B", row=r, col=cols - 4)   # col=16
    for r in range(7, 11, 2):
        game.add_unit(Knight(), "B", row=r, col=cols - 5)    # col=15
    for r in range(5, 13, 2):
        game.add_unit(Crossbowman(), "B", row=r, col=cols - 3)  # col=17

    return game
