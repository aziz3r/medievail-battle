import pygame

# --- CONSTANTES ---
TILE_WIDTH = 64
TILE_HEIGHT = 32
SCREEN_W = 1024
SCREEN_H = 768

# Couleurs des équipes (Cercles au sol)
COLOR_TEAM_A = (0, 80, 255)   # Bleu (Nord/Gauche)
COLOR_TEAM_B = (220, 20, 60)  # Rouge (Sud/Droite)

class GUI:
    def __init__(self, game_instance):
        self.game = game_instance
        # Protection : on récupère la map même si le nom change
        self.map = getattr(game_instance, 'map', None)
        
        self.camera_x = SCREEN_W // 2
        self.camera_y = 50
        
        self.assets = {}
        self._load_assets()

    def _load_assets(self):
        """ Charge les images (Sol + Unités) """
        
        # --- 1. LE SOL (GRASS) ---
        try:
            # On charge l'herbe
            img = pygame.image.load("assets/grass.png").convert()
            # On enlève la couleur du coin (transparence auto)
            img.set_colorkey(img.get_at((0,0)))
            self.assets['grass'] = pygame.transform.scale(img, (TILE_WIDTH, TILE_HEIGHT))
        except:
            # Si pas d'image, carré vert
            print("⚠️ 'assets/grass.png' introuvable.")
            s = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            s.fill((34, 139, 34))
            self.assets['grass'] = s

        # --- 2.CHEVALIER (KNIGHT) ---
        try:
            # On charge l'image nettoyée
            img_k = pygame.image.load("assets/knight.png").convert_alpha()
            
            # ceci va rendre le blanc transparent automatiquement.
            coin = img_k.get_at((0,0))
            if coin.a == 255: # Si le coin n'est pas déjà transparent
                img_k.set_colorkey(coin)

            # On redimensionne (50x50 c'est bien pour un chevalier)
            self.assets['knight'] = pygame.transform.scale(img_k, (50, 50))
            print("✅ Chevalier (knight.png) chargé !")
            
        except Exception as e:
            print(f"⚠️ Erreur chargement Knight: {e}")
            # Fallback : Rond rouge avec un 'K'
            s = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(s, (200, 0, 0), (15, 15), 15)
            self.assets['knight'] = s

        # --- 3. AUTRES UNITÉS (Pikeman, Crossbowman) ---
        for name, color in [("pikeman", (0, 150, 0)), ("crossbowman", (0, 100, 200))]:
            try:
                img = pygame.image.load(f"assets/{name}.png").convert_alpha()
                self.assets[name] = pygame.transform.scale(img, (40, 40))
            except:
                s = pygame.Surface((30, 30), pygame.SRCALPHA)
                pygame.draw.circle(s, color, (15, 15), 12)
                self.assets[name] = s

    def cart_to_iso(self, row, col):
        """ Conversion Grille -> Pixels """
        iso_x = (col - row) * (TILE_WIDTH // 2)
        iso_y = (row + col) * (TILE_HEIGHT // 2)
        return iso_x, iso_y

    def handle_input(self):
        keys = pygame.key.get_pressed()
        s = 15
        if keys[pygame.K_LEFT]: self.camera_x += s
        if keys[pygame.K_RIGHT]: self.camera_x -= s
        if keys[pygame.K_UP]: self.camera_y += s
        if keys[pygame.K_DOWN]: self.camera_y -= s

    def draw(self, screen):
        screen.fill((20, 20, 20)) # Fond gris foncé

        # --- A. DESSIN DE LA MAP ---
        if self.map:
            rows = getattr(self.map, 'rows', 20)
            cols = getattr(self.map, 'cols', 20)
            
            for row in range(rows):
                for col in range(cols):
                    x, y = self.cart_to_iso(row, col)
                    final_x = x + self.camera_x
                    final_y = y + self.camera_y
                    
                    # On dessine seulement si c'est dans l'écran
                    if -64 < final_x < SCREEN_W and -32 < final_y < SCREEN_H:
                        screen.blit(self.assets['grass'], (final_x, final_y))

        # --- B. DESSIN DES UNITÉS ---
        # On récupère la liste des unités vivantes du jeu
        units = []
        if hasattr(self.game, 'alive_units'):
            units = self.game.alive_units()

        for unit in units:
            # 1. Calcul position
            u_x = getattr(unit, 'x', 0)
            u_y = getattr(unit, 'y', 0)
            
            x_iso, y_iso = self.cart_to_iso(u_x, u_y)
            screen_x = x_iso + self.camera_x + 8
            screen_y = y_iso + self.camera_y - 20 # On remonte l'unité pour l'effet 3D

            # 2. Cercle d'équipe (au sol)
            team = getattr(unit, 'team', '?')
            color = COLOR_TEAM_A if team == "A" else COLOR_TEAM_B
            pygame.draw.ellipse(screen, color, (screen_x + 5, screen_y + 40, 30, 8))

            # 3. L'Image de l'unité
            u_type = type(unit).__name__.lower()
            
            # On cherche l'image correspondante, sinon on met Knight par défaut
            img = self.assets.get(u_type, self.assets.get('knight'))
            
            if img:
                
                # Équipe A (Gauche) veut regarder à DROITE -> ON RETOURNE (Miroir)
                if team == "A":
                    img = pygame.transform.flip(img, True, False)
                
                # Équipe B (Droite) veut regarder à GAUCHE -> ON LAISSE NORMAL
                screen.blit(img, (screen_x, screen_y))
            
            # 4. Barre de vie (au-dessus)
            hp = getattr(unit, 'hp', 0)
            if hp > 0:
                pygame.draw.rect(screen, (0,0,0), (screen_x, screen_y - 5, 40, 4))
                w = min(40, max(0, int(hp / 2.5))) 
                pygame.draw.rect(screen, (0, 255, 0), (screen_x, screen_y - 5, w, 4))