import pygame
import sys

# --- IMPORTS ---
# On importe la fonction de création ET les infos des équipes (couleurs, noms)
from main import scenario_simple_vs_braindead, TEAM_INFO
from views.views import GUI

def main():
    # 1. SETUP
    print("Initialisation de la bataille...")
    game = scenario_simple_vs_braindead()

    pygame.init()
    # On définit les constantes de taille ici pour les réutiliser dans le centrage du texte
    SCREEN_W = 1024
    SCREEN_H = 768
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    
    pygame.display.set_caption("Simulation : Captain BRAINDEAD vs Major DAFT")
    clock = pygame.time.Clock()

    view = GUI(game)
    
    # Options de simulation
    auto_play = False
    game_over_processed = False # Pour ne pas spammer le terminal

    print("\n--- COMMANDES ---")
    print("[ENTRÉE] : Lancer / Pause (Auto-play)")
    print("[ESPACE] : Avancer pas à pas")
    print("-----------------\n")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # Toggle Auto-play
                if event.key == pygame.K_RETURN:
                    if not game.is_finished():
                        auto_play = not auto_play
                        state = "ON" if auto_play else "OFF"
                        print(f"Lecture automatique : {state}")
                
                # Pas à pas (seulement si pas fini)
                if event.key == pygame.K_SPACE:
                    if not game.is_finished():
                        game.step(dt=0.1)
                        print(f"Tour joué. Temps: {game.time:.1f}")

        # --- LOGIQUE DE JEU ---
        if not game.is_finished():
            if auto_play:
                game.step(dt=0.1) # Vitesse de simulation
        
        else:
            # --- C'EST FINI (Côté Terminal) ---
            if not game_over_processed:
                print("\n" + "="*30)
                print("   LA BATAILLE EST TERMINÉE !")
                print("="*30)
                
                winner = game.get_winner()
                if winner is None:
                    print("🏁 RÉSULTAT : MATCH NUL")
                else:
                    info = TEAM_INFO.get(winner, {})
                    nom_equipe = info.get("name", f"Équipe {winner}")
                    ia_name = info.get("ia", "?")
                    print(f"🏆 VAINQUEUR : {nom_equipe} ({winner})")
                    print(f"🧠 IA : {ia_name}")
                
                print("="*30 + "\n")
                auto_play = False # On arrête l'auto-play
                game_over_processed = True # On note que c'est fait

        # --- AFFICHAGE ---
        view.handle_input()
        view.draw(screen)
        
        # --- C'EST FINI (Côté Graphique - NOUVEAU CODE) ---
        if game.is_finished():
            winner = game.get_winner()
            font = pygame.font.SysFont("Arial", 40, bold=True)
            
            # Préparation des lignes de texte à afficher
            lines_to_display = []
            
            if winner is None:
                lines_to_display.append(("MATCH NUL", (255, 255, 255))) # Blanc
            else:
                # On récupère les infos jolies
                info = TEAM_INFO.get(winner, {})
                nom_equipe = info.get("name", f"Équipe {winner}")
                ia_name = info.get("ia", "?")
                
                # Ligne 1 : "VICTOIRE : Nom de l'équipe"
                lines_to_display.append((f"VICTOIRE : {nom_equipe}", (255, 215, 0))) # Or
                # Ligne 2 : "Général : Nom de l'IA"
                lines_to_display.append((f"Général : {ia_name}", (200, 200, 200))) # Gris clair

            # Boucle pour afficher chaque ligne centrée
            center_x = SCREEN_W // 2
            start_y = 100 # Hauteur de départ (haut de l'écran)
            
            for i, (text_str, color) in enumerate(lines_to_display):
                text_surf = font.render(text_str, True, color)
                text_rect = text_surf.get_rect(center=(center_x, start_y + i * 50)) # 50px d'écart
                
                # Fond noir semi-transparent derrière pour la lisibilité
                bg_rect = text_rect.inflate(20, 10)
                s = pygame.Surface((bg_rect.width, bg_rect.height))
                s.set_alpha(180) # Transparence (0-255)
                s.fill((0, 0, 0))
                screen.blit(s, bg_rect)
                
                # Le texte par dessus
                screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()