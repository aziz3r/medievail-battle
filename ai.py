# ai.py
from __future__ import annotations
from typing import List, Any, Tuple

from game import Game

# Type d'action:
# ("move", unit, new_row, new_col)
# ("attack", attacker, target)
Action = Tuple[Any, ...]


class BaseController:
    def __init__(self, team: str):
        self.team = team

    def decide_actions(self, game: Game) -> List[Action]:
        raise NotImplementedError


class CaptainBraindead(BaseController):
    """
    Captain BRAINDEAD (IA n°1)
    - Ne donne aucun ordre de déplacement.
    - Les unités n'attaquent que si un ennemi est déjà dans leur ligne de vue
      et (idéalement) à portée.
    - Sinon elles ne font rien.
    """

    def decide_actions(self, game: Game) -> List[Action]:
        actions: List[Action] = []
        my_units = game.alive_units_of_team(self.team)
        enemies = game.enemy_units_of(self.team)

        for u in my_units:
            if not enemies:
                continue

            best_target = None
            best_dist = float("inf")

            los = float(getattr(u, "lineOfSight", 0.0))

            # On ne considère que les ennemis dans la line of sight
            for e in enemies:
                dist = game.map.distance(u, e)
                if dist <= los:
                    if dist < best_dist:
                        best_dist = dist
                        best_target = e

            if best_target is None:
                # Rien en vue -> aucune action
                continue

            # S'il est dans la portée d'attaque, on attaque
            if hasattr(u, "in_range") and u.in_range(best_dist):
                actions.append(("attack", u, best_target))
            # Sinon, Braindead ne bouge pas → aucune action

        return actions


class MajorDaft(BaseController):
    """
    Major DAFT (IA n°2)
    - Ordonne à chaque unité d'attaquer l'ENNEMI LE PLUS PROCHE,
      sans aucune autre considération.
    - Si l'ennemi est à portée -> attaque.
    - Sinon -> se rapproche d'une case vers lui (avance en ligne droite).
    """

    def decide_actions(self, game: Game) -> List[Action]:
        actions: List[Action] = []
        my_units = game.alive_units_of_team(self.team)

        for u in my_units:
            target = game.find_closest_enemy(u)
            if target is None:
                continue

            dist = game.map.distance(u, target)

            # Si on peut frapper, on frappe
            if hasattr(u, "in_range") and u.in_range(dist):
                actions.append(("attack", u, target))
                continue

            # Sinon on avance d'UNE case vers la cible (IA débile mais agressive)
            old_row, old_col = int(getattr(u, "y", 0)), int(getattr(u, "x", 0))
            target_row, target_col = int(getattr(target, "y", 0)), int(getattr(target, "x", 0))

            new_row, new_col = old_row, old_col

            if old_row < target_row:
                new_row = old_row + 1
            elif old_row > target_row:
                new_row = old_row - 1
            else:
                if old_col < target_col:
                    new_col = old_col + 1
                elif old_col > target_col:
                    new_col = old_col - 1

            actions.append(("move", u, new_row, new_col))

        return actions


class SimpleAI(MajorDaft):
    """
    Alias de MajorDaft pour compatibilité avec l'ancien code.
    Même comportement que MajorDaft.
    """
    pass

class GeneralSmart(BaseController):
    def __init__(self, team_id):
        super().__init__(team_id)
        self.name = "General SMART"

    def decide_actions(self, game):
        # Une stratégie plus intelligente ici...
        return []