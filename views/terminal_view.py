import curses
import time
import os
import webbrowser
from dataclasses import dataclass

@dataclass
class Camera:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

    def move(self, dx, dy, limit_w, limit_h):
        self.x = max(0, min(limit_w - self.width, self.x + dx))
        self.y = max(0, min(limit_h - self.height, self.y + dy))
        
    def center_on(self, target_x, target_y, limit_w, limit_h):
        """ Place la caméra pour que (target_x, target_y) soit au centre """
        self.x = target_x - (self.width // 2)
        self.y = target_y - (self.height // 2)
        # On reste dans les limites
        self.x = max(0, min(limit_w - self.width, self.x))
        self.y = max(0, min(limit_h - self.height, self.y))

class TerminalView:
    UNIT_CHARS = {
        'Knight': 'K', 'Pikeman': 'P', 'Crossbowman': 'C',
        'Castle': '#', 'Wonder': 'W'
    }

    def __init__(self, game):
        self.game = game
        self.map = game.map
        self.stdscr = None
        
        self.camera = Camera(0, 0, 0, 0)
        self.paused = False
        self.message = ""
        self.tick_speed = 30
        
        # --- INTELLIGENCE CAMÉRA ---
        self.auto_follow = True  # Activé par défaut

        # Couleurs
        self.COLOR_A = 1
        self.COLOR_B = 2
        self.COLOR_UI = 3

    def start(self):
        """ Point d'entrée principal """
        curses.wrapper(self._main_loop)

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(self.COLOR_A, curses.COLOR_CYAN, -1)
        curses.init_pair(self.COLOR_B, curses.COLOR_RED, -1)
        curses.init_pair(self.COLOR_UI, curses.COLOR_YELLOW, -1)
        curses.curs_set(0) 

    def _update_camera_auto(self):
        """ Calcule le barycentre des unités pour centrer la caméra """
        if not self.auto_follow: return

        units = self.game.alive_units()
        if not units: return

        # Moyenne des positions X et Y
        sum_x = sum(float(getattr(u, 'x', 0)) for u in units)
        sum_y = sum(float(getattr(u, 'y', 0)) for u in units)
        avg_x = int(sum_x / len(units))
        avg_y = int(sum_y / len(units))

        # Application
        self.camera.center_on(avg_x, avg_y, self.map.cols, self.map.rows)

    def _main_loop(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.nodelay(True)
        self._init_colors()

        last_time = time.time()

        while not self.game.is_finished():
            # 1. Gestion Entrées
            self._handle_input()

            # 2. Logique
            if not self.paused:
                current_time = time.time()
                if current_time - last_time > (1 / self.tick_speed):
                    self.game.step(dt=0.1)
                    last_time = current_time

            # 3. Mise à jour Caméra Auto
            self._update_camera_auto()

            # 4. Affichage
            self._draw()
            time.sleep(0.01)

        self._draw_game_over()

    def _handle_input(self):
        try: key = self.stdscr.getch()
        except: return
        if key == -1: return

        # --- ZQSD : DÉSACTIVE LE MODE AUTO ---
        if key in [ord('z'), ord('Z')]: 
            self.auto_follow = False
            self.camera.move(0, -1, self.map.cols, self.map.rows)
        elif key in [ord('s'), ord('S')]: 
            self.auto_follow = False
            self.camera.move(0, 1, self.map.cols, self.map.rows)
        elif key in [ord('q'), ord('Q')]: 
            self.auto_follow = False
            self.camera.move(-1, 0, self.map.cols, self.map.rows)
        elif key in [ord('d'), ord('D')]: 
            self.auto_follow = False
            self.camera.move(1, 0, self.map.cols, self.map.rows)
        
        # --- 'A' ou 'C' : RÉACTIVE LE MODE AUTO ---
        elif key in [ord('a'), ord('A'), ord('c'), ord('C')]:
            self.auto_follow = True
            self.message = "CAMÉRA AUTO"

        # Pause
        elif key in [ord('p'), ord('P')]:
            self.paused = not self.paused
            self.message = "PAUSE" if self.paused else ""

        # Snapshot HTML
        elif key == 9: # TAB
            self.paused = True
            self.generate_html_snapshot()
            self.message = "SNAPSHOT HTML !"

        # Vitesse
        elif key == ord('+'): self.tick_speed += 5
        elif key == ord('-'): self.tick_speed = max(1, self.tick_speed - 5)

        # Quitter
        elif key == 27: exit()

    def _draw(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        ui_height = 4
        map_h = h - ui_height - 2
        map_w = w - 2
        
        self.camera.width = min(self.map.cols, map_w)
        self.camera.height = min(self.map.rows, map_h)

        self._draw_border(0, 0, map_w + 2, map_h + 2)

        for unit in self.game.alive_units():
            ux = int(unit.x) - self.camera.x
            uy = int(unit.y) - self.camera.y

            if 0 <= ux < self.camera.width and 0 <= uy < self.camera.height:
                char = self.UNIT_CHARS.get(type(unit).__name__, '?')
                team = getattr(unit, 'team', '?')
                color = curses.color_pair(self.COLOR_A) if team == 'A' else curses.color_pair(self.COLOR_B)
                try: self.stdscr.addch(uy + 1, ux + 1, char, color | curses.A_BOLD)
                except: pass

        # UI Stats
        mode_cam = "AUTO" if self.auto_follow else "MANUEL"
        stats = f"Time: {self.game.time:.1f}s | Units: {len(self.game.alive_units())} | Cam: {mode_cam}"
        self.stdscr.addstr(h - 3, 2, stats, curses.color_pair(self.COLOR_UI))
        self.stdscr.addstr(h - 2, 2, "Controls: A(Auto) ZQSD(Manuel) P(Pause) TAB(Snapshot) ESC(Quit)", curses.color_pair(self.COLOR_UI))
        
        if self.message:
            self.stdscr.addstr(h - 4, 2, f"*** {self.message} ***", curses.color_pair(self.COLOR_UI) | curses.A_BLINK)

        self.stdscr.refresh()

    def _draw_border(self, y, x, w, h):
        try:
            self.stdscr.hline(y, x, '-', w)
            self.stdscr.hline(y + h - 1, x, '-', w)
            self.stdscr.vline(y, x, '|', h)
            self.stdscr.vline(y, x + w - 1, '|', h)
            self.stdscr.addch(y, x, '+')
            self.stdscr.addch(y, x + w - 1, '+')
            self.stdscr.addch(y + h - 1, x, '+')
            self.stdscr.addch(y + h - 1, x + w - 1, '+')
        except: pass

    def _draw_game_over(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        msg = f"GAME OVER - Winner: {self.game.get_winner()}"
        self.stdscr.addstr(h//2, w//2 - len(msg)//2, msg, curses.A_BOLD)
        self.stdscr.addstr(h//2 + 1, w//2 - 10, "Press any key to quit")
        self.stdscr.nodelay(False)
        self.stdscr.getch()

    def generate_html_snapshot(self):
        filename = "snapshot_terminal.html"
        html = "<html><body><h1>Snapshot</h1><table border='1'><tr><th>ID</th><th>Type</th><th>Team</th><th>HP</th><th>Pos</th></tr>"
        for u in self.game.alive_units():
            color = "blue" if getattr(u, 'team', '?') == 'A' else "red"
            html += f"<tr style='color:{color}'><td>{id(u)}</td><td>{type(u).__name__}</td><td>{getattr(u, 'team', '?')}</td><td>{getattr(u, 'hp', 0):.1f}</td><td>({u.x:.1f}, {u.y:.1f})</td></tr>"
        html += "</table></body></html>"
        with open(filename, "w") as f: f.write(html)
        try: webbrowser.open(filename)
        except: pass