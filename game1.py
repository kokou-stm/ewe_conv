import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tournoi des Super-Héros")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Police
font = pygame.font.Font(None, 36)

# Superhéros et leurs statistiques
superheroes = {
    "Superman": {"intelligence": 85, "strength": 95, "speed": 90, "durability": 100, "power": 100, "combat": 80},
    "Batman": {"intelligence": 95, "strength": 40, "speed": 75, "durability": 60, "power": 65, "combat": 90},
}

# Attaques et défenses
attacks = {
    "Rayon laser": {"stat": "power", "modifier": 1.7},
    "Coup de poing titanesque": {"stat": "strength", "modifier": 1.5},
    "Combo martial": {"stat": "combat", "modifier": 1.3},
}
defenses = {
    "Blocage indestructible": {"reduction": 15},
    "Esquive ultra-rapide": {"reduction": 20},
}

# Fonction pour calculer les dégâts
def calculate_damage(attacker, defender, attack, defense):
    attack_stat = attacker[attacks[attack]["stat"]]
    modifier = attacks[attack]["modifier"]
    reduction = defenses[defense]["reduction"]
    return max(0, (attack_stat * modifier) - reduction)

# Texte affiché
def draw_text(text, x, y):
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (x, y))

# Simulation du combat
def simulate_combat(hero1, hero2):
    hero1_hp, hero2_hp = 1000, 1000
    turn = 1
    running = True

    while running:
        screen.fill(WHITE)
        
        # Affichage des PV
        draw_text(f"{hero1}: {hero1_hp} PV", 50, 50)
        draw_text(f"{hero2}: {hero2_hp} PV", 500, 50)

        # Déterminer qui attaque et qui défend
        if turn % 2 != 0:
            attacker, defender = hero1, hero2
            attacker_hp, defender_hp = hero1_hp, hero2_hp
        else:
            attacker, defender = hero2, hero1
            attacker_hp, defender_hp = hero2_hp, hero1_hp

        # Choisir une attaque et une défense
        attack = random.choice(list(attacks.keys()))
        defense = random.choice(list(defenses.keys()))

        # Calcul des dégâts
        damage = calculate_damage(superheroes[attacker], superheroes[defender], attack, defense)
        defender_hp -= damage

        # Affichage des actions
        draw_text(f"{attacker} utilise {attack}!", 50, 150)
        draw_text(f"{defender} utilise {defense}!", 50, 200)
        draw_text(f"Dégâts infligés: {damage}", 50, 250)

        # Mettre à jour les PV
        if turn % 2 != 0:
            hero2_hp = defender_hp
        else:
            hero1_hp = defender_hp

        # Vérifier si un héros est vaincu
        if hero1_hp <= 0 or hero2_hp <= 0:
            winner = hero1 if hero2_hp <= 0 else hero2
            draw_text(f"{winner} gagne!", 50, 300)
            running = False

        # Mettre à jour l'affichage
        pygame.display.flip()
        pygame.time.wait(2000)  # Pause avant le prochain tour
        turn += 1

        # Fermer la fenêtre à la fin
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# Choisir des héros aléatoires
hero1, hero2 = random.sample(list(superheroes.keys()), 2)
simulate_combat(hero1, hero2)

pygame.quit()
