import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tournoi des Super-Héros")

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# Police
FONT = pygame.font.SysFont("Comic Sans MS", 30, bold=True)

# Paramètres des joueurs
PLAYER_SIZE = 60
VELOCITY = 5

# Définition des héros avec leurs statistiques
heroes = {
    "Superman": {"intelligence": 94, "strength": 100, "speed": 90, "durability": 100, "power": 100, "combat": 85},
    "Batman": {"intelligence": 100, "strength": 40, "speed": 29, "durability": 55, "power": 63, "combat": 90},
}

# Attaques et défenses
attacks = {
    "Coup de poing": ("strength", 1.5),
    "Rayon laser": ("power", 1.7),
}

defenses = {
    "Esquive": 20,
    "Blocage": 15,
}

# Sélection aléatoire des héros
player1, player2 = random.sample(list(heroes.keys()), 2)
pv = {player1: 1000, player2: 1000}

# Détermination du premier joueur
turn = random.choice([player1, player2])

# Positions initiales
player1_x, player1_y = 100, HEIGHT // 2
player2_x, player2_y = WIDTH - 150, HEIGHT // 2

# Boucle principale
running = True
while running:
    pygame.time.delay(50)
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, GOLD, (0, 0, WIDTH, 50))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player1_x -= VELOCITY
    if keys[pygame.K_RIGHT]:
        player1_x += VELOCITY
    if keys[pygame.K_UP]:
        player1_y -= VELOCITY
    if keys[pygame.K_DOWN]:
        player1_y += VELOCITY
    
    if keys[pygame.K_a]:
        player2_x -= VELOCITY
    if keys[pygame.K_d]:
        player2_x += VELOCITY
    if keys[pygame.K_w]:
        player2_y -= VELOCITY
    if keys[pygame.K_s]:
        player2_y += VELOCITY
    
    
    if random.random() < 0.02:  
        attacker, defender = turn, player1 if turn == player2 else player2
        attack = random.choice(list(attacks.keys()))
        defense = random.choice(list(defenses.keys()))
        
        stat, modifier = attacks[attack]
        damage = max(heroes[attacker][stat] * modifier - defenses[defense], 0)
        pv[defender] -= damage
        
        print(f"{attacker} attaque {defender} avec {attack} (-{damage} PV), {defender} défend avec {defense}")
        print(f"PV -> {player1}: {pv[player1]} | {player2}: {pv[player2]}")
        
        if pv[defender] <= 0:
            print(f"{attacker} gagne le combat!")
            running = False
        
        turn = defender  # Changement de rôle
    
    # Dessin des joueurs
    pygame.draw.rect(WIN, RED, (player1_x, player1_y, PLAYER_SIZE, PLAYER_SIZE), border_radius=10)
    pygame.draw.rect(WIN, BLUE, (player2_x, player2_y, PLAYER_SIZE, PLAYER_SIZE), border_radius=10)
    
    # Affichage des scores stylisés
    score_text = FONT.render(f"{player1}: {pv[player1]} PV  |  {player2}: {pv[player2]} PV", True, BLACK)
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
    
    pygame.display.update()

pygame.quit()
