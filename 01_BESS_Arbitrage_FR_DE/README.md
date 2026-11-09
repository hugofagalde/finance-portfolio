# The Value of Power Flexibility: Battery Day-Ahead Arbitrage, France vs Germany (2019–2025)

**Why does a battery earn less in France than in Germany, and how has the gap evolved since 2019?**

We simulate a 1 MW / 2 MWh battery that trades on the day-ahead market. For each day, we solve a linear optimisation problem under constraints: knowing the hourly prices, the battery chooses when to charge and discharge in order to maximise its daily profit, net of a degradation cost.

📄 Full report: [`BESS_Optimisation.pdf`](BESS_Optimisation.pdf) · 📓 Code: [`01_BESS_Arbitrage_FR_DE.ipynb`](01_BESS_Arbitrage_FR_DE.ipynb)

## Key results

- Between 2019 and 2025, day-ahead arbitrage revenues rose more than ten times in both countries: flexibility has become much more valuable on both sides of the border.
- A battery consistently earns more in Germany than in France, by 26% to 74% depending on the year, and this result holds for every value of the degradation cost we tested.
- The reason behind this gap is not only solar power. The main difference comes from the evening: when the sun sets, Germany relies on gas plants, which set a high price, while France still has a large amount of cheap nuclear power that keeps its prices low.

| Year | France (k€/MW) | Germany (k€/MW) | DE/FR ratio |
|------|------:|------:|-----:|
| 2019 | 3.5  | 5.7  | 1.63 |
| 2022 | 69.2 | 92.2 | 1.33 |
| 2025 | 48.4 | 68.6 | 1.42 |

## Method

- Linear optimisation of the battery with `scipy.optimize.linprog` (HiGHS)
- Degradation cost scaled each year with BloombergNEF battery pack prices, with a sensitivity analysis
- Regression of daily battery revenues on the generation mix (solar, wind, nuclear) and the European gas price

Perfect foresight, price taker, day-ahead market only: our revenues show part of what a real battery can earn. See the report for the full limitations.

## Data

[Energy-Charts](https://www.energy-charts.info) (Fraunhofer ISE) for day-ahead prices and generation · [FRED](https://fred.stlouisfed.org/series/PNGASEUUSDM) for the European gas price · BloombergNEF for battery prices

## How to run

```bash
pip install requests pandas numpy scipy statsmodels matplotlib
jupyter notebook 01_BESS_Arbitrage_FR_DE.ipynb
```

Data are downloaded month by month and cached locally in `data_cache/`, so the first run takes a few minutes.

---
Hugo Fagalde — Centrale Lille × EDHEC Business School
