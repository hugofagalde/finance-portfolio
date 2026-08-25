# Quantitative Finance & Systematic Trading Portfolio

Collection of financial engineering models, stochastic risk pricing, and systematic market strategies implemented in Python.

---

## Projects Overview

### 1. Commodity Term Structure – Systematic Carry Strategy
* **Asset Class:** Energy & Commodities (WTI Crude Oil Futures - CME/NYMEX).
* **Core Concept:** Captures the structural risk premium (*roll yield / convenience yield*) across the term structure based on Erb & Harvey (2006).
* **Quantitative Methodology:**
  * Implemented linear regression (`np.polyfit`) across the first 6 active futures contracts ($F_1$ to $F_6$) to estimate the curve slope ($\frac{\partial F}{\partial T}$).
  * Generated dynamic Long/Short signals driven by market regimes (Backwardation vs. Contango).
  * Incorporated 1-day execution lag (`shift(1)`) to strictly prevent look-ahead bias, along with transaction cost and slippage modeling (5 bps per turnover).
* **Performance:** Sharpe Ratio of **1.26** on the multi-month curve backtest.

#### Performance & Regime Analysis
* **Benchmark Comparison:** Over the tested period (Jan to Aug 2026), passive Buy & Hold on F1 generated a raw return of +42.45% (Sharpe 1.55) vs. +32.28% (Sharpe 1.26 net of 5 bps friction) for the systematic strategy.
* **Economic Rationale:** 
  * The underlying commodity experienced a strong, one-way bull market (+42% continuous drift), naturally favoring passive 100% long beta exposure with low relative realized volatility over a short horizon.
  * The systematic Curve Slope strategy trades dynamically based on the term structure slope ($dF/dT$). During flattening or brief curve shift phases, the model reduced net exposure and absorbed rotation costs.
  * While Buy & Hold captures pure unhedged beta in bull runs, it remains fully vulnerable to severe contango regimes and macro downturns (-50%+ drawdowns). The Term Structure strategy delivers an asymmetric profile by systematically shorting contango environments, generating uncorrelated, leveragable alpha across a full commodity cycle.
* **Stack:** Python, Pandas, NumPy, yfinance, Matplotlib.

---

### 2. CatBond-Architect – ILS Structuring & Quantitative Pricing
* **Asset Class:** Insurance-Linked Securities (Catastrophe Bonds / Alternative Risk Transfer).
* **Core Concept:** End-to-end investment banking pipeline for securitizing Atlantic hurricane risk into a 3-tranche Special Purpose Vehicle (SPV).
* **Quantitative Methodology:**
  * Calibrated an Aggregate Loss Model using 45+ years of historical NOAA/HURDAT2 hurricane data.
  * Fitted a Poisson distribution ($\hat{\lambda} = 6.85$) for event frequency and a Pareto distribution via Hill Maximum Likelihood Estimation ($\hat{\alpha} = 4.38$) for extreme tail wind speeds.
  * Executed a vectorized 10,000-year Monte Carlo simulation in NumPy (`np.bincount`, `np.repeat`) to derive the Aggregate Exceedance Probability (AEP) curve.
  * Structured SPV tranches (Junior, Mezzanine, Senior) anchored on Value-at-Risk quantiles VaR 80% to VaR 99.9%.
  * Immunized collateral against interest rate risk via a SOFR Total Return Swap (TRS) with a 15 bps haircut, pricing market spreads with a 2.5x Hard Market multiplier.
* **Stack:** Python, NumPy, SciPy, Matplotlib.

---

## Stack & Dependencies

* **Language:** Python 3.10+
* **Data & Numerical Computing:** `numpy`, `pandas`, `scipy`
* **Market Data & Backtesting:** `yfinance`
* **Visualization:** `matplotlib`, `seaborn`

---

## Author

**Hugo Fagalde**  
* École Centrale de Lille (Engineering) & EDHEC Business School (Master in Management, Finance Track) - Dual Degree (Grad 2029) 
* Background: CPGE MP (Mathematics & Physics)
