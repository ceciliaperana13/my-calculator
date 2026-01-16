"""
Gestionnaire d'historique des calculs avec sauvegarde persistante
"""

import tkinter as tk
import os
from config import COLORS, MAX_HISTORY_ENTRIES


class HistoriqueManager:
    """Gère l'historique des calculs avec sauvegarde dans un fichier"""
    
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.historique = []
        self.hist_window = None
        self.listbox = None
        self.fichier_historique = "historique.txt"
        
        # Charger l'historique existant au démarrage
        self._charger_historique()
    
    def _charger_historique(self):
        """Charge l'historique depuis le fichier texte"""
        if os.path.exists(self.fichier_historique):
            try:
                with open(self.fichier_historique, 'r', encoding='utf-8') as f:
                    for ligne in f:
                        ligne = ligne.strip()
                        if ligne and '=' in ligne:
                            # Format: "expression = resultat"
                            parties = ligne.split('=', 1)
                            if len(parties) == 2:
                                expression = parties[0].strip()
                                resultat = parties[1].strip()
                                self.historique.append({
                                    "expression": expression,
                                    "resultat": resultat
                                })
                
                # Limiter au nombre max d'entrées
                if len(self.historique) > MAX_HISTORY_ENTRIES:
                    self.historique = self.historique[-MAX_HISTORY_ENTRIES:]
                    self._sauvegarder_fichier()  # Réenregistrer la version tronquée
                    
            except Exception as e:
                print(f"Erreur lors du chargement de l'historique: {e}")
                self.historique = []
    
    def _sauvegarder_fichier(self):
        """Sauvegarde tout l'historique dans le fichier"""
        try:
            with open(self.fichier_historique, 'w', encoding='utf-8') as f:
                for entry in self.historique:
                    f.write(f"{entry['expression']} = {entry['resultat']}\n")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique: {e}")
    
    def sauvegarder(self, expression, resultat):
        """Sauvegarde un nouveau calcul dans l'historique"""
        self.historique.append({
            "expression": expression,
            "resultat": resultat
        })
        
        # Limiter le nombre d'entrées
        if len(self.historique) > MAX_HISTORY_ENTRIES:
            self.historique = self.historique[-MAX_HISTORY_ENTRIES:]
        
        # Sauvegarder dans le fichier
        self._sauvegarder_fichier()
        
        # Mettre à jour la listbox si la fenêtre est ouverte
        if self.listbox and self.hist_window and self.hist_window.winfo_exists():
            self._rafraichir_liste()
    
    def afficher(self):
        """Affiche la fenêtre d'historique"""
        # Si la fenêtre existe déjà, la mettre en avant
        if self.hist_window and self.hist_window.winfo_exists():
            self.hist_window.lift()
            self.hist_window.focus_force()
            return
        
        self._creer_fenetre()
    
    def _creer_fenetre(self):
        """Crée la fenêtre d'historique"""
        self.hist_window = tk.Toplevel(self.parent_window)
        self.hist_window.title("Historique")
        self.hist_window.geometry("400x550")
        self.hist_window.resizable(False, False)
        
        self._creer_liste()
        self._creer_boutons()
    
    def _creer_liste(self):
        """Crée la liste scrollable de l'historique"""
        frame = tk.Frame(self.hist_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 12),
            bg=COLORS["black"],
            fg=COLORS["white"]
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Remplir avec l'historique
        self._remplir_liste()
    
    def _remplir_liste(self):
        """Remplit la listbox avec les entrées d'historique (plus récent en haut)"""
        self.listbox.delete(0, tk.END)
        for entry in reversed(self.historique):
            self.listbox.insert(tk.END, f"{entry['expression']} = {entry['resultat']}")
    
    def _rafraichir_liste(self):
        """Rafraîchit l'affichage de la liste"""
        if self.listbox:
            self._remplir_liste()
    
    def _creer_boutons(self):
        """Crée les boutons de contrôle"""
        btn_frame = tk.Frame(self.hist_window)
        btn_frame.pack(pady=10)
        
        # Bouton effacer
        btn_clear = tk.Button(
            btn_frame,
            text="Effacer l'historique",
            command=self._effacer_historique,
            bg=COLORS["blue"],
            fg="white",
            font=("Arial", 12),
            width=18
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Bouton fermer
        btn_close = tk.Button(
            btn_frame,
            text="Fermer",
            command=self.hist_window.destroy,
            bg=COLORS["red"],
            fg="white",
            font=("Arial", 12),
            width=18
        )
        btn_close.pack(side=tk.LEFT, padx=5)
    
    def _effacer_historique(self):
        """Efface tout l'historique (mémoire + fichier)"""
        self.historique = []
        
        # Effacer le fichier
        try:
            if os.path.exists(self.fichier_historique):
                os.remove(self.fichier_historique)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier: {e}")
        
        # Vider la listbox
        if self.listbox:
            self.listbox.delete(0, tk.END)