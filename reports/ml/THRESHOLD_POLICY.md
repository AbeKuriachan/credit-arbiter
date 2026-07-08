# Halcyon Credit ML Risk Scoring Engine: Decision Threshold Policy

This document establishes the official decision threshold policy for classification of credit risk using the LightGBM champion model. 

The champion pipeline is designed to output a raw continuous probability of default ($P(\text{Default})$). The final credit decision (Approve vs. Reject) is governed by a configurable decision threshold ($T$), where:
- $\text{Decision} = \text{Reject}$ if $P(\text{Default}) \ge T$
- $\text{Decision} = \text{Approve}$ if $P(\text{Default}) < T$

---

## Business Decision Policies

Depending on macroeconomic conditions, risk tolerance, and customer acquisition targets, the credit risk committee can adopt one of three predefined policy thresholds:

### 1. Conservative Policy (High Recall)
- **Threshold ($T$)**: **0.36**
- **Recall**: 85.38%
- **Precision**: 12.49%
- **F1-Score**: 0.2179
- **False Negatives (Toxic Loans Approved)**: 726 (Intercepted 4,239 out of 4,965 defaults)
- **False Positives (Good Clients Rejected)**: 29,704
- **Use Case**: Recommended during economic contractions, high-interest-rate environments, or for high-risk credit tiers where the cost of write-offs is extremely high. This policy minimizes toxic defaults at the expense of loan volumes.

### 2. Balanced Policy (Best F1-Score)
- **Threshold ($T$)**: **0.67**
- **Recall**: 40.68%
- **Precision**: 25.17%
- **F1-Score**: 0.3110
- **False Negatives**: 2,945
- **False Positives**: 6,005
- **Use Case**: Recommended for standard, day-to-day credit scoring. It achieves the mathematically optimal compromise between customer acquisition and write-off prevention.

### 3. Revenue-Friendly Policy (Fewer False Positives)
- **Threshold ($T$)**: **0.74**
- **Recall**: 26.08%
- **Precision**: 31.40%
- **F1-Score**: 0.2850
- **False Negatives**: 3,670
- **False Positives**: 2,829 (Reduces rejections of good clients to **2,829**)
- **Use Case**: Recommended during economic growth periods or when launching marketing campaigns to rapidly grow market share. This policy maximizes approval rates and customer acquisition, accepting higher write-off rates.

---

## Comparison Table of Policies

| Policy | Threshold | Recall | Precision | F1-Score | Approved Defaults (FN) | Rejected Good Clients (FP) |
|---|---|---|---|---|---|---|
| **Conservative** | 0.36 | 85.4% | 12.5% | 0.2179 | **726** | 29,704 |
| **Balanced** | 0.67 | 40.7% | 25.2% | 0.3110 | 2,945 | 6,005 |
| **Revenue-Friendly** | 0.74 | 26.1% | 31.4% | 0.2850 | 3,670 | **2,829** |

---

## Architectural Implementation Guidance

### Configurable Inference API
To prevent threshold hardcoding, the prediction engine must not return hardcoded binary predictions. Rather, the inference client should load the threshold dynamically from a central config file or request payload:

```python
# Recommended API Client Implementation Pattern
def make_credit_decision(probabilities: np.ndarray, policy: str = "balanced") -> np.ndarray:
    # Load threshold mapping from configuration
    threshold_mapping = {
        "conservative": 0.36,
        "balanced": 0.67,
        "revenue_friendly": 0.74
    }
    
    threshold = threshold_mapping.get(policy.lower(), 0.67)
    
    # Decisions: 1 = Reject (high risk of default), 0 = Approve
    decisions = (probabilities >= threshold).astype(int)
    return decisions
```
