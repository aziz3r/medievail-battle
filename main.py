# main.py

import os
import time

from map import BattleMap
from game import Game
from ai import CaptainBraindead, MajorDaft

from knight import Knight
from pikeman import Pikeman
from crossbowman import Crossbowman


TEAM_INFO = {
    "A": {"name": "Kingdom of the North", "color": "Bleu", "ia": "MajorDaft (agressive)"},
    "B": {"name": "Empire of the South", "color": "Rouge", "ia": "Captain BRAINDEAD (statique)"},
}


# -------------------------------------------------------------
# Scénario : IA agressive (A) vs défense statique (B)
# -------------------------------------------------------------
def build_simple_vs_braindead_battle() -> Game:
    rows, cols = 20, 20
    battle_map = BattleMap(rows=rows, cols=cols)

    controllers = {
        "A": MajorDaft("A"),          # IA qui avance et attaque
        "B": CaptainBraindead("B"),  # IA statique
    }

    game = Game(battle_map, controllers)

    # ---------------------------------------------------------
    # ARMÉE A (à gauche) — IA agressive
    # - front de piquiers
    # - quelques knights derrière
    # - quelques archers
    # ---------------------------------------------------------
    # ligne de piquiers
    for r in range(6, 11):      # rows 6 → 10
        game.add_unit(Pikeman(), "A", row=r, col=3)

    # knights
    for r in range(7, 10):
        game.add_unit(Knight(), "A", row=r, col=2)

    # crossbowmen
    for r in range(6, 11, 2):
        game.add_unit(Crossbowman(), "A", row=r, col=1)

    # ---------------------------------------------------------
    # ARMÉE B (à droite) — CaptainBraindead
    # - front de piquiers plus dense
    # - quelques knights
    # - ligne d'arbalétriers en fond
    # ---------------------------------------------------------
    # ligne de piquiers
    for r in range(6, 12):      # rows 6 → 11
        game.add_unit(Pikeman(), "B", row=r, col=cols - 4)   # col=16

    # knights
    for r in range(7, 11, 2):
        game.add_unit(Knight(), "B", row=r, col=cols - 5)    # col=15

    # crossbowmen
    for r in range(5, 13, 2):
        game.add_unit(Crossbowman(), "B", row=r, col=cols - 3)  # col=17

    return game


# -------------------------------------------------------------
# Affichage
# -------------------------------------------------------------
def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def compute_team_stats(game: Game):
    stats = {}
    for u in game.alive_units():
        team = getattr(u, "team", "?")
        if team not in stats:
            stats[team] = {"units": 0, "total_hp": 0.0, "by_type": {}}
        stats[team]["units"] += 1
        stats[team]["total_hp"] += float(u.hp)
        tname = type(u).__name__
        stats[team]["by_type"][tname] = stats[team]["by_type"].get(tname, 0) + 1
    return stats


def render(game: Game):
    print(f"Temps simulé : {game.time:.1f}")
    stats = compute_team_stats(game)

    print("=== État des armées ===")
    for team, st in stats.items():
        info = TEAM_INFO.get(team, {})
        label = info.get("name", f"Équipe {team}")
        color = info.get("color", "?")
        ia_name = info.get("ia", "?")
        print(
            f"- {label} (team={team}, couleur={color}, IA={ia_name}) : "
            f"{st['units']} unités en vie, HP total ≈ {st['total_hp']:.1f}"
        )
        compo = ", ".join(f"{cnt}x {t}" for t, cnt in st["by_type"].items())
        print(f"    Composition : {compo}")
    print()

    print("Unités en vie :")
    for u in game.alive_units():
        print(
            f"- {type(u).__name__} (team={u.team}), "
            f"HP={u.hp:.1f}, pos=({u.x:.0f},{u.y:.0f})"
        )
    print()

    print("Carte :")
    game.map.print_ascii()

    print("Événements récents :")
    for log in game.logs[-7:]:
        print(" ", log)
    print()


# -------------------------------------------------------------
# Boucle principale
# -------------------------------------------------------------
def main():
    game = build_simple_vs_braindead_battle()

    max_turns = 200
    turn = 0

    while not game.is_finished() and turn < max_turns:
        turn += 1
        game.step(dt=1.0)

        clear_terminal()
        print(f"===== Tour {turn} =====")
        render(game)

        time.sleep(0.4)

    print("===== Fin de la bataille =====")
    render(game)

    winner = game.get_winner()
    if winner is None:
        print("Match nul.")
    else:
        info = TEAM_INFO.get(winner, {})
        label = info.get("name", f"Équipe {winner}")
        ia_name = info.get("ia", "?")
        print(f"Victoire de {label} (team {winner}, IA={ia_name}) !")


if __name__ == "__main__":
    main()
