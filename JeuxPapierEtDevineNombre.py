import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random

class JeuDevineNombre:
    def __init__(self, master, on_close_callback):
        self.master = master
        self.on_close_callback = on_close_callback
        master.title("Devine le Nombre - 2 Joueurs")
        master.geometry("450x450")
        master.configure(bg="#2c3e50")
        master.resizable(False, False)
        
        # Variables des joueurs
        self.joueur_actuel = "Joueur 1"
        self.joueur1_nom = "Joueur 1"
        self.joueur2_nom = "Joueur 2"
        self.joueur1_score = 0
        self.joueur2_score = 0
        self.tour = 1
        self.max_tours = 3

        # Interface
        self.setup_ui()

    def setup_ui(self):
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 12))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"), foreground="#f1c40f")
        self.style.configure("Player.TLabel", font=("Arial", 14, "bold"), foreground="#3498db")

        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(pady=15, padx=20, fill="both", expand=True)

        self.title_label = ttk.Label(self.main_frame, text="🔢 Devine le Nombre 🔢", style="Title.TLabel")
        self.title_label.pack(pady=(0, 10))

        self.joueur_label = ttk.Label(self.main_frame, text=f"Au tour de: {self.joueur_actuel}", style="Player.TLabel")
        self.joueur_label.pack(pady=5)

        self.score_frame = ttk.Frame(self.main_frame)
        self.score_frame.pack(pady=5)
        
        self.label_score_j1 = ttk.Label(self.score_frame, text=f"{self.joueur1_nom}: 0", font=("Arial", 12), foreground="#2ecc71")
        self.label_score_j1.pack(side="left", padx=10)

        self.label_score_j2 = ttk.Label(self.score_frame, text=f"{self.joueur2_nom}: 0", font=("Arial", 12), foreground="#e74c3c")
        self.label_score_j2.pack(side="left", padx=10)

        self.label_tour = ttk.Label(self.main_frame, text=f"Tour {self.tour}/{self.max_tours}", font=("Arial", 10), foreground="#bdc3c7")
        self.label_tour.pack(pady=5)

        self.nombre_a_deviner = random.randint(1, 100)
        self.tentatives_restantes = 7

        self.label_instructions = ttk.Label(self.main_frame, text="Devinez le nombre entre 1 et 100", justify="center")
        self.label_instructions.pack(pady=10)

        self.label_tentatives = ttk.Label(self.main_frame, text=f"Tentatives restantes: {self.tentatives_restantes}", font=("Arial", 12, "bold"), foreground="#f1c40f")
        self.label_tentatives.pack()

        self.entry_frame = ttk.Frame(self.main_frame)
        self.entry_frame.pack(pady=10)
        
        self.entry_proposition = ttk.Entry(self.entry_frame, width=15, font=("Arial", 12), justify="center")
        self.entry_proposition.pack(side="left", padx=5)
        
        self.bouton_deviner = ttk.Button(self.entry_frame, text="Deviner", command=self.verifier_proposition)
        self.bouton_deviner.pack(side="left")

        self.historique_text = tk.Text(self.main_frame, height=6, width=40, bg="#34495e", fg="#ecf0f1", font=("Arial", 10), state="disabled", padx=5, pady=5)
        self.historique_text.pack(pady=10)

        self.entry_proposition.focus_set()
        self.master.bind("<Return>", lambda event: self.verifier_proposition())

    def verifier_proposition(self):
        try:
            proposition = int(self.entry_proposition.get())
            if proposition < 1 or proposition > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre entre 1 et 100.", parent=self.master)
            return

        self.tentatives_restantes -= 1
        self.label_tentatives.config(text=f"Tentatives restantes: {self.tentatives_restantes}")

        self.historique_text.config(state="normal")
        self.historique_text.insert("end", f"{self.joueur_actuel}: {proposition}\n")
        self.historique_text.see("end")
        self.historique_text.config(state="disabled")

        if proposition < self.nombre_a_deviner:
            messagebox.showinfo("Indice", "C'est plus grand !", parent=self.master)
        elif proposition > self.nombre_a_deviner:
            messagebox.showinfo("Indice", "C'est plus petit !", parent=self.master)
        else:
            if self.joueur_actuel == self.joueur1_nom:
                self.joueur1_score += 1
                self.label_score_j1.config(text=f"{self.joueur1_nom}: {self.joueur1_score}")
            else:
                self.joueur2_score += 1
                self.label_score_j2.config(text=f"{self.joueur2_nom}: {self.joueur2_score}")
            
            messagebox.showinfo("Bravo !", f"{self.joueur_actuel} a trouvé le nombre {self.nombre_a_deviner} !", parent=self.master)
            self.changer_joueur()
            return

        if self.tentatives_restantes == 0:
            messagebox.showinfo("Perdu !", f"{self.joueur_actuel} n'a pas trouvé le nombre {self.nombre_a_deviner}.", parent=self.master)
            self.changer_joueur()

        self.entry_proposition.delete(0, tk.END)

    def changer_joueur(self):
        if self.joueur_actuel == self.joueur1_nom:
            self.joueur_actuel = self.joueur2_nom
        else:
            self.joueur_actuel = self.joueur1_nom
            self.tour += 1
            self.label_tour.config(text=f"Tour {self.tour}/{self.max_tours}")

        if self.tour > self.max_tours:
            self.fin_partie()
            return

        if self.joueur_actuel == self.joueur2_nom and self.tour == 1 and self.joueur2_nom == "Joueur 2":
            self.joueur2_nom = simpledialog.askstring("Nouveau joueur", "Entrez le nom du Joueur 2:", parent=self.master)
            if not self.joueur2_nom:
                self.joueur2_nom = "Joueur 2"
            self.label_score_j2.config(text=f"{self.joueur2_nom}: {self.joueur2_score}")

        self.joueur_label.config(text=f"Au tour de: {self.joueur_actuel}")
        self.nombre_a_deviner = random.randint(1, 100)
        self.tentatives_restantes = 7
        self.label_tentatives.config(text=f"Tentatives restantes: {self.tentatives_restantes}")
        self.entry_proposition.delete(0, tk.END)
        self.historique_text.config(state="normal")
        self.historique_text.insert("end", f"--- Nouveau tour: {self.joueur_actuel} ---\n")
        self.historique_text.see("end")
        self.historique_text.config(state="disabled")
        self.entry_proposition.focus_set()

    def fin_partie(self):
        gagnant = self.joueur1_nom if self.joueur1_score > self.joueur2_score else \
                 self.joueur2_nom if self.joueur2_score > self.joueur1_score else None
        
        if gagnant:
            message = f"Fin de la partie !\n{gagnant} gagne avec {max(self.joueur1_score, self.joueur2_score)} points !"
        else:
            message = f"Fin de la partie !\nÉgalité entre {self.joueur1_nom} et {self.joueur2_nom} !"
        
        message += f"\n\nScores finaux:\n{self.joueur1_nom}: {self.joueur1_score}\n{self.joueur2_nom}: {self.joueur2_score}"
        
        messagebox.showinfo("Résultats", message, parent=self.master)
        self.on_close_callback()
        self.master.destroy()

