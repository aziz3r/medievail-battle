import random

MAP_N = 120           # Required minimum height (rows)
MAP_M = 120           # Required minimum width (columns)
MAX_ELEVATION = 16    # Max elevation level for damage modifiers

# --- GAME MAP CLASS ---

class GameMap:

    def __init__(self, N=MAP_N, M=MAP_M):
        self.N = N
        self.M = M
        self.tiles = self._generate_terrain()

    def _generate_terrain(self):

        tiles = []
        for i in range(self.N):
            row = []
            for j in range(self.M):
                elevation = random.randint(0, 5)
                tile_properties = {
                    'elevation': elevation,
                    'is_impassable': False,
                }
                row.append(tile_properties)
            tiles.append(row)
        return tiles

    def get_elevation(self, i: int, j: int) -> int:

        if 0 <= i < self.N and 0 <= j < self.M:
            return self.tiles[i][j]['elevation']
        # Default elevation if outside map bounds
        return 0

    def get_elevation_at_position(self, x: float, y: float) -> int:

        i = int(y)
        j = int(x)

        return self.get_elevation(i, j)

# --- QUICK TEST EXAMPLE ---
if __name__ == "__main__":
    test_map = GameMap(N=20, M=20)

    # Check elevation at a specific continuous position
    x_pos, y_pos = 12.8, 14.1
    elev = test_map.get_elevation_at_position(x_pos, y_pos)
    print(f"Elevation at ({x_pos}, {y_pos}): {elev}")