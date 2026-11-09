# Quantitative Finance Portfolio

Collection of my finance/financial engineering projects, exploring different markets, asset classes and methodologies.

---

## 1. Battery Storage Arbitrage – France vs Germany (2019–2025)

**Asset Class:** Power (European day-ahead electricity markets)

**Core Concept:** Why does a battery earn less in France than in Germany, and how has the gap evolved since 2019? Simulation of a 1 MW / 2 MWh battery trading on the day-ahead market, and analysis of what drives the difference between the two countries.

**Quantitative Methodology:**
- Solved a daily linear optimisation problem (SciPy, HiGHS) on 7 years of hourly EPEX day-ahead prices, with a degradation cost scaled each year on BloombergNEF battery prices and a sensitivity analysis.
- Ran a regression of daily battery revenues on the generation mix (solar, wind, nuclear) and the European gas price, with Newey-West standard errors.
- A battery consistently earns more in Germany than in France, by 26% to 74% depending on the year. The main difference comes from the evening: Germany relies on gas plants, while France still has a large amount of cheap nuclear power.

**Stack:** Python, pandas, NumPy, SciPy, statsmodels, Matplotlib

---

## 2. Cat Bond – ILS Structuring & Quantitative Pricing

**Asset Class:** Insurance-Linked Securities (Catastrophe Bonds / Alternative Risk Transfer)

**Core Concept:** End-to-end investment banking pipeline for securitizing Atlantic hurricane risk into a 3-tranche Special Purpose Vehicle (SPV).

**Quantitative Methodology:**
- Calibrated an Aggregate Loss Model on 46 years of NOAA/HURDAT2 hurricane data: Poisson frequency of major hurricanes ($\hat{\lambda} = 2.91$), Pareto tail via Hill MLE ($\hat{\alpha} = 4.38$), and a landfall-based probability of hitting the portfolio.
- Ran a vectorized 10,000-year Monte Carlo simulation to derive the Aggregate Exceedance Probability (AEP) curve, and structured Junior, Mezzanine and Senior tranches anchored on VaR quantiles.
- Immunized collateral against interest rate risk via a SOFR Total Return Swap, pricing market spreads with a 2.5x Hard Market multiplier.

**Stack:** Python, NumPy, pandas, Matplotlib

---

## Stack & Dependencies

- **Language:** Python 3.10+
- **Data & Numerical Computing:** numpy, pandas, scipy, statsmodels
- **Data sources:** NOAA/HURDAT2, Energy-Charts API (Fraunhofer ISE), FRED
- **Visualization:** matplotlib

## Author

**Hugo Fagalde**

École Centrale de Lille (Engineering) & EDHEC Business School (Master in Management, Finance Track) – Dual Degree (Grad 2029)

Background: CPGE MP (Mathematics & Physics)
