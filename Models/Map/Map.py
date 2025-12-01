# Models/Map/Map.py

class BattleMap:
    """
    Map très simple :
    - une grille rows x cols
    - chaque case contient une liste d'unités [ [team, unit], ... ]
    """

    def __init__(self, rows: int = 5, cols: int = 5):
        self.rows = rows
        self.cols = cols
        # grid[i][j] = liste d'unités dans la case (i, j)
        self.grid = [[[] for _ in range(cols)] for _ in range(rows)]

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def add_unit(self, row: int, col: int, team: str, unit) -> None:
        """
        Ajoute une unité sur la case (row, col)
        team = 'r' (rouge), 'b' (bleu), etc.
        unit = objet Knight / Pikeman / Crossbowman...
        """
        if not self.in_bounds(row, col):
            raise ValueError(f"Case ({row}, {col}) hors de la map")
        self.grid[row][col].append([team, unit])

    def remove_unit(self, row: int, col: int, team: str, unit) -> None:
        """
        Supprime une unité morte de la case (row, col)
        team = 'r' (rouge), 'b' (bleu), etc.
        unit = objet Knight / Pikeman / Crossbowman...
        """
        for i in len(self.grid[row][col]): ## trouve la position de l'unité morte dans la case (row,col)
            if self.grid[row][col][i] == [team,unit]:
                indice=i
        self.grid[row][col] = self.grid[row][col][:indice] + self.grid[row][col][indice+1:] ## supprime l'unité
   

    def get_units(self, row: int, col: int):
        if not self.in_bounds(row, col):
            return []
        return self.grid[row][col]

    def to_matrix(self):
        """Retourne la matrice brute (pour l'utiliser dans Simulation)."""
        return self.grid

    def _symbol_for_cell(self, cell):
        """
        Pour l'affichage :
        - vide -> "."
        - chevalier rouge -> "Kr"
        - chevalier bleu -> "Kb"
        - etc.
        """
        if not cell:
            return " ."

        # On ne regarde que la première unité de la case pour l'affichage
        team, unit = cell[0]

        # Récupère le type d'unité pour choisir une lettre
        unit_name = type(unit).__name__.lower()

        if "knight" in unit_name:
            letter = "K"
        elif "pikeman" in unit_name:
            letter = "P"
        elif "crossbowman" in unit_name:
            letter = "C"
        else:
            letter = "U"  # Unit

        # Couleur d'équipe
        if team == "r":
            suffix = "r"
        elif team == "b":
            suffix = "b"
        else:
            suffix = "?"

        return f"{letter}{suffix}"

    def print_ascii(self):
        """Affiche la map dans le terminal."""
        for i in range(self.rows):
            row_str = ""
            for j in range(self.cols):
                row_str += self._symbol_for_cell(self.grid[i][j]) + " "
            print(row_str)
        print()  # ligne vide à la fin
