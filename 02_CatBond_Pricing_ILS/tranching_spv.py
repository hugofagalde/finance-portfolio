import numpy as np
import pandas as pd

# ==========================================
# CONNEXION AVEC L'ÉTAPE 1
# ==========================================
# On importe ta classe ALMEngine depuis ton fichier de l'Étape 1.
# (Assure-toi que ton fichier de l'étape 1 est bien nommé 'alm_monte_carlo.py')
from moteur_alm_monte_carlo import ALMEngine

# ==========================================
# 2. LES CLASSES DU VÉHICULE FINANCIER (SPV)
# ==========================================
class Tranche:
    def __init__(self, name, attachment, exhaustion):
        self.name = name
        self.attachment = attachment
        self.exhaustion = exhaustion
        self.principal = exhaustion - attachment

    def calculate_losses(self, aggregate_losses):
        """
        Applique la formule mathématique du Waterfall vectorisée.
        Perte = min(max(Perte_Totale - Attachement, 0), Principal)
        """
        losses = np.minimum(np.maximum(aggregate_losses - self.attachment, 0), self.principal)
        return losses

class SPV:
    def __init__(self, losses_distribution):
        self.losses_dist = losses_distribution
        self.tranches = []

    def add_tranche(self, tranche):
        self.tranches.append(tranche)

    def analyze_structure(self):
        """
        Calcule les métriques clés pour chaque tranche pour le marché secondaire.
        """
        results = []
        for tranche in self.tranches:
            tranche_losses = tranche.calculate_losses(self.losses_dist)
            
            # Probabilité que la perte de la tranche soit > 0
            attachment_prob = np.mean(tranche_losses > 0)
            
            # Probabilité que la perte soit égale au Principal (Tranche détruite)
            exhaustion_prob = np.mean(tranche_losses >= (tranche.principal - 1e-5))
            
            # Expected Loss (EL) : Perte moyenne / Principal
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

# ==========================================
# 3. EXÉCUTION DE L'ÉTAPE 2
# ==========================================
if __name__ == "__main__":
    print("--- DÉMARRAGE DE L'ÉTAPE 2 : STRUCTURATION ---")
    
    # 1. On appelle TON moteur de l'Étape 1 en tâche de fond
    print("1. Appel du moteur ALM de l'Étape 1...")
    alm = ALMEngine(lambda_freq=6.848, alpha=4.3816, xm=96, tiv_m_usd=5000)
    annual_losses = alm.generate_annual_losses()
    
    # 2. Calcul des quantiles (Value at Risk) pour structurer le SPV
    var_80 = np.percentile(annual_losses, 80)
    var_95 = np.percentile(annual_losses, 95)
    var_99 = np.percentile(annual_losses, 99)
    var_99_9 = np.percentile(annual_losses, 99.9)
    
    print("2. Création du SPV et découpe des tranches (Tranching)...")
    spv = SPV(annual_losses)
    
    # On ancre nos tranches sur les mathématiques du risque (VaR)
    spv.add_tranche(Tranche("Junior (High Yield)", var_80, var_95))
    spv.add_tranche(Tranche("Mezzanine", var_95, var_99))
    spv.add_tranche(Tranche("Senior (Safe)", var_99, var_99_9))
    
    print("3. Rapport de Structuration (Metrics pour le Pricing) :\n")
    df_report = spv.analyze_structure()
    print(df_report.to_string(index=False))