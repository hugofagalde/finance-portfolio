import numpy as np
import pandas as pd
import plotly.graph_objects as go

class ALMEngine:
    """
    Moteur de Modélisation des Pertes Agrégées (Aggregate Loss Model)
    Utilise une simulation de Monte Carlo vectorisée sur 10 000 ans.
    """
    def __init__(self, num_years=10000, lambda_freq=6.848, alpha=4.3816, xm=96, 
                 v_max=165, power=3.0, tiv_m_usd=5000):
        # Paramètres de simulation
        self.num_years = num_years
        
        # Paramètres Météo (Calibrés sur HURDAT2)
        self.lambda_freq = lambda_freq  # Fréquence (Poisson)
        self.alpha = alpha              # Sévérité (Pareto)
        self.xm = xm                    # Seuil d'attachement météo
        
        # Paramètres Financiers (Fonction de Dommages)
        self.v_max = v_max              # Vitesse de destruction totale
        self.power = power              # Facteur de convexité
        self.tiv = tiv_m_usd            # Total Insured Value (M$)
        
        # Seed pour reproductibilité des tests
        np.random.seed(42)

    def generate_annual_losses(self):
        print(f"Lancement de la simulation de Monte Carlo sur {self.num_years} ans...")
        
        # 1. FRÉQUENCE : Combien d'ouragans par an ?
        N = np.random.poisson(self.lambda_freq, self.num_years)
        total_events = np.sum(N)
        print(f"-> {total_events} ouragans majeurs simulés au total.")
        
        # 2. SÉVÉRITÉ : Quelle vitesse pour chaque ouragan ? (Pareto Type I)
        wind_speeds = self.xm * (np.random.pareto(self.alpha, total_events) + 1)
        
        # 3. VULNÉRABILITÉ : Quel pourcentage de destruction ?
        ratios = np.maximum(wind_speeds - self.xm, 0) / (self.v_max - self.xm)
        ratios = np.minimum(ratios, 1.0) # Plafond à 100%
        damage_ratios = ratios ** self.power
        
        # 4. PERTE FINANCIÈRE : Quel coût par ouragan ?
        financial_losses = damage_ratios * self.tiv
        
        # 5. AGRÉGATION : Somme des pertes pour chaque année
        year_indices = np.repeat(np.arange(self.num_years), N)
        annual_losses = np.bincount(year_indices, weights=financial_losses, minlength=self.num_years)
        
        # Compilation dans un DataFrame
        df_results = pd.DataFrame({
            'Year': np.arange(1, self.num_years + 1),
            'Num_Events': N,
            'Aggregate_Loss_M': annual_losses
        })
        
        print("Simulation terminée avec succès !\n")
        return df_results

def tracer_courbe_ep(df_losses):
    """
    Trace la courbe de probabilité de dépassement (Exceedance Probability Curve).
    Affiche la Perte en fonction de la Période de Retour (Return Period).
    """
    # On extrait les pertes supérieures à 0
    pertes = df_losses[df_losses['Aggregate_Loss_M'] > 0]['Aggregate_Loss_M'].values
    
    # On trie les pertes par ordre décroissant (du pire scénario au plus clément)
    pertes_triees = np.sort(pertes)[::-1]
    
    # Calcul de la probabilité de dépassement pour chaque perte
    # Formule : Rang / Nombre total d'années simulées
    nb_annees = len(df_losses)
    probabilite_depassement = np.arange(1, len(pertes_triees) + 1) / nb_annees
    
    # Période de retour (Return Period) = 1 / Probabilité
    # Ex: Une proba de 0.01 (1%) correspond à un événement "1-in-100 years"
    periode_retour = 1 / probabilite_depassement
    
    # Création du graphique Plotly
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=periode_retour, 
        y=pertes_triees, 
        mode='lines', 
        name='AEP Curve',
        line=dict(color='darkblue', width=2)
    ))
    
    # Repères visuels pour les "Return Periods" standards en finance
    for rp in [10, 50, 100, 250]:
        # Trouver la perte correspondante à cette période de retour
        idx = (np.abs(periode_retour - rp)).argmin()
        perte_rp = pertes_triees[idx]
        
        fig.add_scatter(
            x=[rp], y=[perte_rp], mode='markers+text',
            marker=dict(color='red', size=8),
            text=[f"{rp} ans: {perte_rp:.0f} M$"],
            textposition="top left",
            showlegend=False
        )

    fig.update_layout(
        title="Courbe de Probabilité de Dépassement (AEP Curve)",
        xaxis_title="Période de Retour (Années) - Échelle Logarithmique",
        yaxis_title="Perte Financière Agrégée (Millions $)",
        xaxis_type="log", # Échelle log très importante pour ce type de graphe
        template="plotly_white"
    )
    
    fig.show()

# ==========================================
# EXÉCUTION
# ==========================================
if __name__ == "__main__":
    # 1. Initialisation du moteur avec nos paramètres calculés
    alm = ALMEngine(
        lambda_freq=6.848, 
        alpha=4.3816, 
        xm=96, 
        tiv_m_usd=5000
    )
    
    # 2. Lancement du Monte Carlo
    df_simulations = alm.generate_annual_losses()
    
    # Affichage de quelques statistiques descriptives
    print("--- STATISTIQUES DU PORTEFEUILLE ---")
    print(f"Perte Moyenne Annuelle (Expected Loss) : {df_simulations['Aggregate_Loss_M'].mean():.2f} M$")
    print(f"Pire année simulée (Maximum Loss) : {df_simulations['Aggregate_Loss_M'].max():.2f} M$")
    print(f"Pourcentage d'années avec 0$ de perte : {(df_simulations['Aggregate_Loss_M'] == 0).mean() * 100:.2f}%\n")
    
    # 3. Affichage du graphique professionnel
    print("Génération du graphique AEP dans le navigateur...")
    tracer_courbe_ep(df_simulations)