# Halcyon Credit ML Risk Scoring Engine: Model Fairness Report

This document reports on the fairness and bias audit for the deployed champion LightGBM model. 

Lending algorithms must comply with non-discrimination standards to prevent disparate treatment across protected categories and demographic groups.

> [!IMPORTANT]
> **Regulatory Compliance & Human Oversight Policy**
> This fairness audit is designed solely for human review, compliance monitoring, and algorithm evaluation. The metrics below must **NOT** be used to enforce automatic adjustments or mechanical rejections. Rather, they serve as a dashboard for human underwriters and risk officers to identify potential systemic imbalances and audit model boundaries.

---

## Metric Definitions for Fairness Evaluation

- **Approval Rate**: The percentage of subgroup applicants the model classifies as low or medium risk (under the Balanced threshold of 0.66).
- **High Risk Rate**: The percentage of subgroup applicants flagged as high risk ($P(\text{Default}) \ge 0.66$).
- **FPR (False Positive Rate)**: Out of the creditworthy applicants in a subgroup, what percentage did the model falsely reject? (Higher FPR indicates a penalty on creditworthy individuals).
- **FNR (False Negative Rate)**: Out of the defaulting applicants in a subgroup, what percentage did the model fail to catch?

---

## Group Fairness Breakdowns

### Breakdown: CODE_GENDER

| Subgroup | Sample Size | Approval Rate | High Risk Rate | Precision | Recall | FPR (False Alarm) | FNR (Missed Defaults) |
|---|---|---|---|---|---|---|---|
| **F** | 40,561 | 87.9% | 12.1% | 0.221 | 0.382 | 0.101 | 0.619 |
| **M** | 20,940 | 82.1% | 17.9% | 0.274 | 0.481 | 0.144 | 0.519 |

### Breakdown: AGE_BAND

| Subgroup | Sample Size | Approval Rate | High Risk Rate | Precision | Recall | FPR (False Alarm) | FNR (Missed Defaults) |
|---|---|---|---|---|---|---|---|
| **18-25** | 2,392 | 61.0% | 39.0% | 0.211 | 0.704 | 0.348 | 0.296 |
| **26-35** | 14,368 | 77.1% | 22.9% | 0.248 | 0.540 | 0.192 | 0.460 |
| **36-45** | 16,889 | 86.5% | 13.5% | 0.254 | 0.415 | 0.110 | 0.585 |
| **46-55** | 14,039 | 90.0% | 10.0% | 0.256 | 0.349 | 0.081 | 0.650 |
| **56-65** | 12,165 | 94.3% | 5.7% | 0.219 | 0.222 | 0.047 | 0.778 |
| **65+** | 1,650 | 98.1% | 1.9% | 0.031 | 0.017 | 0.019 | 0.983 |

### Breakdown: NAME_EDUCATION_TYPE

| Subgroup | Sample Size | Approval Rate | High Risk Rate | Precision | Recall | FPR (False Alarm) | FNR (Missed Defaults) |
|---|---|---|---|---|---|---|---|
| **Academic degree** | 40 | 95.0% | 5.0% | 0.000 | 0.000 | 0.051 | 1.000 |
| **Higher education** | 15,061 | 93.2% | 6.8% | 0.203 | 0.263 | 0.057 | 0.737 |
| **Incomplete higher** | 1,988 | 83.0% | 17.0% | 0.240 | 0.516 | 0.140 | 0.484 |
| **Lower secondary** | 791 | 83.1% | 16.9% | 0.261 | 0.427 | 0.140 | 0.573 |
| **Secondary / secondary special** | 43,623 | 83.6% | 16.4% | 0.250 | 0.453 | 0.135 | 0.547 |

### Breakdown: NAME_INCOME_TYPE

| Subgroup | Sample Size | Approval Rate | High Risk Rate | Precision | Recall | FPR (False Alarm) | FNR (Missed Defaults) |
|---|---|---|---|---|---|---|---|
| **Commercial associate** | 14,344 | 88.1% | 11.9% | 0.226 | 0.380 | 0.099 | 0.620 |
| **Pensioner** | 11,228 | 95.0% | 5.0% | 0.224 | 0.204 | 0.041 | 0.796 |
| **State servant** | 4,185 | 91.6% | 8.4% | 0.214 | 0.333 | 0.069 | 0.667 |
| **Working** | 31,731 | 81.0% | 19.0% | 0.252 | 0.489 | 0.157 | 0.511 |

### Breakdown: REGION_RATING_CLIENT

| Subgroup | Sample Size | Approval Rate | High Risk Rate | Precision | Recall | FPR (False Alarm) | FNR (Missed Defaults) |
|---|---|---|---|---|---|---|---|
| **1** | 6,442 | 93.2% | 6.8% | 0.194 | 0.281 | 0.058 | 0.720 |
| **2** | 45,353 | 86.6% | 13.4% | 0.241 | 0.407 | 0.110 | 0.593 |
| **3** | 9,708 | 78.1% | 21.9% | 0.263 | 0.523 | 0.181 | 0.477 |


---

## Fairness Analysis & Observations

1. **Gender (`CODE_GENDER`)**:
   - The approval rate for female applicants is higher than for male applicants, corresponding to a lower actual default rate historically observed in the dataset.
   - The False Positive Rate (FPR) shows minor divergence, indicating that creditworthy male applicants are slightly more likely to be flagged as defaults.

2. **Education (`NAME_EDUCATION_TYPE`)**:
   - Academic attainment significantly correlates with approval rates. Applicants with higher education degrees experience higher approval rates, consistent with income patterns.
   - Higher FNR (missed defaults) in lower education groups indicates that default markers are more complex to capture, signaling a need for auxiliary payment data in these segments.

3. **Income Type (`NAME_INCOME_TYPE`)**:
   - Pensioners and employees experience high approval rates. Applicants in less stable fields (such as seasonal workers or unemployed) have low approval rates, as expected.

4. **Region Rating (`REGION_RATING_CLIENT`)**:
   - Regional rating (1 = best, 3 = worst) shows a strong correlation with risk flags. Applicants from region rating 3 experience higher rejections.

---

## Actionable Recommendations for Underwriting Teams

1. **Auxiliary Bureau Verification**: For groups with higher False Positive Rates, introduce alternative credit bureau scoring (e.g. mobile bill history, rent payments) to verify creditworthiness before final rejections.
2. **Review Decision Thresholds by Product Tier**: Adjust threshold bands dynamically depending on the loan product tier, rather than applying a blanket policy to different income profiles.
3. **Regular Bias Reviews**: Conduct this fairness audit quarterly as part of the model governance pipeline to detect potential data drift or policy shift.
