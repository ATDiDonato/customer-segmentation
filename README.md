# Customer segmentation with clustering

Understanding and serving customers are two of the retail industry's most important strategic marketing objectives. This project explores historical e-commerce purchasing patterns and develops customer segments to inform potential marketing activity.

Developed from an academic customer-segmentation mini-project (Course 1, Week 6), the analysis combines data preparation, feature engineering, clustering diagnostics and business interpretation. The business scenario is illustrative; proposed campaigns require validation.

**[View the customer segmentation notebook](customer_segmentation.ipynb).**

## Source

The supplied reference attributes **CUSTOMERS_CLEAN** to SAS (2024), last revised 15 December 2021. The notebook reads the existing external ZIP from the [FourthRev teaching repository](https://github.com/FourthRevGitHub/CAM_DS_Public-Data-Sets/blob/main/Course%201/Week%206/CUSTOMERS_CLEAN.zip). Raw customer data is not included and no dataset redistribution permissions are asserted.

## Approach

- Review data quality, remove exact duplicate order lines under a stated assumption, and parse financial and date fields.
- Aggregate to five customer features: distinct-order **Frequency**, summed **Observed_Revenue**, unweighted order-line **Avg_Unit_Cost**, **Age** and **Recency**. Customer ID is retained for identification, outside modelling.
- Use `analysis_date = maximum delivery date + 7 days` as a reproducible historical snapshot. The corrected Age calculation is checked for birthdays before, on and after the analysis date.
- Standardise features using StandardScaler in a column transformer and pipeline. Preserve the full-data K-means diagnostics for k=1–10 and silhouettes for k=2–5. Each silhouette mean is derived from one silhouette_samples calculation per k.
- Use **k=3** as a choice balancing diagnostics and business interpretability, with `random_state=42` and `n_init=10`. Describe refreshed segments using counts, percentages, median feature values, box plots and PCA.

## Execution and verified results

The portfolio refresh selectively executed **16 preparation and modelling cells in a fresh kernel**: corrected customer features, full-data k=3 K-means, segment summary, box plots and final PCA. Birthday, input-validity, label-alignment and segment-total checks passed. This was **not a complete clean-kernel Run All execution**.

Saved full-data K-means diagnostics, silhouettes and diagnostic plots were preserved from earlier completed diagnostic cells. Original dendrograms and the **unseeded** t-SNE figure are supplementary outputs from the original analysis; they were not regenerated during this refresh. Their original inputs and settings are explicit in the notebook.

- Source: **951,669 order lines, 20 columns**; removing 21 exact duplicates leaves **951,648 lines**.
- Orders: **1 January 2012–30 December 2016**; historical analysis date: **26 January 2017**.
- Analysis: **68,300 customers, five modelling features**, using all customers throughout.

Preserved full-data diagnostics:

| k | Mean silhouette | Negative fraction |
|---|---:|---:|
| 2 | 0.25925651 | 3.8785% |
| 3 | 0.25145980 | 3.9239% |
| 4 | 0.25183460 | 5.1493% |
| 5 | 0.26546811 | 5.4758% |

k=5 has the highest mean score. These results do not prove k=3 optimal; three segments provide a practical starting point for business interpretation.

Refreshed full-data segment summary:

| Cluster / observed profile | Customers | Share | Median frequency | Median observed revenue | Median unit cost | Median age | Median recency (days) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 / intermediate activity | 39,188 | 57.38% | 9 | 1,407.90 | 71.31 | 43 | 163 |
| 1 / higher activity | 13,851 | 20.28% | 22 | 4,179.45 | 79.77 | 38 | 75 |
| 2 / lower activity, longer recency | 15,261 | 22.34% | 3 | 553.80 | 69.55 | 49 | 951 |

Cluster labels retain their previous interpretation. The refreshed k=3 WCSS is **205,307.28644580**, consistent with the preserved diagnostic table. The first two PCA components explain approximately **65.09%** of scaled feature variance. Financial values are treated as USD following the original source description.

## Limitations

Observed_Revenue covers the dataset period and is not predicted lifetime value. Avg_Unit_Cost is neither quantity-weighted nor a selling price. Recency and Age describe the historical snapshot, not current activity. Exact row deduplication is an assumption. Plausible extreme values remain unverified; K-means and Ward linkage are sensitive to them.

K-means assigns hard labels. Overlap in PCA or t-SNE projections does not imply soft clustering or independently validate segment quality. “Loyal”, “churned”, RETAIN, CULTIVATE and WIN-BACK are hypotheses requiring domain review, subsequent behaviour and controlled campaign evaluation. Stability across seeds and feature choices remains future work. The original supplementary figures do not verify the corrected inputs or a seeded t-SNE run.

## Run locally

Tested with Python 3.12 and the direct dependencies in `requirements.txt`. Internet access is required for the external dataset.

From this directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m ipykernel install --user --name python3 --display-name "Python 3"
.\.venv\Scripts\python execute_notebook.py
```

The runner executes only the preparation, full-data k=3 model, segment summary, box plots and final PCA in a fresh kernel, validates the notebook and saves the refreshed outputs. It preserves the saved diagnostics and original supplementary figures. Kernel registration creates or updates the user kernel named `python3`.

For interactive use, open the final notebook and select the project environment. `RECOMPUTE_DIAGNOSTICS`, `RUN_HIERARCHICAL` and `RUN_TSNE` default to **False**, so Run All skips expensive diagnostics, hierarchical clustering and t-SNE. Enabling a flag is an explicit opt-in using all customers; there is no sampling fallback. The optional t-SNE uses seed 42 and is separate from the saved original unseeded figure. Use the selective runner to refresh outputs while retaining the saved figures.

Local source notebooks, comparison notes and review artifacts are excluded from the public presentation. The report is unchanged and omitted until it matches these results.
