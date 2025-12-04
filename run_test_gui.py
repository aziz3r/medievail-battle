import pygame
import sys
import time

# --- IMPORTS DU COLLÈGUE ---
from game import Game
from map import BattleMap
from ai import CaptainBraindead, MajorDaft
from knight import Knight
from pikeman import Pikeman
from crossbowman import Crossbowman

# --- IMPORT DE TA VUE ---
from views.views import GUI

# --- FONCTION DE SCÉNARIO (Copiée depuis son main.py) ---
def build_battle_scenario() -> Game:
    rows, cols = 20, 20
    battle_map = BattleMap(rows=rows, cols=cols)

    controllers = {
        "A": MajorDaft("A"),       # IA qui avance
        "B": CaptainBraindead("B"), # IA statique
    }

    game = Game(battle_map, controllers)

    # --- Placement des unités (Copie simplifiée) ---
    # Équipe A (Gauche)
    for r in range(6, 11):
        game.add_unit(Pikeman(), "A", row=r, col=3)
    for r in range(7, 10):
        game.add_unit(Knight(), "A", row=r, col=2)

    # Équipe B (Droite)
    for r in range(6, 12):
        game.add_unit(Pikeman(), "B", row=r, col=cols - 4)
    for r in range(7, 11, 2):
        game.add_unit(Knight(), "B", row=r, col=cols - 5)

    return game

# --- BOUCLE PRINCIPALE AVEC PYGAME ---
def main():
    print("Initialisation du scénario...")
    game = build_battle_scenario()

    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Age of Python - Simulation Visuelle")
    clock = pygame.time.Clock()

    # On branche ta vue
    view = GUI(game)
    
    print("Moteur Graphique lancé !")
    print("-> Appuie sur ESPACE pour faire avancer le temps (Tour par tour)")
    print("-> Reste appuyé sur ENTREE pour avance rapide")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- CONTRÔLE MANUEL (ESPACE) ---
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not game.is_finished():
                    game.step(dt=1.0) # On fait avancer la simulation de 1 seconde
                    print(f"Tour joué. Temps: {game.time:.1f}")
                else:
                    print("La bataille est finie !")

        # --- CONTRÔLE CONTINU (ENTREE) ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
             if not game.is_finished():
                game.step(dt=0.5) # Plus rapide

        # Mises à jour vue
        view.handle_input() # Caméra
        view.draw(screen)   # Dessin
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()