class JeuPierrePapierCiseaux:
    def __init__(self, master, on_close_callback):
        self.master = master
        self.on_close_callback = on_close_callback
        master.title("Pierre-Papier-Ciseaux - 2 Joueurs")
        master.geometry("500x500")
        master.configure(bg="#2c3e50")
        master.resizable(False, False)

        # Variables des joueurs
        self.joueur_actuel = "Joueur 1"
        self.joueur1_nom = "Joueur 1"
        self.joueur2_nom = "Joueur 2"
        self.joueur1_score = 0
        self.joueur2_score = 0
        self.manche = 1
        self.max_manches = 5

        # Interface
        self.setup_ui()

    def setup_ui(self):
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 12))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"), foreground="#f1c40f")
        self.style.configure("Player.TLabel", font=("Arial", 14, "bold"), foreground="#3498db")

        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(pady=15, padx=20, fill="both", expand=True)

        self.title_label = ttk.Label(self.main_frame, text="✊ Pierre-Papier-Ciseaux ✌️", style="Title.TLabel")
        self.title_label.pack(pady=(0, 10))

        self.joueur_label = ttk.Label(self.main_frame, text=f"Au tour de: {self.joueur_actuel}", style="Player.TLabel")
        self.joueur_label.pack(pady=5)

        self.score_frame = ttk.Frame(self.main_frame)
        self.score_frame.pack(pady=5)
        
        self.label_score_j1 = ttk.Label(self.score_frame, text=f"{self.joueur1_nom}: 0", font=("Arial", 12), foreground="#2ecc71")
        self.label_score_j1.pack(side="left", padx=10)

        self.label_score_j2 = ttk.Label(self.score_frame, text=f"{self.joueur2_nom}: 0", font=("Arial", 12), foreground="#e74c3c")
        self.label_score_j2.pack(side="left", padx=10)

        self.label_manche = ttk.Label(self.main_frame, text=f"Manche {self.manche}/{self.max_manches}", font=("Arial", 10), foreground="#bdc3c7")
        self.label_manche.pack(pady=5)

        self.label_instructions = ttk.Label(self.main_frame, text="Choisissez votre coup :", font=("Arial", 12))
        self.label_instructions.pack(pady=10)

        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=10)

        self.bouton_pierre = ttk.Button(self.buttons_frame, text="Pierre ✊", command=lambda: self.jouer("pierre"), width=10)
        self.bouton_pierre.grid(row=0, column=0, padx=5)

        self.bouton_papier = ttk.Button(self.buttons_frame, text="Papier ✋", command=lambda: self.jouer("papier"), width=10)
        self.bouton_papier.grid(row=0, column=1, padx=5)

        self.bouton_ciseaux = ttk.Button(self.buttons_frame, text="Ciseaux ✌️", command=lambda: self.jouer("ciseaux"), width=10)
        self.bouton_ciseaux.grid(row=0, column=2, padx=5)

        self.historique_text = tk.Text(self.main_frame, height=8, width=50, bg="#34495e", fg="#ecf0f1", font=("Arial", 10), state="disabled", padx=5, pady=5)
        self.historique_text.pack(pady=10)

        # Demander le nom du joueur 2
        self.demander_nom_joueur2()

    def demander_nom_joueur2(self):
        self.joueur2_nom = simpledialog.askstring("Nouveau joueur", "Entrez le nom du Joueur 2:", parent=self.master)
        if not self.joueur2_nom:
            self.joueur2_nom = "Joueur 2"
        self.label_score_j2.config(text=f"{self.joueur2_nom}: {self.joueur2_score}")

    def jouer(self, choix_joueur):
        choix_ordi = random.choice(["pierre", "papier", "ciseaux"])
        resultat = self.determiner_resultat(choix_joueur, choix_ordi)

        self.historique_text.config(state="normal")
        self.historique_text.insert("end", f"{self.joueur_actuel}: {choix_joueur} vs Ordinateur: {choix_ordi}\n")
        self.historique_text.insert("end", f"Résultat: {resultat}\n\n")
        self.historique_text.see("end")
        self.historique_text.config(state="disabled")

        if "gagné" in resultat:
            if self.joueur_actuel == self.joueur1_nom:
                self.joueur1_score += 1
                self.label_score_j1.config(text=f"{self.joueur1_nom}: {self.joueur1_score}")
            else:
                self.joueur2_score += 1
                self.label_score_j2.config(text=f"{self.joueur2_nom}: {self.joueur2_score}")

        self.changer_joueur()

    def determiner_resultat(self, choix_joueur, choix_ordi):
        if choix_joueur == choix_ordi:
            return "Égalité !"
        elif (choix_joueur == "pierre" and choix_ordi == "ciseaux") or \
             (choix_joueur == "papier" and choix_ordi == "pierre") or \
             (choix_joueur == "ciseaux" and choix_ordi == "papier"):
            return f"{self.joueur_actuel} a gagné !"
        else:
            return f"{self.joueur_actuel} a perdu !"

    def changer_joueur(self):
        if self.joueur_actuel == self.joueur1_nom:
            self.joueur_actuel = self.joueur2_nom
        else:
            self.joueur_actuel = self.joueur1_nom
            self.manche += 1
            self.label_manche.config(text=f"Manche {self.manche}/{self.max_manches}")

        if self.manche > self.max_manches:
            self.fin_partie()
            return

        self.joueur_label.config(text=f"Au tour de: {self.joueur_actuel}")

    def fin_partie(self):
        gagnant = self.joueur1_nom if self.joueur1_score > self.joueur2_score else \
                 self.joueur2_nom if self.joueur2_score > self.joueur1_score else None
        
        if gagnant:
            message = f"Fin de la partie !\n{gagnant} gagne avec {max(self.joueur1_score, self.joueur2_score)} points !"
        else:
            message = f"Fin de la partie !\nÉgalité entre {self.joueur1_nom} et {self.joueur2_nom} !"
        
        message += f"\n\nScores finaux:\n{self.joueur1_nom}: {self.joueur1_score}\n{self.joueur2_nom}: {self.joueur2_score}"
        
        messagebox.showinfo("Résultats", message, parent=self.master)
        self.on_close_callback()
        self.master.destroy()

