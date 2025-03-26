import tkinter as tk
import random
import time
from tkinter import messagebox

class CarGame:
    def __init__(self, master, difficulty="Elementary"):
        """
        Initialise le jeu de course de voitures.

        Args:
            master (tk.Tk): La fenêtre principale du jeu.
            difficulty (str, optional): La difficulté du jeu ("Elementary" ou "Fast").
                La valeur par défaut est "Elementary".
        """
        self.master = master
        master.title("Car Racing Game")
        master.configure(bg="#0077cc")  # Fond bleu pour la fenêtre principale

        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="#0066cc")  # Fond bleu foncé
        self.canvas.pack(pady=10, padx=10)

        self.car_width = 40
        self.car_height = 60
        self.car_x = self.canvas_width // 2 - self.car_width // 2
        self.car_y = self.canvas_height - self.car_height - 10
        self.car = self.canvas.create_rectangle(
            self.car_x, self.car_y,
            self.car_x + self.car_width,
            self.car_y + self.car_height,
            fill="#003366", outline="#ffffff"  # Voiture bleu foncé avec contour blanc
        )

        self.obstacle_width = 30
        self.obstacle_height = 50
        self.obstacles = []
        self.score = 0
        self.score_label = self.canvas.create_text(
            10, 10,
            text=f"Score: {self.score}",
            anchor="nw",
            fill="white",
            font=("Arial", 12, "bold")
        )
        self.score_update_interval = 100
        self.score_counter = 0

        self.game_over = False
        self.difficulty = difficulty  # Utilisez la difficulté donnée
        self.set_difficulty(difficulty)  # Appliquez les paramètres de difficulté

        self.car_dx = 0
        self.car_dy = 0

        # Liaison des événements clavier pour le mouvement de la voiture
        self.canvas.bind_all("<Left>", self.start_move_left)
        self.canvas.bind_all("<Right>", self.start_move_right)
        self.canvas.bind_all("<Up>", self.start_move_up)
        self.canvas.bind_all("<Down>", self.start_move_down)
        self.canvas.bind_all("<KeyRelease-Left>", self.stop_move_left)
        self.canvas.bind_all("<KeyRelease-Right>", self.stop_move_right)
        self.canvas.bind_all("<KeyRelease-Up>", self.stop_move_up)
        self.canvas.bind_all("<KeyRelease-Down>", self.stop_move_down)

        self.create_road_lines()
        self.create_obstacles()
        self.update_game()

    def set_difficulty(self, difficulty):
        """
        Définit la vitesse du jeu et la vitesse des obstacles en fonction de la difficulté.

        Args:
            difficulty (str): La difficulté du jeu ("Elementary" ou "Fast").
        """
        if difficulty == "Elementary":
            self.speed = 5
            self.obstacle_speed = 3
        elif difficulty == "Fast":
            self.speed = 10
            self.obstacle_speed = 6
        else:
            self.speed = 5
            self.obstacle_speed = 3

    def create_road_lines(self):
        """Crée les lignes de la route sur le canvas."""
        line_width = 5
        line_color = "white"
        line_spacing = 50
        for i in range(0, self.canvas_height, line_spacing):
            self.canvas.create_line(
                self.canvas_width // 2, i,
                self.canvas_width // 2, i + 20,
                width=line_width,
                fill=line_color
            )

    def create_obstacles(self):
        """Crée un nouvel obstacle à une position aléatoire."""
        if not self.game_over:
            x = random.randint(50, self.canvas_width - 50 - self.obstacle_width)
            y = -self.obstacle_height
            obstacle = self.canvas.create_rectangle(
                x, y,
                x + self.obstacle_width,
                y + self.obstacle_height,
                fill="#cc0000", outline="#ffffff"  # Obstacle rouge avec contour blanc
            )
            self.obstacles.append(obstacle)
            self.master.after(random.randint(1000, 2000), self.create_obstacles)

    def start_move_left(self, event):
        """Démarre le mouvement de la voiture vers la gauche."""
        self.car_dx = -1

    def start_move_right(self, event):
        """Démarre le mouvement de la voiture vers la droite."""
        self.car_dx = 1

    def start_move_up(self, event):
        """Démarre le mouvement de la voiture vers le haut."""
        self.car_dy = -1

    def start_move_down(self, event):
        """Démarre le mouvement de la voiture vers le bas."""
        self.car_dy = 1

    def stop_move_left(self, event):
        """Arrête le mouvement de la voiture vers la gauche."""
        if self.car_dx == -1:
            self.car_dx = 0

    def stop_move_right(self, event):
        """Arrête le mouvement de la voiture vers la droite."""
        if self.car_dx == 1:
            self.car_dx = 0

    def stop_move_up(self, event):
        """Arrête le mouvement de la voiture vers le haut."""
        if self.car_dy == -1:
            self.car_dy = 0

    def stop_move_down(self, event):
        """Arrête le mouvement de la voiture vers le bas."""
        if self.car_dy == 1:
            self.car_dy = 0

    def move_car(self):
        """Déplace la voiture en fonction de sa vitesse actuelle."""
        if not self.game_over:
            new_x = self.car_x + self.car_dx * self.speed
            new_y = self.car_y + self.car_dy * self.speed

            # Empêche la voiture de sortir du canvas
            new_x = max(0, min(new_x, self.canvas_width - self.car_width))
            new_y = max(0, min(new_y, self.canvas_height - self.car_height))

            self.canvas.move(
                self.car,
                new_x - self.car_x,
                new_y - self.car_y
            )  # Utilisez la distance réelle
            self.car_x = new_x
            self.car_y = new_y

    def update_game(self):
        """Met à jour l'état du jeu (mouvement de la voiture, des obstacles, etc.)."""
        if not self.game_over:
            self.move_car()
            self.move_obstacles()
            self.check_collisions()
            self.update_score()
            self.master.after(20, self.update_game)

    def move_obstacles(self):
        """Déplace tous les obstacles vers le bas."""
        for obstacle in self.obstacles:
            self.canvas.move(obstacle, 0, self.obstacle_speed)
            y1, y2 = self.canvas.coords(obstacle)[1], self.canvas.coords(obstacle)[3]
            if y2 > self.canvas_height:
                self.canvas.delete(obstacle)
                self.obstacles.remove(obstacle)

    def check_collisions(self):
        """Vérifie si la voiture entre en collision avec un obstacle."""
        car_coords = self.canvas.coords(self.car)
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if self.check_collision(car_coords, obstacle_coords):
                self.game_over = True
                self.show_game_over()
                break

    def check_collision(self, rect1, rect2):
        """
        Vérifie si deux rectangles se chevauchent.

        Args:
            rect1 (tuple): (x1, y1, x2, y2) les coordonnées du premier rectangle.
            rect2 (tuple): (x1, y1, x2, y2) les coordonnées du deuxième rectangle.

        Returns:
            bool: True si les rectangles se croisent, False sinon.
        """
        x1, y1, x2, y2 = rect1
        x3, y3, x4, y4 = rect2
        return not (x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4)

    def update_score(self):
        """Met à jour le score du joueur."""
        self.score_counter += 1
        if self.score_counter >= self.score_update_interval:
            self.score += 1
            self.canvas.itemconfig(
                self.score_label,
                text=f"Score: {self.score}"
            )
            self.score_counter = 0

    def show_game_over(self):
        """Affiche l'écran de fin de partie."""
        self.canvas.create_rectangle(
            100, 150, 500, 250,
            fill="#003366", outline="white", width=2
        )
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2 - 20,
            text="Game Over!",
            font=("Arial", 30, "bold"),
            fill="white"
        )
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2 + 30,
            text=f"Your Score: {self.score}",
            font=("Arial", 20),
            fill="white"
        )

    def restart_game(self):
        """Redémarre le jeu."""
        self.canvas.delete("all")
        self.obstacles = []
        self.score = 0
        self.score_counter = 0
        self.game_over = False
        self.car_x = self.canvas_width // 2 - self.car_width // 2
        self.car_y = self.canvas_height - self.car_height - 10
        self.car = self.canvas.create_rectangle(
            self.car_x,
            self.car_y,
            self.car_x + self.car_width,
            self.car_y + self.car_height,
            fill="#003366", outline="#ffffff"
        )
        self.score_label = self.canvas.create_text(
            10, 10,
            text=f"Score: {self.score}",
            anchor="nw",
            fill="white",
            font=("Arial", 12, "bold")
        )
        self.create_road_lines()
        self.create_obstacles()
        self.update_game()

