import pandas as pd

class CatBondPricer:
    def __init__(self, sofr_rate=0.0364, trs_margin=0.0015):
        self.collateral_net_yield = sofr_rate - trs_margin
        self.market_multiple = 2.5

    def price_tranches(self, tranches_data):
        results = []
        for tranche in tranches_data:
            name = tranche['name']
            el = tranche['expected_loss'] 
            spread = el * self.market_multiple
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

if __name__ == "__main__":
    print("--- ÉTAPE 4 : PRICING À L'ÉMISSION (NEW ISSUE PRICING) ---\n")
    
    tranches_spv = [
        {"name": "Tranche Junior (High Yield)", "expected_loss": 0.1156}, # 11.56%
        {"name": "Tranche Mezzanine", "expected_loss": 0.0256},           # 2.56%
        {"name": "Tranche Senior (Safe)", "expected_loss": 0.0040}        # 0.40%
    ]
    
    pricer = CatBondPricer(sofr_rate=0.0364, trs_margin=0.0015)
    
    print("Conditions de marché : Multiple moyen = 2.5x")
    print("Rendement du Collatéral (SOFR net) = 3.49%\n")

    df_pricing = pricer.price_tranches(tranches_spv)

    print(df_pricing.to_string(index=False))
