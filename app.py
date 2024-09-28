import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fichier CSV pour stocker les données de performances
FILENAME = 'performances_cyclistes.csv'


# Sauvegarde des performances dans un fichier CSV
def sauvegarder_performance(date, distance, vitesse_moyenne, denivele, type_sortie):
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Distance (km)", "Vitesse Moyenne (km/h)", "Dénivelé (m)", "Type de Sortie"])

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, distance, vitesse_moyenne, denivele, type_sortie])


# Fonction pour afficher les performances précédentes
def afficher_performances():
    if not os.path.exists(FILENAME):
        return []

    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Sauter les en-têtes
        return list(reader)


# Fonction pour mettre à jour les performances après édition ou suppression
def reinitialiser_fichier(performances):
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Distance (km)", "Vitesse Moyenne (km/h)", "Dénivelé (m)", "Type de Sortie"])
        for perf in performances:
            writer.writerow(perf)


# Interface Tkinter
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Suivi des performances cyclistes")
        self.geometry("600x700")

        # Création des composants de l'interface
        self.create_widgets()

    def create_widgets(self):
        # Titre principal
        tk.Label(self, text="Enregistrer une nouvelle sortie", font=("Helvetica", 16)).pack(pady=10)

        # Distance
        tk.Label(self, text="Distance (km) :").pack()
        self.distance_entry = tk.Entry(self)
        self.distance_entry.pack()

        # Vitesse moyenne
        tk.Label(self, text="Vitesse Moyenne (km/h) :").pack()
        self.vitesse_entry = tk.Entry(self)
        self.vitesse_entry.pack()

        # Dénivelé
        tk.Label(self, text="Dénivelé (m) :").pack()
        self.denivele_entry = tk.Entry(self)
        self.denivele_entry.pack()

        # Type de sortie
        tk.Label(self, text="Type de sortie :").pack()
        self.type_sortie = ttk.Combobox(self, values=["Entraînement", "Course", "Sortie longue", "Sortie rapide"])
        self.type_sortie.pack()

        # Bouton pour sauvegarder la sortie
        tk.Button(self, text="Enregistrer la sortie", command=self.sauvegarder_sortie).pack(pady=10)

        # Section des performances enregistrées
        tk.Label(self, text="Historique des performances", font=("Helvetica", 16)).pack(pady=10)
        self.performance_listbox = tk.Listbox(self, height=10, width=70)
        self.performance_listbox.pack(pady=5)

        # Boutons pour éditer ou supprimer une sortie
        tk.Button(self, text="Éditer la sortie", command=self.editer_sortie).pack(pady=5)
        tk.Button(self, text="Supprimer la sortie", command=self.supprimer_sortie).pack(pady=5)

        # Bouton pour visualiser les performances
        tk.Button(self, text="Analyser les sorties", command=self.analyser_sorties).pack(pady=5)

        # Zone pour afficher les graphiques
        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack(pady=10)

        self.update_performance_list()

    def sauvegarder_sortie(self):
        # Récupération des données saisies
        distance = self.distance_entry.get()
        vitesse = self.vitesse_entry.get()
        denivele = self.denivele_entry.get()
        type_sortie = self.type_sortie.get()

        # Validation de la saisie
        if not distance or not vitesse or not denivele or not type_sortie:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            distance = float(distance)
            vitesse = float(vitesse)
            denivele = float(denivele)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides.")
            return

        # Date du jour
        date_aujourd_hui = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Sauvegarde des performances
        sauvegarder_performance(date_aujourd_hui, distance, vitesse, denivele, type_sortie)

        # Mise à jour de la liste des performances
        self.update_performance_list()

        # Réinitialisation des champs de saisie
        self.distance_entry.delete(0, tk.END)
        self.vitesse_entry.delete(0, tk.END)
        self.denivele_entry.delete(0, tk.END)
        self.type_sortie.set("")

        messagebox.showinfo("Succès", "La sortie a été enregistrée avec succès.")

    def update_performance_list(self):
        # Effacer la liste actuelle
        self.performance_listbox.delete(0, tk.END)

        # Récupérer et afficher les performances
        self.performances = afficher_performances()
        for perf in self.performances:
            display_text = f"Date: {perf[0]}, Distance: {perf[1]} km, Vitesse: {perf[2]} km/h, Dénivelé: {perf[3]} m, Type: {perf[4]}"
            self.performance_listbox.insert(tk.END, display_text)

    def editer_sortie(self):
        selection = self.performance_listbox.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Veuillez sélectionner une sortie à éditer.")
            return

        index = selection[0]
        selected_performance = self.performances[index]

        # Remplir les champs avec les données actuelles pour l'édition
        self.distance_entry.delete(0, tk.END)
        self.distance_entry.insert(0, selected_performance[1])

        self.vitesse_entry.delete(0, tk.END)
        self.vitesse_entry.insert(0, selected_performance[2])

        self.denivele_entry.delete(0, tk.END)
        self.denivele_entry.insert(0, selected_performance[3])

        self.type_sortie.set(selected_performance[4])

        # Supprimer l'entrée sélectionnée pour qu'elle soit réenregistrée
        self.performances.pop(index)
        reinitialiser_fichier(self.performances)
        self.update_performance_list()

    def supprimer_sortie(self):
        selection = self.performance_listbox.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Veuillez sélectionner une sortie à supprimer.")
            return

        index = selection[0]
        self.performances.pop(index)

        reinitialiser_fichier(self.performances)
        self.update_performance_list()

        messagebox.showinfo("Succès", "La sortie a été supprimée.")

    def analyser_sorties(self):
        if not self.performances:
            messagebox.showerror("Erreur", "Aucune donnée disponible pour l'analyse.")
            return

        # Calcul des statistiques
        total_distance = sum(float(perf[1]) for perf in self.performances)
        total_vitesse = sum(float(perf[2]) for perf in self.performances) / len(self.performances)
        total_denivele = sum(float(perf[3]) for perf in self.performances)

        # Affichage des statistiques
        analysis_text = f"Analyse des sorties:\n- Distance Totale: {total_distance:.2f} km\n- Vitesse Moyenne: {total_vitesse:.2f} km/h\n- Dénivelé Total: {total_denivele:.2f} m"
        messagebox.showinfo("Analyse des sorties", analysis_text)

        # Affichage des graphiques
        self.afficher_graphiques()

    def afficher_graphiques(self):
        # Vider le cadre des graphiques
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Extraire les données
        dates = [perf[0] for perf in self.performances]
        distances = [float(perf[1]) for perf in self.performances]
        vitesses = [float(perf[2]) for perf in self.performances]
        deniveles = [float(perf[3]) for perf in self.performances]

        # Création des graphiques
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5, 8))

        ax1.plot(dates, distances, marker='o', color='blue')
        ax1.set_title("Distance au fil du temps")
        ax1.set_ylabel("Distance (km)")
        ax1.tick_params(axis='x', rotation=45)

        ax2.plot(dates, vitesses, marker='o', color='orange')
        ax2.set_title("Vitesse moyenne au fil du temps")
        ax2.set_ylabel("Vitesse (km/h)")
        ax2.tick_params(axis='x', rotation=45)

        ax3.plot(dates, deniveles, marker='o', color='green')
        ax3.set_title("Dénivelé au fil du temps")
        ax3.set_ylabel("Dénivelé (m)")
        ax3.tick_params(axis='x', rotation=45)

        plt.tight_layout()

        # Intégrer les graphiques dans l'interface Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


# Démarrage de l'application
if __name__ == "__main__":
    app = Application()
    app.mainloop()