class MenuPrincipal:
    """
    Gère le menu principal du jeu.
    """
    def __init__(self, master):
        """
        Initialise le menu principal.

        Args:
            master (tk.Tk): La fenêtre principale de l'application.
        """
        self.master = master
        master.title("Menu des Jeux")
        master.configure(bg="#0077cc")  # Fond bleu pour la fenêtre principale
        self.scores = []  # Pour stocker les scores de jeu

        self.label_bienvenue = tk.Label(
            master,
            text="Bienvenue dans le menu du jeux M_rocha 😋😋 !",
            font=("Arial", 16, "bold"),
            bg="#0077cc", fg="white"  # Texte blanc sur fond bleu
        )
        self.label_bienvenue.pack(pady=20)

        # Style des boutons
        button_style = {
            "bg": "#005599",  # Fond bleu moyen
            "fg": "white",    # Texte blanc
            "activebackground": "#003366",  # Fond bleu foncé quand cliqué
            "activeforeground": "white",
            "font": ("Arial", 12),
            "width": 20,
            "height": 2,
            "relief": "raised",
            "borderwidth": 3
        }

        self.bouton_demarrer = tk.Button(
            master,
            text="Démarrer le jeu",
            command=self.demarrer_jeu,
            **button_style
        )
        self.bouton_demarrer.pack(pady=10)

        self.bouton_restart = tk.Button(
            master,
            text="Restart",
            command=self.restart_game,
            **button_style
        )
        self.bouton_restart.pack(pady=10)

        self.bouton_niveau = tk.Menubutton(
            master,
            text="Niveau",
            **button_style
        )
        self.bouton_niveau.pack(pady=10)
        self.menu_niveau = tk.Menu(
            self.bouton_niveau,
            tearoff=0,
            bg="#005599",  # Fond bleu moyen
            fg="white",    # Texte blanc
            activebackground="#003366"  # Fond bleu foncé quand sélectionné
        )
        self.bouton_niveau["menu"] = self.menu_niveau
        self.menu_niveau.add_command(
            label="Élémentaire",
            command=lambda: self.changer_niveau("Elementary")
        )
        self.menu_niveau.add_command(
            label="Rapide",
            command=lambda: self.changer_niveau("Fast")
        )

        self.bouton_voir_scores = tk.Button(
            master,
            text="Voir les scores",
            command=self.voir_scores,
            **button_style
        )
        self.bouton_voir_scores.pack(pady=10)

        self.bouton_quitter = tk.Button(
            master,
            text="Quitter le jeu",
            command=master.quit,
            **button_style
        )
        self.bouton_quitter.pack(pady=20)

        self.jeu = None  # Instance du jeu CarGame
        self.difficulty = "Elementary"  # Difficulté par défaut

    def demarrer_jeu(self):
        """Démarre une nouvelle partie du jeu."""
        if self.jeu is None or self.jeu.game_over:
            # Si aucun jeu n'est en cours ou si le jeu précédent est terminé
            if self.jeu is not None:
                self.jeu.master.destroy()  # Détruit l'ancienne fenêtre du jeu
            nouvelle_fenetre = tk.Toplevel(self.master)  # Crée une nouvelle fenêtre
            nouvelle_fenetre.configure(bg="#0077cc")  # Fond bleu pour la nouvelle fenêtre
            self.jeu = CarGame(
                nouvelle_fenetre,
                self.difficulty
            )  # Passe la difficulté actuelle
            self.bouton_restart.config(
                command=self.jeu.restart_game
            )  # Configure le bouton Restart pour le nouveau jeu
        else:
            messagebox.showinfo(
                "Info",
                "Le jeu est déjà en cours."
            )  # Affiche un message si le jeu est en cours

    def restart_game(self):
        """Redémarre la partie de jeu en cours."""
        if self.jeu:
            self.jeu.restart_game()
        else:
            messagebox.showinfo(
                "Info",
                "Le jeu n'a pas encore démarré."
            )  # Affiche un message si le jeu n'a pas démarré

    def changer_niveau(self, niveau):
        """
        Change le niveau de difficulté du jeu.

        Args:
            niveau (str): Le niveau de difficulté sélectionné ("Elementary" ou "Fast").
        """
        self.difficulty = niveau
        if self.jeu:
            self.jeu.set_difficulty(
                niveau
            )  # Met à jour la difficulté dans l'instance du jeu
            self.jeu.restart_game()  # Redémarre le jeu pour appliquer la nouvelle difficulté

    def voir_scores(self):
        """Affiche les scores enregistrés."""
        if self.jeu and self.jeu.game_over:
            self.scores.append(
                self.jeu.score
            )  # Ajoute le score actuel à la liste
        if not self.scores:
            messagebox.showinfo(
                "Scores",
                "Aucun score enregistré."
            )  # Affiche un message si aucun score n'est enregistré
        else:
            scores_str = "\n".join(
                [f"Score {i + 1}: {score}" for i, score in enumerate(self.scores)]
            )  # Formatte les scores
            messagebox.showinfo(
                "Scores",
                f"Scores enregistrés:\n{scores_str}"
            )  # Affiche les scores

def main():
    """Fonction principale pour démarrer l'application."""
    root = tk.Tk()  # Crée la fenêtre principale
    root.configure(bg="#0077cc")  # Fond bleu pour la fenêtre principale
    MenuPrincipal(root)  # Crée une instance du menu principal
    root.mainloop()  # Démarre la boucle principale de l'interface graphique

if __name__ == "__main__":
    main()  # Appelle la fonction main lorsque le script est exécuté