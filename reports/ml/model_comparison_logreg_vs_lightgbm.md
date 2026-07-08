# Model Comparison: Baseline Logistic Regression vs. LightGBM Challenger

This report compares the performance of the baseline Logistic Regression model (v1) and the LightGBM challenger model (v1) on the Home Credit Default Risk dataset using identical datasets and preprocessing features.

## Side-by-Side Performance Comparison

| Metric | Baseline (Logistic Regression v1) | Challenger (LightGBM v1) | Delta (Challenger - Baseline) | Business Impact |
|---|---|---|---|---|
| **ROC-AUC** | 0.7415 | **0.7575** | **+0.0160** | **Significant improvement** in risk ranking. |
| **Accuracy** | 0.6856 | **0.7007** | **+0.0151** | Overall predictive accuracy increased. |
| **Precision** | 0.1577 | **0.1667** | **+0.0090** | **Fewer false alarms**; fewer good clients rejected. |
| **Recall** | 0.6669 | **0.6773** | **+0.0105** | Intercepts more defaulting loan applications. |
| **F1-Score** | 0.2551 | **0.2676** | **+0.0125** | Better harmonic balance of risk metrics. |

### Confusion Matrix Delta

| Prediction Category | Baseline (LogReg v1) | Challenger (LightGBM v1) | Count Delta | Business Impact |
|---|---|---|---|---|
| **True Negatives (TN)** | 38,855 | 39,731 | **+876** | Correctly approved more creditworthy applications. |
| **False Positives (FP)** | 17,683 | 16,807 | **-876** | Reduced false alarms (fewer lost clients). |
| **False Negatives (FN)** | 1,654 | 1,602 | **-52** | Reduced toxic leakage (fewer unpaid defaults). |
| **True Positives (TP)** | 3,311 | 3,363 | **+52** | Intercepted more defaults. |

---

## Performance Analysis & Insights

1. **ROC-AUC Performance**:
   - The LightGBM model achieves a ROC-AUC of **0.7575**, outperforming the Logistic Regression baseline by **0.0160**.
   - Because gradient boosted trees model non-linear boundaries natively, LightGBM handles non-linear feature interactions (such as the interaction between `EXT_SOURCE` fields and financial ratios) far better than the baseline linear regression.

2. **Precision and Recall Trade-off**:
   - LightGBM increases **Precision** by **+0.0090** and increases **Recall** by **+0.0105**.
   - In most business cases, moving one metric compromises the other. However, because LightGBM has greater overall discriminative power, it shifts the entire frontier outward, resulting in a simultaneous increase in both the capture rate (Recall) and the efficiency rate (Precision).

3. **Financial Impact**:
   - By switching to LightGBM, the credit team blocks more default events (FN decreased), saving major default capital, and approves more creditworthy candidates (FP decreased), securing extra interest margins.

---

## Recommendation
Based on the metrics, the **LightGBM v1 challenger model is recommended to replace the Logistic Regression model** as the active champion model in the Halcyon Credit Risk Scoring Engine.
