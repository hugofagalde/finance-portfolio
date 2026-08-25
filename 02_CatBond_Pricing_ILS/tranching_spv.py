import numpy as np
import pandas as pd

from moteur_alm_monte_carlo import ALMEngine

class Tranche:
    def __init__(self, name, attachment, exhaustion):
        self.name = name
        self.attachment = attachment
        self.exhaustion = exhaustion
        self.principal = exhaustion - attachment

    def calculate_losses(self, aggregate_losses):
        losses = np.minimum(np.maximum(aggregate_losses - self.attachment, 0), self.principal)
        return losses

class SPV:
    def __init__(self, losses_distribution):
        self.losses_dist = losses_distribution
        self.tranches = []

    def add_tranche(self, tranche):
        self.tranches.append(tranche)

    def analyze_structure(self):
        results = []
        for tranche in self.tranches:
            tranche_losses = tranche.calculate_losses(self.losses_dist)
            attachment_prob = np.mean(tranche_losses > 0)
            exhaustion_prob = np.mean(tranche_losses >= (tranche.principal - 1e-5))
            expected_loss = np.mean(tranche_losses) / tranche.principal
            
            results.append({
                'Tranche': tranche.name,
                'Principal (M$)': f"{tranche.principal:,.0f}",
                'Attachement (M$)': f"{tranche.attachment:,.0f}",
                'Épuisement (M$)': f"{tranche.exhaustion:,.0f}",
                'Prob. Attachement': f"{attachment_prob*100:.2f}%",
                'Prob. Épuisement': f"{exhaustion_prob*100:.2f}%",
                'Expected Loss (EL)': f"{expected_loss*100:.2f}%"
            })
            
        return pd.DataFrame(results)

if __name__ == "__main__":
    print("--- DÉMARRAGE DE L'ÉTAPE 2 : STRUCTURATION ---")
    
    print("1. Appel du moteur ALM de l'Étape 1...")
    alm = ALMEngine(lambda_freq=6.848, alpha=4.3816, xm=96, tiv_m_usd=5000)
    annual_losses = alm.generate_annual_losses()
    
    var_80 = np.percentile(annual_losses, 80)
    var_95 = np.percentile(annual_losses, 95)
    var_99 = np.percentile(annual_losses, 99)
    var_99_9 = np.percentile(annual_losses, 99.9)
    
    print("2. Création du SPV et découpe des tranches (Tranching)...")
    spv = SPV(annual_losses)
    
    spv.add_tranche(Tranche("Junior (High Yield)", var_80, var_95))
    spv.add_tranche(Tranche("Mezzanine", var_95, var_99))
    spv.add_tranche(Tranche("Senior (Safe)", var_99, var_99_9))
    
    print("3. Rapport de Structuration (Metrics pour le Pricing) :\n")
    df_report = spv.analyze_structure()
    print(df_report.to_string(index=False))
