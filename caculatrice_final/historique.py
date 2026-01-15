
import os
import tkinter as tk
from config import COLORS, FICHIER_HISTORIQUE


class HistoriqueManager:
    """Gestionnaire de l'historique des calculs"""
    
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.history_window = None
        self.history_listbox = None

    def sauvegarder(self, calcul: str, resultat: str):
        """Sauvegarde un calcul dans l'historique"""
        try:
            with open(FICHIER_HISTORIQUE, "a", encoding="utf-8") as f:
                f.write(f"{calcul} = {resultat}\n")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")

    def afficher(self):
        """Affiche la fenêtre d'historique"""
        if self.history_window and tk.Toplevel.winfo_exists(self.history_window):
            self.history_window.lift()
            return

        self.history_window = tk.Toplevel(self.parent_window)
        self.history_window.title("Historique des calculs")
        self.history_window.geometry("400x500")
        
        # Frame principal
        main_frame = tk.Frame(self.history_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Label titre
        title_label = tk.Label(
            main_frame,
            text="Historique",
            font=("Arial", 16, "bold"),
            bg=COLORS["white"]
        )
        title_label.pack(pady=(0, 10))

        # Frame pour la listbox et scrollbar
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox
        self.history_listbox = tk.Listbox(
            list_frame,
            font=("Courier", 12),
            yscrollcommand=scrollbar.set,
            bg=COLORS["white"],
            fg=COLORS["black"]
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        # Charger l'historique
        self.charger()

        # Boutons
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=(10, 0))

        clear_btn = tk.Button(
            btn_frame,
            text="Effacer l'historique",
            font=("Arial", 12),
            bg=COLORS["rouge"],
            fg=COLORS["white"],
            command=self.effacer
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        close_btn = tk.Button(
            btn_frame,
            text="Fermer",
            font=("Arial", 12),
            bg=COLORS["dark_gray"],
            fg=COLORS["white"],
            command=self.history_window.destroy
        )
        close_btn.pack(side=tk.LEFT, padx=5)

    def charger(self):
        """Charge l'historique depuis le fichier"""
        if not self.history_listbox:
            return
            
        self.history_listbox.delete(0, tk.END)
        try:
            if os.path.exists(FICHIER_HISTORIQUE):
                with open(FICHIER_HISTORIQUE, "r", encoding="utf-8") as f:
                    for ligne in f:
                        self.history_listbox.insert(tk.END, ligne.strip())
        except Exception as e:
            self.history_listbox.insert(tk.END, f"Erreur de chargement: {e}")

    def effacer(self):
        """Efface tout l'historique"""
        try:
            if os.path.exists(FICHIER_HISTORIQUE):
                os.remove(FICHIER_HISTORIQUE)
            if self.history_listbox:
                self.history_listbox.delete(0, tk.END)
        except Exception as e:
            print(f"Erreur lors de l'effacement: {e}")