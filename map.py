# map.py

class BattleMap:
    """
    Map sous forme de matrice row x col.
    Chaque case contient une unité ou None.
    """

    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def place_unit(self, unit, row, col):
        """Place une unité sur la map et met à jour sa position."""
        if not self.in_bounds(row, col):
            raise ValueError("Position hors de la map")

        if self.grid[row][col] is not None:
            raise ValueError("Case déjà occupée")

        self.grid[row][col] = unit
        unit.x = col
        unit.y = row

    def move_unit(self, unit, new_row, new_col):
        """Déplace une unité sur la map en respectant les collisions."""
        if not self.in_bounds(new_row, new_col):
            return False

        # ancienne position
        old_row, old_col = int(unit.y), int(unit.x)

        # vérifier que c'est bien lui sur la case
        if self.grid[old_row][old_col] != unit:
            return False

        if self.grid[new_row][new_col] is not None:
            # case occupée → pas de move
            return False

        # déplacer
        self.grid[old_row][old_col] = None
        self.grid[new_row][new_col] = unit

        unit.x = new_col
        unit.y = new_row

        return True

    
    def distance(self, u1, u2):
        """Distance de Manhattan simple."""
        return ( (u1.x - u2.x)**2 + (u1.y - u2.y)**2 ) ** 0.5

    def print_ascii(self):  
        """Affichage simple de la map."""
        for r in range(self.rows):
            row_str = ""
            for c in range(self.cols):
                u = self.grid[r][c]
                if u is None:
                    row_str += " . "
                else:
                    name = type(u).__name__[0]  # K / P / C
                    row_str += f" {name} "
            print(row_str)
        print()

    def get_unit(self, row, col):
        if not self.in_bounds(row, col):
            return None
        return self.grid[row][col]

    def remove_unit(self, unit):
        row, col = int(unit.y), int(unit.x)
        if self.in_bounds(row, col) and self.grid[row][col] == unit:
            self.grid[row][col] = None
