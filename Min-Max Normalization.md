# Algorithm: Weighted Scoring System

## Step 1: Normalize Values
To bring transaction count & volume between **0 and 1**, we apply **Min-Max Normalization**:

\[
\text{Normalized Value} = \frac{\text{Value} - \text{Min}}{\text{Max} - \text{Min}}
\]

- This prevents categories with naturally higher costs (e.g., **travel**) from dominating.
- If a person has the **highest count/volume**, they get **1**; the lowest gets **0**.

## Step 2: Apply Weighted Formula
We calculate the **Final Score** using a **weighted sum**:

\[
\text{Final Score} = \left( \frac{\text{Transaction Count}}{\text{Max Count}} \times 0.6 \right) + \left( \frac{\text{Transaction Volume}}{\text{Max Volume}} \times 0.4 \right)
\]

- **60% weight** to **Transaction Count** → Frequent purchases indicate stronger interest.
- **40% weight** to **Transaction Volume** → Spending matters, but doesn’t dominate.

## Step 3: Compare Scores
- **Higher Score** → More Interest in that Category
- If **Travel Score > Online Shopping Score** → More interested in **Traveling**.
- Otherwise → More interested in **Online Shopping**.

## Example Calculation:
Assume we have the following transactions for a user:

| Category          | Count | Volume (Rs.) |
|------------------|------|--------------|
| Online Shopping | 2    | 20,000       |
| Traveling       | 2    | 88,000       |

### **Normalization**
- **Max Count** = `3`, **Max Volume** = `88,000`
- **Online Shopping**:
  - Normalized Count = `2 / 3 = 0.67`
  - Normalized Volume = `20,000 / 88,000 = 0.227`
- **Traveling**:
  - Normalized Count = `2 / 3 = 0.67`
  - Normalized Volume = `88,000 / 88,000 = 1.0`

### **Final Score Calculation**
\[
\text{Online Shopping Score} = (0.67 \times 0.6) + (0.227 \times 0.4) = 0.402 + 0.0908 = 0.4928
\]

\[
\text{Travel Score} = (0.67 \times 0.6) + (1.0 \times 0.4) = 0.402 + 0.4 = 0.802
\]

Since **Travel Score > Online Shopping Score**, the user is more interested in **Traveling**.

---
