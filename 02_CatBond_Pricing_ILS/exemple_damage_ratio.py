import numpy as np
import pandas as pd
import plotly.graph_objects as go

def calculer_damage_ratio(v, xm=96, v_max=165, power=3.0):
    """
    Calcule le Taux de Destruction (Damage Ratio) en fonction de la vitesse du vent.
    - xm : Seuil de déclenchement (96 noeuds)
    - v_max : Destruction totale (165 noeuds)
    - power : Facteur de non-linéarité (3.0 pour l'effet cubique)
    """
    # 1. On ignore tout ce qui est sous le seuil xm (max avec 0)
    ratio = np.maximum(v - xm, 0) / (v_max - xm)
    
    # 2. On plafonne la destruction à 100% (min avec 1)
    ratio = np.minimum(ratio, 1.0)
    
    # 3. On applique la puissance cubique
    return ratio ** power

# ==========================================
# 1. TABLEAU D'EXEMPLES CONCRETS
# ==========================================
# Différents scénarios de vents (en noeuds)
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

# Calcul des ratios
ratios = calculer_damage_ratio(vents_exemples)

# Calcul des pertes financières (Pour un TIV de 5 Milliards $)
tiv_m_usd = 5000
pertes_financieres = ratios * tiv_m_usd

# Affichage propre dans la console
df_exemples = pd.DataFrame({
    "Vitesse du Vent (noeuds)": vents_exemples,
    "Sévérité": categories,
    "Taux de Destruction (%)": np.round(ratios * 100, 2),
    "Perte Financière (M$)": np.round(pertes_financieres, 1)
})

print("--- EXEMPLES DE LA FONCTION DE DOMMAGES (TIV = 5 Milliards $) ---")
print(df_exemples.to_string(index=False))

# ==========================================
# 2. VISUALISATION INTERACTIVE AVEC PLOTLY
# ==========================================
# On génère un vecteur de vents continus de 50 à 180 noeuds pour tracer la courbe
vents_continus = np.linspace(50, 180, 500)
ratios_continus = calculer_damage_ratio(vents_continus)

# Création du graphique Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=vents_continus, 
    y=ratios_continus * 100, 
    mode='lines', 
    name='Damage Ratio (k=3)',
    line=dict(color='firebrick', width=3)
))

# Ajout de repères visuels pour comprendre les seuils
fig.add_vline(x=96, line_dash="dash", line_color="green", annotation_text="Seuil d'attachement (96 noeuds)")
fig.add_vline(x=165, line_dash="dash", line_color="red", annotation_text="Destruction Totale (165 noeuds)")

fig.update_layout(
    title="Courbe de Vulnérabilité d'un Portefeuille (Vulnerability Curve)",
    xaxis_title="Vitesse Maximale des Vents (noeuds)",
    yaxis_title="Taux de Destruction (%)",
    template="plotly_white",
    hovermode="x unified"
)

# Ouvre le graphique dans ton navigateur web
fig.show()