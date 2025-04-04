import tkinter as tk
from tkinter import ttk, messagebox, font
import random
from PIL import Image, ImageTk
import os
import json

class SuperHero:
    def __init__(self, name, image_path, stats):
        self.name = name
        self.image_path = image_path
        self.stats = stats  # Dictionnaire avec Force, Intelligence, Vitesse, etc.
        self.current_hp = 1000
        self.max_hp = 1000
        self.consecutive_attacks = {}  # Pour limiter les attaques consécutives
        
    def reset(self):
        self.current_hp = self.max_hp
        self.consecutive_attacks = {}
        
    def __str__(self):
        return self.name

class SuperHeroesTournament:
    def __init__(self, root):
        self.root = root
        self.root.title("Tournoi des Super-Héros")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        
        # Police personnalisée
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=10, weight="bold")
        
        # Couleurs
        self.bg_color = "#1E1E2E"
        self.accent_color = "#F85C50"
        self.text_color = "#FFFFFF"
        self.button_color = "#3D3D65"
        self.button_hover = "#535383"
        
        self.root.configure(bg=self.bg_color)
        
        # Liste des super-héros
        self.heroes = self.load_heroes()
        
        # Variables du jeu
        self.player1_hero = None
        self.player2_hero = None
        self.current_attacker = None
        self.current_defender = None
        self.game_started = False
        self.game_over = False
        self.turn_count = 0
        
        # Attaques et défenses disponibles
        self.attacks = {
            "Intelligence": [
                {"name": "Stratégie imparable", "modifier": 1.1},
                {"name": "Feinte déstabilisante", "modifier": 1.05}
            ],
            "Force": [
                {"name": "Coup de poing titanesque", "modifier": 1.5},
                {"name": "Coup de pied écrasant", "modifier": 1.4}
            ],
            "Vitesse": [
                {"name": "Frappe éclair", "modifier": 1.3},
                {"name": "Rafale de coups", "modifier": 1.2}
            ],
            "Durabilité": [
                {"name": "Impact écrasant", "modifier": 1.4},
                {"name": "Résistance offensive", "modifier": 1.3}
            ],
            "Puissance": [
                {"name": "Rayon laser", "modifier": 1.7},
                {"name": "Explosion télékinétique", "modifier": 1.6}
            ],
            "Combat": [
                {"name": "Combo martial", "modifier": 1.3},
                {"name": "Projection au sol", "modifier": 1.2}
            ]
        }
        
        self.defenses = {
            "Intelligence": [
                {"name": "Lecture de l'attaque", "reduction": 10},
                {"name": "Feinte défensive", "reduction": 8}
            ],
            "Force": [
                {"name": "Blocage indestructible", "reduction": 15},
                {"name": "Parade musclée", "reduction": 12}
            ],
            "Vitesse": [
                {"name": "Esquive ultra-rapide", "reduction": 20},
                {"name": "Déplacement instantané", "reduction": 18}
            ],
            "Durabilité": [
                {"name": "Endurance renforcée", "reduction": 15},
                {"name": "Absorption des chocs", "reduction": 12}
            ],
            "Puissance": [
                {"name": "Bouclier d'énergie", "reduction": 25},
                {"name": "Absorption d'énergie", "reduction": 22}
            ],
            "Combat": [
                {"name": "Riposte défensive", "reduction": 14},
                {"name": "Contre-attaque rapide", "reduction": 12}
            ]
        }
        
        # Interface principale
        self.setup_main_screen()
    
    def load_heroes(self):
        # Liste des super-héros avec leurs statistiques
        heroes = [
            SuperHero("Superman", "superman.png", {
                "Force": 95, 
                "Intelligence": 70, 
                "Vitesse": 90, 
                "Durabilité": 95, 
                "Puissance": 85, 
                "Combat": 75
            }),
            SuperHero("Batman", "batman.png", {
                "Force": 70, 
                "Intelligence": 100, 
                "Vitesse": 65, 
                "Durabilité": 60, 
                "Puissance": 60, 
                "Combat": 90
            }),
            SuperHero("Wonder Woman", "wonderwoman.png", {
                "Force": 90, 
                "Intelligence": 75, 
                "Vitesse": 85, 
                "Durabilité": 80, 
                "Puissance": 70, 
                "Combat": 95
            }),
            SuperHero("Flash", "flash.png", {
                "Force": 65, 
                "Intelligence": 80, 
                "Vitesse": 100, 
                "Durabilité": 60, 
                "Puissance": 70, 
                "Combat": 75
            }),
            SuperHero("Green Lantern", "greenlantern.png", {
                "Force": 75, 
                "Intelligence": 80, 
                "Vitesse": 70, 
                "Durabilité": 70, 
                "Puissance": 95, 
                "Combat": 80
            }),
            SuperHero("Aquaman", "aquaman.png", {
                "Force": 85, 
                "Intelligence": 75, 
                "Vitesse": 70, 
                "Durabilité": 80, 
                "Puissance": 70, 
                "Combat": 85
            }),
            SuperHero("Captain Marvel", "captainmarvel.png", {
                "Force": 90, 
                "Intelligence": 75, 
                "Vitesse": 85, 
                "Durabilité": 90, 
                "Puissance": 90, 
                "Combat": 80
            }),
            SuperHero("Iron Man", "ironman.png", {
                "Force": 70, 
                "Intelligence": 95, 
                "Vitesse": 70, 
                "Durabilité": 70, 
                "Puissance": 85, 
                "Combat": 75
            })
        ]
        return heroes
        
    def setup_main_screen(self):
        # Supprimer tous les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Image de fond (à remplacer par votre propre image)
        # self.bg_image = ImageTk.PhotoImage(Image.open("background.jpg").resize((1200, 800)))
        # bg_label = tk.Label(self.root, image=self.bg_image)
        # bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Titre du jeu
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=30)
        
        title_label = tk.Label(title_frame, text="TOURNOI DES SUPER-HÉROS", font=self.title_font, bg=self.bg_color, fg=self.accent_color)
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Duels stratégiques entre les plus grands héros", font=self.subtitle_font, bg=self.bg_color, fg=self.text_color)
        subtitle_label.pack(pady=10)
        
        # Bouton pour commencer le jeu
        start_button = tk.Button(self.root, text="COMMENCER LE TOURNOI", font=self.button_font, bg=self.accent_color, fg=self.text_color,
                               command=self.start_game, width=25, height=2, relief=tk.FLAT)
        start_button.pack(pady=20)
        
        # Règles du jeu
        rules_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        rules_frame.pack(fill=tk.BOTH, expand=True, padx=50)
        
        rules_label = tk.Label(rules_frame, text="RÈGLES DU JEU", font=self.subtitle_font, bg=self.bg_color, fg=self.accent_color)
        rules_label.pack(pady=10)
        
        rules_text = """
        Bienvenue dans le Tournoi des Super-Héros, un jeu de combat où les plus grands héros 
        s'affrontent dans des duels stratégiques.
        
        Déroulement du Combat:
        1. Le jeu affecte aléatoirement un super héros à chaque joueur.
        2. Chaque héros commence avec 1000 PV.
        3. Au premier tour, le jeu détermine quel joueur va débuter.
        4. À chaque tour :
           • Le joueur attaquant choisit une attaque.
           • Le joueur défenseur choisit une défense.
        5. Les dégâts sont calculés avec la formule: Dégâts = statistique utilisée × modificateur − réduction de défense
        6. Les PV sont mis à jour après chaque attaque.
        7. Le rôle attaque/défense alterne à chaque tour.
        8. Le combat continue jusqu'à ce qu'un héros atteigne 0 PV.
        
        Restrictions sur les Attaques:
        • Chaque attaque ne peut être utilisée que 2 fois d'affilée.
        • Après 2 utilisations consécutives, le joueur doit choisir une autre attaque.
        
        Serez-vous capable de dominer l'arène et devenir le plus puissant des super-héros ?
        """
        
        rules_text_label = tk.Label(rules_frame, text=rules_text, font=self.normal_font, bg=self.bg_color, fg=self.text_color, justify=tk.LEFT)
        rules_text_label.pack(pady=5, fill=tk.BOTH, expand=True)
        
    def start_game(self):
        # Sélection aléatoire des héros
        selected_heroes = random.sample(self.heroes, 2)
        self.player1_hero = selected_heroes[0]
        self.player2_hero = selected_heroes[1]
        
        # Réinitialisation des héros
        self.player1_hero.reset()
        self.player2_hero.reset()
        
        # Déterminer aléatoirement qui commence
        if random.choice([True, False]):
            self.current_attacker = self.player1_hero
            self.current_defender = self.player2_hero
        else:
            self.current_attacker = self.player2_hero
            self.current_defender = self.player1_hero
        
        self.game_started = True
        self.game_over = False
        self.turn_count = 1
        
        # Passer à l'écran de combat
        self.setup_battle_screen()

    def setup_battle_screen(self):
        # Supprimer tous les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Cadre principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Information du tour en cours
        turn_frame = tk.Frame(main_frame, bg=self.bg_color)
        turn_frame.pack(fill=tk.X, pady=10)
        
        turn_label = tk.Label(turn_frame, 
                               text=f"TOUR {self.turn_count} - {self.current_attacker.name} ATTAQUE, {self.current_defender.name} DÉFEND",
                               font=self.subtitle_font, bg=self.bg_color, fg=self.accent_color)
        turn_label.pack()
        
        # Zone de combat (affichage des héros et barres de vie)
        battle_frame = tk.Frame(main_frame, bg=self.bg_color)
        battle_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Affichage Héros 1
        hero1_frame = tk.Frame(battle_frame, bg=self.bg_color)
        hero1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        
        # Placeholder pour l'image du héros 1 (image à remplacer)
        try:
            hero1_img = ImageTk.PhotoImage(Image.open(self.player1_hero.image_path).resize((200, 300)))
            hero1_img_label = tk.Label(hero1_frame, image=hero1_img, bg=self.bg_color)
            hero1_img_label.image = hero1_img  # Garder une référence
        except:
            hero1_img_label = tk.Label(hero1_frame, text="[Image du héros]", height=10, width=20, bg=self.button_color, fg=self.text_color)
        hero1_img_label.pack(pady=10)
        
        hero1_name = tk.Label(hero1_frame, text=self.player1_hero.name, font=self.subtitle_font, bg=self.bg_color, fg=self.text_color)
        hero1_name.pack(pady=5)
        
        hero1_hp_frame = tk.Frame(hero1_frame, bg=self.bg_color)
        hero1_hp_frame.pack(fill=tk.X, pady=5)
        
        hero1_hp_label = tk.Label(hero1_hp_frame, text=f"PV: {self.player1_hero.current_hp}/{self.player1_hero.max_hp}", font=self.normal_font, bg=self.bg_color, fg=self.text_color)
        hero1_hp_label.pack(side=tk.LEFT)
        
        hero1_hp_bar = ttk.Progressbar(hero1_frame, orient="horizontal", length=200, mode="determinate", maximum=self.player1_hero.max_hp, value=self.player1_hero.current_hp)
        hero1_hp_bar.pack(fill=tk.X, pady=5)
        
        # Affichage statistiques héros 1
        hero1_stats_frame = tk.Frame(hero1_frame, bg=self.bg_color)
        hero1_stats_frame.pack(fill=tk.X, pady=10)
        
        for stat, value in self.player1_hero.stats.items():
            stat_frame = tk.Frame(hero1_stats_frame, bg=self.bg_color)
            stat_frame.pack(fill=tk.X, pady=2)
            
            stat_label = tk.Label(stat_frame, text=f"{stat}:", width=10, anchor="e", font=self.normal_font, bg=self.bg_color, fg=self.text_color)
            stat_label.pack(side=tk.LEFT)
            
            stat_value = tk.Label(stat_frame, text=str(value), width=3, font=self.normal_font, bg=self.bg_color, fg=self.accent_color)
            stat_value.pack(side=tk.LEFT)
            
            stat_bar = ttk.Progressbar(stat_frame, orient="horizontal", length=100, mode="determinate", maximum=100, value=value)
            stat_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            
        # VS Label
        vs_label = tk.Label(battle_frame, text="VS", font=self.title_font, bg=self.bg_color, fg=self.accent_color)
        vs_label.pack(side=tk.LEFT)
            
        # Affichage Héros 2
        hero2_frame = tk.Frame(battle_frame, bg=self.bg_color)
        hero2_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)
        
        # Placeholder pour l'image du héros 2
        try:
            hero2_img = ImageTk.PhotoImage(Image.open(self.player2_hero.image_path).resize((200, 300)))
            hero2_img_label = tk.Label(hero2_frame, image=hero2_img, bg=self.bg_color)
            hero2_img_label.image = hero2_img  # Garder une référence
        except:
            hero2_img_label = tk.Label(hero2_frame, text="[Image du héros]", height=10, width=20, bg=self.button_color, fg=self.text_color)
        hero2_img_label.pack(pady=10)
        
        hero2_name = tk.Label(hero2_frame, text=self.player2_hero.name, font=self.subtitle_font, bg=self.bg_color, fg=self.text_color)
        hero2_name.pack(pady=5)
        
        hero2_hp_frame = tk.Frame(hero2_frame, bg=self.bg_color)
        hero2_hp_frame.pack(fill=tk.X, pady=5)
        
        hero2_hp_label = tk.Label(hero2_hp_frame, text=f"PV: {self.player2_hero.current_hp}/{self.player2_hero.max_hp}", font=self.normal_font, bg=self.bg_color, fg=self.text_color)
        hero2_hp_label.pack(side=tk.LEFT)
        
        hero2_hp_bar = ttk.Progressbar(hero2_frame, orient="horizontal", length=200, mode="determinate", maximum=self.player2_hero.max_hp, value=self.player2_hero.current_hp)
        hero2_hp_bar.pack(fill=tk.X, pady=5)
        
        # Affichage statistiques héros 2
        hero2_stats_frame = tk.Frame(hero2_frame, bg=self.bg_color)
        hero2_stats_frame.pack(fill=tk.X, pady=10)
        
        for stat, value in self.player2_hero.stats.items():
            stat_frame = tk.Frame(hero2_stats_frame, bg=self.bg_color)
            stat_frame.pack(fill=tk.X, pady=2)
            
            stat_label = tk.Label(stat_frame, text=f"{stat}:", width=10, anchor="e", font=self.normal_font, bg=self.bg_color, fg=self.text_color)
            stat_label.pack(side=tk.LEFT)
            
            stat_value = tk.Label(stat_frame, text=str(value), width=3, font=self.normal_font, bg=self.bg_color, fg=self.accent_color)
            stat_value.pack(side=tk.LEFT)
            
            stat_bar = ttk.Progressbar(stat_frame, orient="horizontal", length=100, mode="determinate", maximum=100, value=value)
            stat_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Zone des actions
        action_frame = tk.Frame(main_frame, bg=self.bg_color, padx=20, pady=20)
        action_frame.pack(fill=tk.X, pady=10)
        
        # Cadre pour les attaques et défenses
        self.current_action_frame = tk.Frame(action_frame, bg=self.bg_color)
        self.current_action_frame.pack(fill=tk.BOTH, expand=True)
        
        # Afficher les options en fonction du joueur actuel
        if self.current_attacker == self.player1_hero:
            attack_label = tk.Label(self.current_action_frame, text=f"Joueur 1 ({self.player1_hero.name}) - Choisissez votre attaque:", font=self.subtitle_font, bg=self.bg_color, fg=self.text_color)
            attack_label.pack(pady=5)
            self.show_attack_options()
        else:
            attack_label = tk.Label(self.current_action_frame, text=f"Joueur 2 ({self.player2_hero.name}) - Choisissez votre attaque:", font=self.subtitle_font, bg=self.bg_color, fg=self.text_color)
            attack_label.pack(pady=5)
            self.show_attack_options()
    
    def show_attack_options(self):
        # Afficher toutes les attaques disponibles
        attack_options_frame = tk.Frame(self.current_action_frame, bg=self.bg_color)
        attack_options_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Créer un cadre pour chaque type de pouvoir
        row = 0
        col = 0
        
        for power_type, attacks in self.attacks.items():
            power_frame = tk.Frame(attack_options_frame, bg=self.bg_color, bd=2, relief=tk.GROOVE, padx=10, pady=10)
            power_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            power_label = tk.Label(power_frame, text=power_type, font=self.subtitle_font, bg=self.bg_color, fg=self.accent_color)
            power_label.pack(pady=5)
            
            # Afficher les attaques de ce type de pouvoir
            for attack in attacks:
                # Vérifier si l'attaque peut être utilisée (pas plus de 2 fois consécutives)
                attack_name = attack["name"]
                attack_count = self.current_attacker.consecutive_attacks.get(attack_name, 0)
                disabled = attack_count >= 2
                
                button_text = f"{attack_name} (x{attack_count}/2)" if attack_count > 0 else attack_name
                button_text += f" - Mod: x{attack['modifier']}"
                
                attack_btn = tk.Button(power_frame, text=button_text, 
                                     command=lambda a=attack, p=power_type: self.select_attack(a, p),
                                     font=self.button_font, bg=self.button_color if not disabled else "#666666", 
                                     fg=self.text_color, width=25, relief=tk.FLAT,
                                     state=tk.NORMAL if not disabled else tk.DISABLED)
                attack_btn.pack(pady=2, fill=tk.X)
            
            # Gestion de la grille
            col += 1
            if col > 2:  # 3 colonnes max
                col = 0
                row += 1
    
    def select_attack(self, attack, power_type):
        # Enregistrer l'attaque sélectionnée
        self.selected_attack = attack
        self.selected_attack_power = power_type
        
        # Mettre à jour le compteur d'attaques consécutives
        attack_name = attack["name"]
        for a_name in list(self.current_attacker.consecutive_attacks.keys()):
            if a_name != attack_name:
                self.current_attacker.consecutive_attacks[a_name] = 0
                
        current_count = self.current_attacker.consecutive_attacks.get(attack_name, 0)
        self.current_attacker.consecutive_attacks[attack_name] = current_count + 1
        
        # Effacer le cadre d'action actuel
        for widget in self.current_action_frame.winfo_children():
            widget.destroy()
            
        # Afficher le message de transition
        transition_label = tk.Label(self.current_action_frame, 
                                  text=f"{self.current_attacker.name} a choisi {attack_name} ({power_type})!", 
                                  font=self.subtitle_font, bg=self.bg_color, fg=self.accent_color)
        transition_label.pack(pady=10)
        
        defense_label = tk.Label(self.current_action_frame, 
                               text=f"{self.current_defender.name} - Choisissez votre défense:", 
                               font=self.subtitle_font, bg=self.bg_color, fg=self.text_color)
        defense_label.pack(pady=10)
        
        # Afficher les options de défense
        self.show_defense_options()
    
    def show_defense_options(self):
        # Afficher toutes les défenses disponibles
        defense_options_frame = tk.Frame(self.current_action_frame, bg=self.bg_color)
        defense_options_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Créer un cadre pour chaque type de pouvoir
        row = 0
        col = 0
        
        for power_type, defenses in self.defenses.items():
            power_frame = tk.Frame(defense_options_frame, bg=self.bg_color, bd=2, relief=tk.GROOVE, padx=10, pady=10)
            power_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            power_label = tk.Label(power_frame, text=power_type, font=self.subtitle_font, bg=self.bg_color, fg=self.accent_color)
            power_label.pack(pady=5)
            
            # Afficher les défenses de ce type de pouvoir
            for defense in defenses:
                defense_btn = tk.Button(power_frame, text=f"{defense['name']} - Réd: {defense['reduction']}", 
                                       command=lambda d=defense, p=power_type: self.select_defense(d, p),
                                       font=self.button_font, bg=self.button_color, fg=self.text_color, 
                                       width=25, relief=tk.FLAT)
                defense_btn.pack(pady=2, fill=tk.X)
            
            # Gestion de la grille
            col += 1
            if col > 2:  # 3 colonnes max
                col = 0
                row += 1
    
    def select_defense(self, defense, power_type):
        # Enregistrer la défense sélectionnée
        self.selected_defense = defense
        self.selected_defense_power = power_type
        
        # Calculer les dégâts
        self.calculate_damage()
        
    def calculate_damage(self):
        # Récupérer les valeurs
        attack_power = self.current_attacker.stats[self.selected_attack_power]
        attack_modifier = self.selected_attack["modifier"]
        defense_reduction = self.selected_defense["reduction"]
        
        # Calcul des dégâts: Dégâts = statistique utilisée × modificateur − réduction de défense
        damage = int(attack_power * attack_modifier) - defense_reduction
        damage = max(0, damage)  # Pas de dégâts négatifs
        
        # Appliquer les dégâts
        self.current_defender.current_hp -= damage
        self.current_defender.current_hp = max(0, self.current_defender.current_hp)  # Pas de PV négatifs
        
        # Afficher le résultat de l'attaque
        self.show_attack_result(damage)
    
    def show_attack_result(self, damage):
        # Effacer le cadre d'action actuel
        for widget in self.current_action_frame.winfo_children():
            widget.destroy()
            
        # Afficher le résultat
        result_frame = tk.Frame(self.current_action_frame, bg=self.bg_color)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        attack_label = tk.Label(result_frame, 
                            text=f"{self.current_attacker.name} utilise {self.selected_attack['name']} ({self.selected_attack_power})!", 
                            font=self.subtitle_font, bg=self.bg_color, fg=self.accent_color)
        attack_label.pack(pady=5)
        
        defense_label = tk.Label(result_frame, 
                             text=f"{self.current_defender.name} se défend avec {self.selected_defense['name']} ({self.selected_defense_power})!", 
                             font=self.subtitle_font, bg=self.bg_color, fg=self.text_color)
        defense_label.pack(pady=5)
        
        damage_label = tk.Label(result_frame, 
                             text=f"Dégâts infligés: {damage}", 
                             font=self.title_font, bg=self.bg_color, fg="#FF0000")
        damage_label.pack(pady=10)
        
        hp_label = tk.Label(result_frame, 
                         text=f"{self.current_defender.name} a maintenant {self.current_defender.current_hp}/{self.current_defender.max_hp} PV", 
                         font=self.subtitle_font, bg=self.bg_color, fg=self.text_color)
        hp_label.pack(pady=5)
        
        # Vérifier si le jeu est terminé
        if self.current_defender.current_hp <= 0:
            self.game_over = True
            game_over_label = tk.Label(result_frame, 
                                  text=f"{self.current_attacker.name} a vaincu {self.current_defender.name}!", 
                                  font=self.title_font, bg=self.bg_color, fg=self.accent_color)
            game_over_label.pack(pady=20)
            
            # Bouton pour recommencer
            restart_button = tk.Button(result_frame, text="NOUVEAU COMBAT", 
                                     command=self.start_game, 
                                     font=self.button_font, bg=self.accent_color, fg=self.text_color,)