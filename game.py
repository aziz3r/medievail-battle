# game.py
"""
Moteur de bataille (logique du jeu).

- Indépendant de l'affichage (terminal ou graphique).
- Gère : unités, équipes, progression du temps, application des actions des IA.
- Les "généraux" (IA) sont des objets qui exposent une méthode decide_actions(game).
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Optional, Iterable, Any

from map import BattleMap

# Type simple pour une "action" proposée par une IA :
# ("move", unit, new_row, new_col)
# ("attack", attacker, target)
Action = Tuple[Any, ...]


class Game:
    def __init__(self, battle_map: BattleMap, controllers: Dict[str, Any]):
        """
        :param battle_map: instance de BattleMap (grille N x M)
        :param controllers: dictionnaire {team_id: controller}
            - team_id = string du genre "A", "B", "r", "b"...
            - controller = objet avec une méthode decide_actions(game) -> list[Action]
        """
        self.map: BattleMap = battle_map
        self.controllers: Dict[str, Any] = controllers

        # Liste de TOUTES les unités présentes dans la bataille
        self.units: List[Any] = []

        # Temps simulé (en secondes ou ticks arbitraires)
        self.time: float = 0.0

        # Indique si la partie est encore en cours
        self.running: bool = True

        # Gagnant éventuel ("A", "B", etc.)
        self.winner: Optional[str] = None

        self.logs: List[str] = []

    # ------------------------------------------------------------------
    # Gestion des unités / équipes
    # ------------------------------------------------------------------

    def add_unit(self, unit: Any, team: str, row: int, col: int) -> None:
        """Ajoute une unité à la partie, l'associe à une équipe et la place sur la map."""
        setattr(unit, "team", team)
        self.units.append(unit)
        self.map.place_unit(unit, row, col)

    def alive_units(self) -> List[Any]:
        """Retourne la liste des unités encore vivantes."""
        return [u for u in self.units if getattr(u, "hp", 0) > 0]

    def alive_units_of_team(self, team: str) -> List[Any]:
        """Unités vivantes appartenant à une équipe donnée."""
        return [u for u in self.alive_units() if getattr(u, "team", None) == team]

    def enemy_units_of(self, team: str) -> List[Any]:
        """Unités vivantes qui NE sont PAS dans l'équipe 'team'."""
        return [u for u in self.alive_units() if getattr(u, "team", None) != team]

    # ------------------------------------------------------------------
    # Recherche d'ennemis
    # ------------------------------------------------------------------

    def find_closest_enemy(self, unit: Any) -> Optional[Any]:
        """Renvoie l'ennemi vivant le plus proche de 'unit'."""
        team = getattr(unit, "team", None)
        enemies = self.enemy_units_of(team)
        if not enemies:
            return None

        best_target = None
        best_dist = float("inf")
        for e in enemies:
            d = self.map.distance(unit, e)
            if d < best_dist:
                best_dist = d
                best_target = e
        return best_target

    # ------------------------------------------------------------------
    # Boucle de jeu : un "pas" de simulation
    # ------------------------------------------------------------------

    def step(self, dt: float = 1.0) -> None:
        """
        Effectue un pas de simulation :
        - demande à chaque IA les actions à effectuer
        - applique ces actions
        - fait avancer le temps
        - nettoie les morts
        - vérifie les conditions de victoire
        """
        if not self.running:
            return

        # 1) actions des IA
        all_actions: List[Action] = []
        for team, controller in self.controllers.items():
            if not self.alive_units_of_team(team):
                continue
            if not hasattr(controller, "decide_actions"):
                continue
            actions = controller.decide_actions(self)
            if actions:
                all_actions.extend(actions)

        # 2) appliquer les actions
        self.apply_actions(all_actions)

        # 3) tick sur les unités
        for u in self.alive_units():
            if hasattr(u, "tick"):
                u.tick(dt)

        # 4) nettoyer les morts
        self.cleanup_dead_units()

        # 5) temps + victoire
        self.time += dt
        self.check_victory_conditions()

    # ------------------------------------------------------------------
    # Application des actions
    # ------------------------------------------------------------------

    def apply_actions(self, actions: Iterable[Action]) -> None:
        for action in actions:
            if not action:
                continue
            kind = action[0]

            if kind == "move":
                _, unit, new_row, new_col = action
                self._do_move(unit, int(new_row), int(new_col))

            elif kind == "attack":
                _, attacker, target = action
                self._do_attack(attacker, target)

    def _do_move(self, unit: Any, new_row: int, new_col: int) -> bool:
        if getattr(unit, "hp", 0) <= 0:
            return False
        return self.map.move_unit(unit, new_row, new_col)

    def _do_attack(self, attacker: Any, target: Any) -> None:
        """
        Effectue une attaque si possible.
        C'est l'unité elle-même qui gère:
        - can_strike(distance, target)
        - calcul des dégâts
        - application des dégâts
        - cooldown
        """
        if getattr(attacker, "hp", 0) <= 0:
            return
        if getattr(target, "hp", 0) <= 0:
            return
        if not hasattr(attacker, "attaquer"):
            return

        dist = self.map.distance(attacker, target)
        dmg = attacker.attaquer(target, dist)

        # On ajoute un log lisible
        try:
            dmg_val = float(dmg) if dmg is not None else 0.0
        except (TypeError, ValueError):
            dmg_val = 0.0

        att_name = type(attacker).__name__
        tgt_name = type(target).__name__
        att_team = getattr(attacker, "team", "?")
        tgt_team = getattr(target, "team", "?")

        self.logs.append(
            f"{att_team}:{att_name} → {tgt_team}:{tgt_name} | "
            f"{dmg_val:.1f} dmg (dist={dist:.0f}, HP cible={target.hp:.1f})"
        )


    # ------------------------------------------------------------------
    # Gestion des morts / fin de partie
    # ------------------------------------------------------------------

    def cleanup_dead_units(self) -> None:
        """Retire de la map les unités dont les HP sont à 0."""
        for u in self.units:
            if getattr(u, "hp", 0) > 0:
                continue
            row, col = int(getattr(u, "y", -1)), int(getattr(u, "x", -1))
            if 0 <= row < self.map.rows and 0 <= col < self.map.cols:
                if self.map.grid[row][col] is u:
                    self.map.grid[row][col] = None

    def check_victory_conditions(self) -> None:
        alive = self.alive_units()
        if not alive:
            self.running = False
            self.winner = None
            return

        teams_alive = {getattr(u, "team", None) for u in alive}
        teams_alive.discard(None)
        if len(teams_alive) == 1:
            self.running = False
            self.winner = next(iter(teams_alive))

    # ------------------------------------------------------------------
    # Utilitaires
    # ------------------------------------------------------------------

    def is_finished(self) -> bool:
        return not self.running

    def get_winner(self) -> Optional[str]:
        return self.winner
