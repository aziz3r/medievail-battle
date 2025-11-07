# views/views.py
import os
import sys


from Models.Map.Map import GameMap
# CORRECTION 1 : L'import doit pointer vers Guerrier dans guerrier.py (tel que défini dans notre architecture).
from Entity.Unit.guerrier import Guerrier

# --- 2. VIEW CONFIGURATION ---
VIEW_WIDTH = 80
VIEW_HEIGHT = 20
SCROLL_STEP = 5

# --- 3. ANSI COLOR CODES ---
RESET = "\033[0m"
# Colors for elevation (0=Water, 1-2=Plain, 3+=Mountain)
ELEV_COLORS = [
    "\033[34m",  # Blue (Level 0)
    "\033[32m",  # Green (Level 1-2)
    "\033[92m",  # Light Green (Level 3-4)
    "\033[37m",  # Gray (Level 5+)
]
COLOR_PLAYER_1 = "\033[94m"  # Bright Blue
COLOR_PLAYER_2 = "\033[91m"  # Bright Red

# --- 4. TERMINAL VIEW CLASS ---

class TerminalView:
    """Manages the textual display of the map, units, and scrolling."""
    def __init__(self, game_map: GameMap):
        self.map = game_map
        self.view_x = 0  # Viewport top-left X coordinate
        self.view_y = 0  # Viewport top-left Y coordinate

    def _clear_screen(self):
        """Clears the terminal screen for a clean refresh."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _get_tile_symbol(self, elevation):
        """Returns the colored symbol for the terrain based on elevation."""
        color_index = min(elevation, len(ELEV_COLORS) - 1)
        color = ELEV_COLORS[color_index]

        if elevation == 0:
            return f"{color}~{RESET}" # Water
        elif elevation < 3:
            return f"{color}.{RESET}" # Plain
        else:
            return f"{color}#{RESET}" # Elevation

    # CORRECTION 2 : Changement du typage pour 'Guerrier' (lisibilité).
    def draw_map(self, units: list[Guerrier], tick=0):
        """Draws the visible map section and overlays units."""
        self._clear_screen()

        unit_positions = {}
        for unit in units:
            # Cette ligne Nécessite la méthode get_grid_coords() dans Guerrier.py
            unit_i, unit_j = unit.get_grid_coords()
            view_i = unit_i - self.view_y
            view_j = unit_j - self.view_x

            if 0 <= view_i < VIEW_HEIGHT and 0 <= view_j < VIEW_WIDTH:
                unit_positions[(view_i, view_j)] = unit

        output_lines = []
        for i in range(VIEW_HEIGHT):
            line = []
            for j in range(VIEW_WIDTH):

                if (i, j) in unit_positions:
                    # Draw Unit
                    unit = unit_positions[(i, j)]

                    # CORRECTION 3 : unit.unit_type n'existe pas. On utilise le nom de la classe (ex: Knight -> K).
                    symbol = type(unit).__name__[0].upper()

                    color = COLOR_PLAYER_1 if unit.player_id == 1 else COLOR_PLAYER_2
                    line.append(f"{color}{symbol}{RESET}")

                else:
                    # Draw Terrain
                    map_i = self.view_y + i
                    map_j = self.view_x + j

                    if 0 <= map_i < self.map.N and 0 <= map_j < self.map.M:
                        elevation = self.map.get_elevation(map_i, map_j)
                        line.append(self._get_tile_symbol(elevation))
                    else:
                        line.append(' ') # Space outside map bounds

                output_lines.append("".join(line))

        # Display everything
        print(f"--- AIge of EmpAIres: Terminal View (Tick: {tick}) ---")
        print(f"Viewport: ({self.view_x}, {self.view_y}) to ({self.view_x + VIEW_WIDTH - 1}, {self.view_y + VIEW_HEIGHT - 1})")
        print('\n'.join(output_lines))
        print("Controls: ZQSD to scroll, P to pause/resume, X to quit.")
        sys.stdout.flush()

    def move_viewport(self, dx: int, dy: int):
        """Moves the viewport, respecting map boundaries."""
        max_x = self.map.M - VIEW_WIDTH
        max_y = self.map.N - VIEW_HEIGHT

        self.view_x = max(0, min(max_x, self.view_x + dx))
        self.view_y = max(0, min(max_y, self.view_y + dy))