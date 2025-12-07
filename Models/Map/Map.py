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

    def inBounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def addUnit(self, row: int, col: int, team: str, unit) -> None:
        """
        Ajoute une unité sur la case (row, col)
        team = 'r' (rouge), 'b' (bleu), etc.
        unit = objet Knight / Pikeman / Crossbowman...
        """
        if not self.inBounds(row, col):
            raise ValueError(f"Case ({row}, {col}) hors de la map")
        self.grid[row][col].append([team, unit])

    def removeUnit(self, row: int, col: int, team: str, unit) -> None:
        """
        Supprime une unité morte de la case (row, col)
        team = 'r' (rouge), 'b' (bleu), etc.
        unit = objet Knight / Pikeman / Crossbowman...
        """
        for i in len(self.grid[row][col]): ## trouve la position de l'unité morte dans la case (row,col)
            if self.grid[row][col][i] == [team,unit]:
                indice=i
        self.grid[row][col] = self.grid[row][col][:indice] + self.grid[row][col][indice+1:] ## supprime l'unité
   

    def getUnits(self, row: int, col: int):
        if not self.inBounds(row, col):
            return []
        return self.grid[row][col]

    def toMatrix(self):
        """Retourne la matrice brute (pour l'utiliser dans Simulation)."""
        return self.grid

    def symbolForCell(self, cell):
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
        unitName = type(unit).__name__.lower()

        if "knight" in unitName:
            letter = "K"
        elif "pikeman" in unitName:
            letter = "P"
        elif "crossbowman" in unitName:
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

    def printAscii(self):
        """Affiche la map dans le terminal."""
        for i in range(self.rows):
            rowStr = ""
            for j in range(self.cols):
                rowStr += self.symbolForCell(self.grid[i][j]) + " "
            print(rowStr)
        print()  # ligne vide à la fin
