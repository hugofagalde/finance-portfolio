import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

ticker = ['CLV26.NYM','CLX26.NYM','CLZ26.NYM','CLF27.NYM','CLG27.NYM','CLH27.NYM']
series_list= []
for i in ticker : 
    series_list.append(yf.download(i, start = '2026-01-01')['Close'])
df_curve = pd.concat(series_list, axis=1).dropna()
df_curve.columns = ['F1','F2','F3','F4','F5','F6']

#df_curve['Signal'] = (df_curve['F1']-df_curve['F6'])/((5/12)*df_curve['F1'])
#df_curve['Position'] = np.where(df_curve['Signal'] > 0, 1, -1)
#df_curve['Position_Reelle'] = df_curve['Position'].shift(1)

x = np.arange(1, 7)
def calculer_pente(ligne) :
    coeff  = np.polyfit(x, ligne, deg = 1)
    return coeff[0]

df_curve['Slope'] = df_curve[['F1','F2','F3','F4','F5','F6']].apply(calculer_pente, axis = 1)
df_curve['Position'] = np.where (df_curve['Slope'] < 0, 1, -1)
df_curve['Position_R'] = df_curve['Position'].shift(1)

df_curve['Return_F1'] = df_curve['F1'].pct_change()
df_curve['Return'] = df_curve['Position_R'] * df_curve['Return_F1'] 

df_curve['Cumul_Strat'] = (1 + df_curve['Return'].fillna(0)).cumprod()
df_curve['Cumul_BuyHold'] = (1 + df_curve['Return_F1'].fillna(0)).cumprod()

rendement_moyen = df_curve['Return'].mean() * 252
volatilite = df_curve['Return'].std() * np.sqrt(252)
sharpe_strat = rendement_moyen / volatilite
sharpe_buyhold = (df_curve['Return_F1'].mean() * 252) / (df_curve['Return_F1'].std() * np.sqrt(252))

print("--- RÉSULTATS DU BACKTEST ---")
print(
    f"Rendement Total Stratégie (Term Structure) : {(df_curve['Cumul_Strat'].iloc[-1] - 1) * 100:.2f}%"
)
print(
    f"Rendement Total Buy & Hold (F1)             : {(df_curve['Cumul_BuyHold'].iloc[-1] - 1) * 100:.2f}%"
)
print(f"Sharpe Ratio Annualisé Stratégie                    : {sharpe_strat:.2f}")
print(f"Sharpe Ratio Annualisé Buy & Hold                     : {sharpe_buyhold:.2f}")

plt.figure(figsize=(10, 5))
plt.plot(
    df_curve.index,
    df_curve['Cumul_Strat'],
    label='Stratégie Curve Slope (6M)',
    color='navy',
    lw=1.5,
)
plt.plot(
    df_curve.index,
    df_curve['Cumul_BuyHold'],
    label='Buy & Hold F1',
    color='grey',
    linestyle='--',
)
plt.title('Backtest WTI Term Structure Carry Strategy (Pente 6 Contrats)')
plt.ylabel('Valeur du Portefeuille (Base 1.0)')
plt.legend()
plt.grid(True)
plt.show()



