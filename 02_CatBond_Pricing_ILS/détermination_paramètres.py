import pandas as pd
import numpy as np
import os

def calibrer_parametres_catbond(chemin_csv):
    """
    Lit le fichier CSV nettoyé des ouragans, corrige les relevés multiples 
    (6-hourly tracks) et calcule les paramètres statistiques pour le modèle ALM.
    """
    print(f"Chargement des données depuis : {chemin_csv}...\n")
    df = pd.read_csv(chemin_csv)
    
    # ==========================================
    # 1. CALIBRATION DE LA FRÉQUENCE (LAMBDA)
    # ==========================================
    # On groupe par année, et on compte le nombre de 'Storm_ID' uniques.
    # 'nunique()' est la fonction magique qui évite de compter les doublons.
    ouragans_par_an = df.groupby('Year')['Storm_ID'].nunique()
    
    # Lambda est simplement la moyenne arithmétique de ces comptes annuels
    lambda_poisson = ouragans_par_an.mean()
    
    # ==========================================
    # 2. CALIBRATION DE LA SÉVÉRITÉ (ALPHA - PARETO)
    # Paramétrique basé sur la vitesse du vent
    # ==========================================
    # Pour la sévérité, on ne veut que la vitesse MAXIMALE atteinte par chaque ouragan
    vents_max_par_ouragan = df.groupby('Storm_ID')['Max_Wind_knots'].max()
    
    # Dans l'industrie (Cat Bonds), on s'intéresse souvent aux ouragans majeurs (Catégorie 3+)
    # Catégorie 3 sur l'échelle Saffir-Simpson commence à 96 noeuds.
    # On fixe donc notre point d'attachement statistique (xm) à 96.
    xm = 96
    
    # On ne garde que les ouragans qui ont dépassé ce seuil
    vents_extremes = vents_max_par_ouragan[vents_max_par_ouragan >= xm]
    
    # Calcul de l'estimateur du Maximum de Vraisemblance (MLE) pour la loi de Pareto
    n = len(vents_extremes)
    alpha_pareto = n / np.sum(np.log(vents_extremes / xm))
    
    # ==========================================
    # AFFICHAGE DES RÉSULTATS POUR LE DESK QUANT
    # ==========================================
    print("--- RÉSULTATS DE LA CALIBRATION ---")
    print(f"Période analysée : {ouragans_par_an.index.min()} - {ouragans_par_an.index.max()}")
    print(f"Total d'ouragans uniques identifiés : {ouragans_par_an.sum()}")
    print(f"Total d'ouragans majeurs (>= 96 noeuds) : {n}\n")
    
    print("-> Paramètre FRÉQUENCE (Loi de Poisson) :")
    print(f"   Lambda (λ) = {lambda_poisson:.3f} ouragans par an")
    
    print("\n-> Paramètre SÉVÉRITÉ (Loi de Pareto) :")
    print(f"   Seuil minimum (xm) = {xm} noeuds")
    print(f"   Indice de queue (α) = {alpha_pareto:.4f}")
    
    return lambda_poisson, alpha_pareto, xm

if __name__ == "__main__":
    # Construit le chemin robuste vers ton fichier CSV
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    chemin_fichier = os.path.join(dossier_script, "hurdat2_1980_2025.csv")
    
    # Exécution de la calibration
    if os.path.exists(chemin_fichier):
        lam, alf, xm = calibrer_parametres_catbond(chemin_fichier)
    else:
        print(f"ERREUR : Le fichier {chemin_fichier} n'a pas été trouvé.")
        print("Assure-toi d'avoir bien exécuté le script d'extraction précédent.")