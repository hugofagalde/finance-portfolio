import pandas as pd
import numpy as np
import os

def calibrer_parametres_catbond(chemin_csv):
    print(f"Chargement des données depuis : {chemin_csv}...\n")
    df = pd.read_csv(chemin_csv)
    
    ouragans_par_an = df.groupby('Year')['Storm_ID'].nunique()
    
    lambda_poisson = ouragans_par_an.mean()
    
    vents_max_par_ouragan = df.groupby('Storm_ID')['Max_Wind_knots'].max()

    xm = 96
    
    vents_extremes = vents_max_par_ouragan[vents_max_par_ouragan >= xm]
    
    n = len(vents_extremes)
    alpha_pareto = n / np.sum(np.log(vents_extremes / xm))
    
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
    dossier_script = os.path.dirname(os.path.abspath(__file__))
    chemin_fichier = os.path.join(dossier_script, "hurdat2_1980_2025.csv")
    
    if os.path.exists(chemin_fichier):
        lam, alf, xm = calibrer_parametres_catbond(chemin_fichier)
    else:
        print(f"ERREUR : Le fichier {chemin_fichier} n'a pas été trouvé.")