class MenuPrincipal:
    def __init__(self, master):
        self.master = master
        master.title("M_rocha Games - Menu Principal")
        master.geometry("500x400")
        master.configure(bg="#2c3e50")
        master.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 12))
        self.style.configure("Title.TLabel", font=("Arial", 20, "bold"), foreground="#f1c40f")
        self.style.configure("TButton", font=("Arial", 12), padding=10, width=20)
        self.style.map("TButton", 
                      background=[("active", "#3498db"), ("!disabled", "#2980b9")],
                      foreground=[("!disabled", "white")])

        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        self.label_bienvenue = ttk.Label(self.main_frame, text="🎮 M_rocha Games 🎮", style="Title.TLabel")
        self.label_bienvenue.pack(pady=(0, 30))

        self.bouton_devine_nombre = ttk.Button(
            self.main_frame, 
            text="Devine le Nombre (2 joueurs)", 
            command=lambda: self.lancer_jeu(JeuDevineNombre),
            style="TButton"
        )
        self.bouton_devine_nombre.pack(pady=15)

        self.bouton_ppc = ttk.Button(
            self.main_frame, 
            text="Pierre-Papier-Ciseaux (2 joueurs)", 
            command=lambda: self.lancer_jeu(JeuPierrePapierCiseaux),
            style="TButton"
        )
        self.bouton_ppc.pack(pady=15)

        self.bouton_quitter = ttk.Button(
            self.main_frame, 
            text="Quitter", 
            command=master.quit,
            style="TButton"
        )
        self.bouton_quitter.pack(pady=15)

    def lancer_jeu(self, jeu_class):
        nouvelle_fenetre = tk.Toplevel(self.master)
        jeu_class(nouvelle_fenetre, lambda: None)

def main():
    root = tk.Tk()
    MenuPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()