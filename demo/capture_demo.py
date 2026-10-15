#!/usr/bin/env python3
"""
capture_demo.py - Génère la démo de MedievAIl Battle (captures PNG + vidéo MP4 + aperçu GIF).

Le vrai jeu est exécuté (menu fenêtré -> configuration -> bataille) avec son code
inchangé. Seuls l'entrée (souris / clavier) et l'horloge sont pilotées par un
scénario scripté, et l'affichage utilise le pilote SDL « dummy » (aucune fenêtre
n'est ouverte). Chaque image réellement dessinée par le jeu est enregistrée,
à 30 images/s en temps virtuel : la vidéo est donc fluide quelle que soit la
puissance de la machine.

Usage (depuis la racine du dépôt) :
    python demo/capture_demo.py

Dépendances : pygame et ffmpeg (dans le PATH).
"""
import os
import subprocess
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

import pygame  # noqa: E402

FPS = 30
OUT_DIR = os.path.join(ROOT, "demo")
SHOT_DIR = os.path.join(OUT_DIR, "screenshots")
VIDEO = os.path.join(OUT_DIR, "demo.mp4")
GIF = os.path.join(OUT_DIR, "demo_apercu.gif")


class StopDemo(Exception):
    """Levée à la fin du scénario pour sortir de la boucle du jeu."""


