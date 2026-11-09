# Quantitative Finance Portfolio

Collection of financial engineering models, stochastic risk pricing, and systematic market strategies implemented in Python.

---

### 1. Cat Bond – ILS Structuring & Quantitative Pricing
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
