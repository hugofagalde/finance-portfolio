import numpy as np
import pandas as pd
import plotly.graph_objects as go

def calculer_damage_ratio(v, xm=96, v_max=165, power=3.0):
    ratio = np.maximum(v - xm, 0) / (v_max - xm)

    ratio = np.minimum(ratio, 1.0)

    return ratio ** power
    
vents_exemples = np.array([85, 96, 110, 130, 145, 160, 165, 180])
categories = [
    "Catégorie 2 (Sans danger)", 
    "Catégorie 3 (Seuil d'attachement)", 
    "Catégorie 3 fort", 
    "Catégorie 4 (Ouragan majeur)", 
    "Catégorie 4 extrême", 
    "Catégorie 5 (Dévastateur)", 
    "Catégorie 5+ (Destruction totale)", 
    "Cataclysme absolu"
]

ratios = calculer_damage_ratio(vents_exemples)

tiv_m_usd = 5000
pertes_financieres = ratios * tiv_m_usd

df_exemples = pd.DataFrame({
    "Vitesse du Vent (noeuds)": vents_exemples,
    "Sévérité": categories,
    "Taux de Destruction (%)": np.round(ratios * 100, 2),
    "Perte Financière (M$)": np.round(pertes_financieres, 1)
})

print("--- EXEMPLES DE LA FONCTION DE DOMMAGES (TIV = 5 Milliards $) ---")
print(df_exemples.to_string(index=False))

vents_continus = np.linspace(50, 180, 500)
ratios_continus = calculer_damage_ratio(vents_continus)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=vents_continus, 
    y=ratios_continus * 100, 
    mode='lines', 
    name='Damage Ratio (k=3)',
    line=dict(color='firebrick', width=3)
))

fig.add_vline(x=96, line_dash="dash", line_color="green", annotation_text="Seuil d'attachement (96 noeuds)")
fig.add_vline(x=165, line_dash="dash", line_color="red", annotation_text="Destruction Totale (165 noeuds)")

fig.update_layout(
    title="Courbe de Vulnérabilité d'un Portefeuille (Vulnerability Curve)",
    xaxis_title="Vitesse Maximale des Vents (noeuds)",
    yaxis_title="Taux de Destruction (%)",
    template="plotly_white",
    hovermode="x unified"
)

fig.show()
