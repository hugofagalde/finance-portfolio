# Cat Bond – ILS Structuring & Quantitative Pricing

**How would an investment bank structure and price a catastrophe bond on Atlantic hurricane risk?**

In this project, I tried to put myself in the shoes of an arranger in an investment bank and to cover the whole pipeline of a Cat Bond: from raw NOAA hurricane data to the yield paid to investors, for an insured portfolio of 5 billion dollars exposed to major hurricanes.

📓 Code: [`02_CatBond_Pricing_ILS.ipynb`](02_CatBond_Pricing_ILS.ipynb)

## Key results

| Tranche | Principal (M$) | Expected Loss | Spread (2.5x EL) | Total investor yield |
|---|---:|---:|---:|---:|
| Junior | 331 | 12.7% | 31.8% | 35.3% |
| Mezzanine | 1,499 | 6.7% | 16.6% | 20.1% |
| Senior | 3,161 | 3.9% | 9.7% | 13.2% |

- Expected annual loss of the portfolio: 267 M$, i.e. 5.3% of the Total Insured Value.
- A yield above 30% on the Junior tranche is not a mathematical anomaly, but the compensation for a risk of losing a large part of the capital in one year out of five.

## Method

1. **Loss model**: calibrated on 46 years of NOAA HURDAT2 data (1980–2025). Poisson frequency of major hurricanes ($\hat{\lambda} = 2.91$ per year), Pareto severity of wind speeds via the Hill / MLE estimator ($\hat{\alpha} = 4.38$), a hit probability based on US major landfalls, and a cubic vulnerability curve.
2. **Monte Carlo simulation**: 10,000 years simulated with NumPy vectorisation (`np.bincount`, `np.repeat`), giving the Aggregate Exceedance Probability (AEP) curve.
3. **Structuring**: three tranches inside a Special Purpose Vehicle (SPV), anchored on the VaR of the simulated losses.
4. **Collateral**: a Total Return Swap paying SOFR − 15 bps protects the capital of the SPV against interest rate risk.
5. **Pricing**: spread = Expected Loss × a 2.5x hard market multiple, plus the collateral yield (3.49%).

## Limitations

- Every major US landfall is assumed to hit the whole portfolio, and we use the maximum wind speed of each hurricane rather than its wind speed at landfall: our losses are conservative.
- The total destruction at 165 knots makes the upper tranches riskier than real Senior cat bond tranches.
- A single market multiple is used for all tranches.

## How to run

```bash
pip install numpy pandas matplotlib
jupyter notebook 02_CatBond_Pricing_ILS.ipynb
```

The parsed HURDAT2 data is included (`hurdat2_1980_2025.csv`). If the file is missing, the notebook downloads and parses the raw file from the NOAA website.

## Data

[NOAA National Hurricane Center – HURDAT2](https://www.nhc.noaa.gov/data/#hurdat) · NOAA NCEI for the frequency of major US landfalls

---
Hugo Fagalde — Centrale Lille × EDHEC Business School
