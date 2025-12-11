from views.terminal_view import TerminalView

from scenarios import scenario_small_terminal

if __name__ == "__main__":
    # 1. Créer le jeu
    game = scenario_small_terminal()
    
    # 2. Créer la vue
    view = TerminalView(game)
    
    # 3. Lancer !
    view.start()