class Driver:
    """Remplace horloge, souris et clavier de pygame et enregistre chaque image."""

    def __init__(self):
        self.frame = 0
        self.mouse = (512, 384)
        self.buttons = [False, False, False]
        self.pressed = set()
        self.game = None
        self.gui = None
        self._last_rel = self.mouse
        self._ffmpeg = None
        self._wait = 0
        self._scenario = None

    # ---------- installation des substituts ----------
    def install(self):
        drv = self

        class FakeClock:
            def tick(self, fps=0):
                drv._on_frame()
                return int(1000 / FPS)

            tick_busy_loop = tick

            def get_fps(self):
                return float(FPS)

            def get_time(self):
                return int(1000 / FPS)

        class Keys:
            def __getitem__(self, key):
                return key in drv.pressed

        pygame.time.Clock = FakeClock
        pygame.time.get_ticks = lambda: int(drv.frame * 1000 / FPS)
        pygame.mouse.get_pos = lambda: drv.mouse
        pygame.mouse.get_pressed = lambda *a, **k: tuple(drv.buttons)
        pygame.mouse.get_rel = drv._get_rel
        pygame.key.get_pressed = lambda: Keys()

        # Mémorise la partie en cours pour que le scénario sache quand elle se termine.
        import model.game as model_game
        original_step = model_game.Game.step

        def step(game, *args, **kwargs):
            drv.game = game
            return original_step(game, *args, **kwargs)

        model_game.Game.step = step

        # Mémorise aussi la vue pour que la caméra puisse suivre l'action.
        import view.views as views
        original_draw = views.GUI.draw

        def draw(gui, screen):
            drv.gui = gui
            return original_draw(gui, screen)

        views.GUI.draw = draw

    def _get_rel(self):
        dx = self.mouse[0] - self._last_rel[0]
        dy = self.mouse[1] - self._last_rel[1]
        self._last_rel = self.mouse
        return dx, dy

    # ---------- enregistrement ----------
    def _on_frame(self):
        surf = pygame.display.get_surface()
        if self._ffmpeg is None:
            w, h = surf.get_size()
            self._ffmpeg = subprocess.Popen(
                ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                 "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-",
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "25", "-preset", "medium",
                 "-movflags", "+faststart", VIDEO],
                stdin=subprocess.PIPE)
        self._ffmpeg.stdin.write(pygame.image.tostring(surf, "RGB"))
        self.frame += 1

        if self._wait > 0:
            self._wait -= 1
            return
        try:
            self._wait = max(next(self._scenario) - 1, 0)
        except StopIteration:
            raise StopDemo()

    def finish(self):
        if self._ffmpeg is not None:
            self._ffmpeg.stdin.close()
            self._ffmpeg.wait()

    # ---------- actions du scénario (à utiliser avec « yield from ») ----------
    def _post(self, type_, **attrs):
        pygame.event.post(pygame.event.Event(type_, **attrs))

    def move(self, pos):
        rel = (pos[0] - self.mouse[0], pos[1] - self.mouse[1])
        self.mouse = (int(pos[0]), int(pos[1]))
        self._post(pygame.MOUSEMOTION, pos=self.mouse, rel=rel, buttons=tuple(self.buttons))

    def glide(self, pos, frames=18):
        x0, y0 = self.mouse
        for i in range(1, frames + 1):
            t = i / frames
            t = t * t * (3 - 2 * t)
            self.move((x0 + (pos[0] - x0) * t, y0 + (pos[1] - y0) * t))
            yield 1

    def click(self, pos=None, frames=18):
        if pos is not None:
            yield from self.glide(pos, frames)
            yield 4
        self.buttons[0] = True
        self._post(pygame.MOUSEBUTTONDOWN, pos=self.mouse, button=1)
        yield 3
        self.buttons[0] = False
        self._post(pygame.MOUSEBUTTONUP, pos=self.mouse, button=1)
        yield 1

    def drag(self, start, end, frames=40):
        yield from self.glide(start, 12)
        self.buttons[0] = True
        self._post(pygame.MOUSEBUTTONDOWN, pos=self.mouse, button=1)
        yield 2
        yield from self.glide(end, frames)
        self.buttons[0] = False
        self._post(pygame.MOUSEBUTTONUP, pos=self.mouse, button=1)
        yield 1

    def pan_to_action(self, frames=40):
        """Fait glisser la caméra (au moyen de vrais glisser-déposer) vers le centre des unités vivantes."""
        alive = self.game.alive_units()
        if not alive or self.gui is None:
            return
        gui = self.gui
        ix, iy = gui.cart_to_iso(sum(u.x for u in alive) / len(alive), sum(u.y for u in alive) / len(alive))
        dx = gui.screen_w / 2 - (ix + gui.camera_x)
        dy = gui.screen_h / 2 - (iy + gui.camera_y)
        parts = max(1, int(max(abs(dx), abs(dy)) // 300) + 1)
        for _ in range(parts):
            sx, sy = dx / parts, dy / parts
            start = (gui.screen_w / 2 - sx / 2, 330 - sy / 2)
            yield from self.drag(start, (start[0] + sx, start[1] + sy), max(frames // parts, 8))

    def wheel(self, notches, every=4):
        for _ in range(abs(notches)):
            self._post(pygame.MOUSEWHEEL, x=0, y=1 if notches > 0 else -1, flipped=False, which=0)
            yield every

    def key(self, key, hold=1):
        self.pressed.add(key)
        self._post(pygame.KEYDOWN, key=key, mod=0, unicode="", scancode=0)
        yield hold
        self.pressed.discard(key)
        self._post(pygame.KEYUP, key=key, mod=0)
        yield 1

    def shot(self, name):
        os.makedirs(SHOT_DIR, exist_ok=True)
        pygame.image.save(pygame.display.get_surface(), os.path.join(SHOT_DIR, name + ".png"))
        print(f"  capture : {name}.png")


# ----------------------------------------------------------------------------------
# Scénario : menu principal -> configuration -> bataille jusqu'à la victoire
# ----------------------------------------------------------------------------------
def scenario(d, menu):
    # Menu principal
    yield 40
    d.shot("01_menu_principal")
    yield from d.click(menu.btn_play.rect.center)
    yield 20
    d.shot("02_configuration_bataille")

    # Choix des IA (équipe A : General STRATEGUS, équipe B : Major DAFT)
    yield from d.click(menu.setup_ai_a.rect.center)
    yield 10
    d.shot("03_choix_de_l_ia")
    yield from d.click(menu.setup_ai_a.option_rects[2].center)
    yield 8
    yield from d.click(menu.setup_ai_b.rect.center)
    yield 8
    yield from d.click(menu.setup_ai_b.option_rects[1].center)
    yield 8

    # Composition : Grande Bataille, terrain : Colline Centrale
    yield from d.click(menu.setup_composition.rect.center)
    yield 8
    yield from d.click(menu.setup_composition.option_rects[1].center)
    yield 8
    yield from d.click(menu.setup_terrain.rect.center)
    yield 8
    yield from d.click(menu.setup_terrain.option_rects[1].center)
    yield 10
    d.shot("04_configuration_complete")

    # Lancement de la bataille
    yield from d.click(menu.btn_start.rect.center)
    yield 20
    d.shot("05_bataille_debut")

    # Vue d'ensemble : on dézoome, puis la caméra suit l'action pendant toute la bataille
    t0 = d.frame
    d.move((512, 384))
    yield from d.wheel(-4)
    yield 10
    d.shot("06_vue_d_ensemble")

    done = set()

    def once(name, at):
        """Vrai une seule fois, quand `at` images se sont écoulées depuis le début de la bataille."""
        if name not in done and d.frame - t0 >= at:
            done.add(name)
            return True
        return False

    while d.game is None or not d.game.is_finished():
        yield from d.pan_to_action(40)
        yield 20
        if once("melee", 240):
            d.shot("07_melee")
        if once("zoom", 330):
            d.move((512, 384))
            yield from d.wheel(3)
            yield 40
            d.shot("08_zoom_melee")
        if once("minimap", 600):
            yield from d.key(pygame.K_m)
            yield 45
            yield from d.key(pygame.K_m)
        if once("en_cours", 760):
            d.shot("09_bataille_en_cours")
        if d.frame - t0 > 90 * FPS:
            break

    # Victoire : la caméra se centre sur les survivants
    yield 10
    yield from d.pan_to_action(40)
    yield 20
    d.shot("10_victoire")
    yield 90

    # Retour au menu principal
    yield from d.key(pygame.K_ESCAPE)
    yield 30
    d.shot("11_retour_menu")
    yield 20


def make_preview():
    """Génère un GIF léger (accéléré x3, lisible dans le README) à partir de la vidéo."""
    palette = os.path.join(OUT_DIR, "_palette.png")
    base = "setpts=PTS/3,fps=8,scale=420:-1:flags=lanczos"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VIDEO,
                    "-vf", f"{base},palettegen=max_colors=64:stats_mode=diff", palette], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VIDEO, "-i", palette,
                    "-lavfi", f"{base}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
                    GIF], check=True)
    os.remove(palette)


def main():
    os.makedirs(SHOT_DIR, exist_ok=True)
    d = Driver()
    d.install()

    from view.menu import MainMenu
    menu = MainMenu(windowed=True)
    d._scenario = scenario(d, menu)

    print("Enregistrement de la démo...")
    try:
        menu.run()
    except StopDemo:
        pass
    finally:
        d.finish()
        pygame.quit()

    print(f"{d.frame} images enregistrées ({d.frame / FPS:.1f} s)")
    make_preview()
    print("Terminé :", VIDEO)


if __name__ == "__main__":
    main()
