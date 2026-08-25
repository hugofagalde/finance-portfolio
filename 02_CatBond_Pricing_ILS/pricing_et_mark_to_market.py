import pandas as pd

class CatBondPricer:
    """
    Module de valorisation à l'émission pour un Cat Bond.
    Calcule le rendement total exigé par les investisseurs pour chaque tranche.
    """
    def __init__(self, sofr_rate=0.0364, trs_margin=0.0015):
        # 1. Le socle "Sans Risque" (issu de l'Étape 3)
        self.collateral_net_yield = sofr_rate - trs_margin
        
        # 2. Conditions de marché actuelles (Le Multiple)
        # Un multiple de 2.5 signifie que les investisseurs exigent 
        # 2.5 fois l'Expected Loss en prime de risque.
        self.market_multiple = 2.5

    def price_tranches(self, tranches_data):
        """
        Calcule le Spread et le Rendement Total pour une liste de tranches.
        """
        results = []
        for tranche in tranches_data:
            name = tranche['name']
            el = tranche['expected_loss'] # Expected Loss en décimal
            
            # Calcul de la Prime de Risque (Spread)
            # Formule : Spread = EL * Multiple de Marché
            spread = el * self.market_multiple
            
            # Calcul du Rendement Total pour l'investisseur
            total_yield = self.collateral_net_yield + spread
            
            results.append({
                "Tranche": name,
                "Expected Loss (EL)": f"{el * 100:.2f}%",
                "Multiple de Marché": f"{self.market_multiple}x",
                "Spread (Payé par l'Assureur)": f"{spread * 100:.2f}%",
                "Rendement TRS (Collatéral)": f"{self.collateral_net_yield * 100:.2f}%",
                "RENDEMENT TOTAL INVESTISSEUR": f"{total_yield * 100:.2f}%"
            })
            
        return pd.DataFrame(results)

# ==========================================
# EXÉCUTION DE L'ÉTAPE 4
# ==========================================
if __name__ == "__main__":
    print("--- ÉTAPE 4 : PRICING À L'ÉMISSION (NEW ISSUE PRICING) ---\n")
    
    # 1. On récupère les Expected Loss (EL) calculés à l'Étape 2
    # J'ai repris tes chiffres exacts de ta capture d'écran !
    tranches_spv = [
        {"name": "Tranche Junior (High Yield)", "expected_loss": 0.1156}, # 11.56%
        {"name": "Tranche Mezzanine", "expected_loss": 0.0256},           # 2.56%
        {"name": "Tranche Senior (Safe)", "expected_loss": 0.0040}        # 0.40%
    ]
    
    # 2. Initialisation du Pricer avec les taux de Juin 2026 (Étape 3)
    # SOFR = 3.64%, Marge = 0.15%
    pricer = CatBondPricer(sofr_rate=0.0364, trs_margin=0.0015)
    
    print("Conditions de marché : Multiple moyen = 2.5x")
    print("Rendement du Collatéral (SOFR net) = 3.49%\n")
    
    # 3. Calcul du prix de vente
    df_pricing = pricer.price_tranches(tranches_spv)
    
    # Affichage propre dans la console
    print(df_pricing.to_string(index=False))