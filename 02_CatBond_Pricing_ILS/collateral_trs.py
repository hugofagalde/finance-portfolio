import numpy as np
import pandas as pd

class CollateralManager:
    """
    Simule la gestion du capital d'un SPV et le mécanisme de Total Return Swap (TRS).
    """
    # NOUVEAU : Le taux SOFR est actualisé à 3.64% (0.0364) pour Juin 2026
    def __init__(self, principal_m_usd, months=12, sofr_annual_rate=0.0364, trs_margin_annual=0.0015):
        self.principal = principal_m_usd
        self.months = months
        # Taux SOFR garanti par le Swap
        self.sofr_monthly = sofr_annual_rate / 12  
        
        # La marge de la banque (ex: 15 bps = 0.15% par an)
        self.trs_margin_monthly = trs_margin_annual / 12 
        
        np.random.seed(42)

    def simulate_market_environment(self):
        """
        Simule l'évolution du prix des Bons du Trésor (T-Bills) sur le marché.
        On va simuler un "Krach Obligataire" (baisse des prix due à une hausse des taux).
        """
        # On simule des rendements mensuels volatils (moyenne négative pour simuler une crise)
        t_bill_returns = np.random.normal(loc=-0.002, scale=0.01, size=self.months)
        return t_bill_returns

    def run_trs_simulation(self):
        """
        Calcule les flux financiers mois par mois avec et sans le Swap.
        """
        t_bill_returns = self.simulate_market_environment()
        
        # Suivi des portefeuilles
        valeur_sans_trs = self.principal
        valeur_avec_trs = self.principal
        
        historique = []

        for mois in range(1, self.months + 1):
            rendement_marche = t_bill_returns[mois-1]
            
            # ---------------------------------------------------------
            # SCÉNARIO 1 : GESTION NAÏVE (SANS TRS)
            # Le SPV subit de plein fouet les fluctuations du marché.
            # ---------------------------------------------------------
            perte_ou_gain_marche = valeur_sans_trs * rendement_marche
            valeur_sans_trs += perte_ou_gain_marche
            
            # ---------------------------------------------------------
            # SCÉNARIO 2 : GESTION COUVERTE (AVEC TRS)
            # Le SPV échange la performance du marché contre le taux SOFR garanti.
            # ---------------------------------------------------------
            # 1. Le SPV gagne le rendement du marché sur ses Bons du Trésor
            flux_marche = valeur_avec_trs * rendement_marche
            
            # 2. MECANIQUE DU SWAP : 
            # Le SPV "donne" ce flux_marche à la Banque.
            flux_paye_a_banque = flux_marche
            
            # La Banque "donne" le taux SOFR au SPV... mais soustrait sa Marge !
            flux_recu_de_banque = valeur_avec_trs * (self.sofr_monthly - self.trs_margin_monthly)
            
            # Calcul du profit brut de la banque sur ce mois
            profit_banque_mois = valeur_avec_trs * self.trs_margin_monthly
            
            # 3. Bilan pour le SPV avec TRS
            # Valeur = Valeur_Initiale + Ce que le marché a donné - Ce qu'on donne à la banque + Ce que la banque nous donne
            valeur_avec_trs = valeur_avec_trs + flux_marche - flux_paye_a_banque + flux_recu_de_banque
            
            # Enregistrement pour le Dashboard
            historique.append({
                "Mois": mois,
                "Rendement T-Bill (%)": rendement_marche * 100,
                "Flux TRS Net (M$)": flux_recu_de_banque - flux_paye_a_banque,
                "Bénéfice Banque (M$)": profit_banque_mois,
                "Valeur SPV SANS Swap (M$)": valeur_sans_trs,
                "Valeur SPV AVEC Swap (M$)": valeur_avec_trs
            })

        return pd.DataFrame(historique)

# ==========================================
# EXÉCUTION DE L'ÉTAPE 3
# ==========================================
if __name__ == "__main__":
    print("--- ÉTAPE 3 : MODÉLISATION DU COLLATÉRAL ET DU TRS ---\n")
    
    # On prend l'exemple de la Tranche Junior calculée à l'Étape 2 (ex: 3437 M$)
    capital_initial = 3437.0 
    
    print(f"Capital initial placé dans le SPV : {capital_initial:,.2f} M$")
    print("Mise en place d'un Total Return Swap (TRS) indexé sur le taux SOFR (3.64% annuel - Juin 2026).")
    print("La banque prélève une marge de 15 points de base (0.15% annuel).")
    print("Simulation d'un krach obligataire sur 12 mois...\n")
    
    manager = CollateralManager(principal_m_usd=capital_initial)
    df_simulation = manager.run_trs_simulation()
    
    # Formatage esthétique du tableau pour la console
    format_dict = {
        'Rendement T-Bill (%)': '{:.2f}%',
        'Flux TRS Net (M$)': '{:,.2f}',
        'Bénéfice Banque (M$)': '{:,.2f}',
        'Valeur SPV SANS Swap (M$)': '{:,.2f}',
        'Valeur SPV AVEC Swap (M$)': '{:,.2f}'
    }
    print(df_simulation.style.format(format_dict).to_string())
    
    print("\n--- BILAN FINANCIER À LA FIN DE L'ANNÉE ---")
    valeur_finale_sans = df_simulation['Valeur SPV SANS Swap (M$)'].iloc[-1]
    valeur_finale_avec = df_simulation['Valeur SPV AVEC Swap (M$)'].iloc[-1]
    total_benef_banque = df_simulation['Bénéfice Banque (M$)'].sum()
    
    print(f"Valeur si on n'avait PAS fait de Swap : {valeur_finale_sans:,.2f} M$ "
          f"(Perte de capital : {valeur_finale_sans - capital_initial:,.2f} M$)")
    print(f"Valeur grâce à la couverture du TRS   : {valeur_finale_avec:,.2f} M$ "
          f"(Gain garanti (SOFR - Marge) : {valeur_finale_avec - capital_initial:,.2f} M$)")
    print(f"-> COMMISSION TOTALE ENCAISSÉE PAR LA BANQUE : {total_benef_banque:,.2f} M$")