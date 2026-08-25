import numpy as np
import pandas as pd
import plotly.graph_objects as go

class ALMEngine:
    def __init__(self, num_years=10000, lambda_freq=6.848, alpha=4.3816, xm=96, 
                 v_max=165, power=3.0, tiv_m_usd=5000):
        self.num_years = num_years
        
        self.lambda_freq = lambda_freq  
        self.alpha = alpha              
        self.xm = xm                   
        
        self.v_max = v_max             
        self.power = power       
        self.tiv = tiv_m_usd           
        
        np.random.seed(42)

    def generate_annual_losses(self):
        print(f"Lancement de la simulation de Monte Carlo sur {self.num_years} ans...")
        
        N = np.random.poisson(self.lambda_freq, self.num_years)
        total_events = np.sum(N)
        print(f"-> {total_events} ouragans majeurs simulés au total.")
        
        wind_speeds = self.xm * (np.random.pareto(self.alpha, total_events) + 1)
        
        ratios = np.maximum(wind_speeds - self.xm, 0) / (self.v_max - self.xm)
        ratios = np.minimum(ratios, 1.0) 
        damage_ratios = ratios ** self.power
        
        financial_losses = damage_ratios * self.tiv

        year_indices = np.repeat(np.arange(self.num_years), N)
        annual_losses = np.bincount(year_indices, weights=financial_losses, minlength=self.num_years)

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

    pertes = df_losses[df_losses['Aggregate_Loss_M'] > 0]['Aggregate_Loss_M'].values
    
    pertes_triees = np.sort(pertes)[::-1]
    
    nb_annees = len(df_losses)
    probabilite_depassement = np.arange(1, len(pertes_triees) + 1) / nb_annees
    
    periode_retour = 1 / probabilite_depassement
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=periode_retour, 
        y=pertes_triees, 
        mode='lines', 
        name='AEP Curve',
        line=dict(color='darkblue', width=2)
    ))
    
    for rp in [10, 50, 100, 250]:
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
        xaxis_type="log", 
        template="plotly_white"
    )
    
    fig.show()

if __name__ == "__main__":
    alm = ALMEngine(
        lambda_freq=6.848, 
        alpha=4.3816, 
        xm=96, 
        tiv_m_usd=5000
    )
    
    df_simulations = alm.generate_annual_losses()
    
    print("--- STATISTIQUES DU PORTEFEUILLE ---")
    print(f"Perte Moyenne Annuelle (Expected Loss) : {df_simulations['Aggregate_Loss_M'].mean():.2f} M$")
    print(f"Pire année simulée (Maximum Loss) : {df_simulations['Aggregate_Loss_M'].max():.2f} M$")
    print(f"Pourcentage d'années avec 0$ de perte : {(df_simulations['Aggregate_Loss_M'] == 0).mean() * 100:.2f}%\n")
    
    print("Génération du graphique AEP dans le navigateur...")
    tracer_courbe_ep(df_simulations)
