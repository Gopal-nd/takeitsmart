

# 1️⃣ What is Statistics?

Statistics is the process of collecting, organizing, analyzing, interpreting, and presenting data in a meaningful way to make data-driven decisions.

It helps to:

* Understand summary of data
* Detect outliers
* Find relationships
* Make predictions

---

# 2️⃣ Types of Statistics

Statistics is divided into two main types:

### 1) Descriptive Statistics

Describes what is happening in the dataset.

Includes:

* Mean, Median, Mode
* Standard deviation
* Variance
* Charts and graphs

### 2) Inferential Statistics

Used to make conclusions or predictions about a population using sample data.

Includes:

* Hypothesis testing
* Correlation
* Regression
* t-test, z-test, ANOVA

---

# 3️⃣ What is Central Tendency?

Central tendency tells us the center or average of the data.

Three main measures:

1. Mean → Average
2. Median → Middle value
3. Mode → Most frequent value

### Hands-on Code

```python
import numpy as np
import pandas as pd

data = np.array([10, 20, 30, 40, 50, 50])

mean = np.mean(data)
median = np.median(data)
mode = pd.Series(data).mode()[0]

print("Mean:", mean)
print("Median:", median)
print("Mode:", mode)
```

---

# 4️⃣ Measures of Dispersion

Dispersion tells how spread out the data is.

### 1) Range

Difference between maximum and minimum.

Range = max - min

### 2) Variance

Measures how far values are from mean.

### 3) Standard Deviation (STD)

Square root of variance.

### 4) IQR (Interquartile Range)

Difference between Q3 and Q1.

### Code:

```python
data = np.array([10, 20, 30, 40, 50])

print("Range:", np.max(data) - np.min(data))
print("Variance:", np.var(data))
print("Standard Deviation:", np.std(data))

Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
print("IQR:", Q3 - Q1)
```

---

# 5️⃣ What is t-test?

t-test compares means of two groups when sample size is small and population standard deviation is unknown.

Used when:

* Sample size < 30
* Data is normally distributed

---

# 6️⃣ What is z-test?

z-test compares means when:

* Sample size is large
* Population standard deviation is known

---

# 7️⃣ What is ANOVA?

ANOVA (Analysis of Variance) compares means of more than two groups.

Assumptions:

* Data is normally distributed
* Equal variance
* Independent observations

---

# 8️⃣ What is p-value?

p-value tells the probability of getting results assuming null hypothesis is true.

If p-value < 0.05 → Reject null hypothesis
If p-value > 0.05 → Fail to reject null hypothesis

---

# 9️⃣ What is Hypothesis Testing?

It is a statistical method to test an assumption.

Steps:

1. Define null hypothesis (H0)
2. Define alternative hypothesis (H1)
3. Choose significance level
4. Calculate test statistic
5. Compare with p-value

---

# 🔟 What is Z-score?

Z-score tells how many standard deviations a value is from mean.

Formula:
Z = (X - Mean) / Std

Used to detect outliers.

---

# 1️⃣1️⃣ Why Significance Level is Important?

Significance level (α = 0.05 usually) decides when to reject null hypothesis.

It controls Type 1 error (false positive).

---

# 1️⃣2️⃣ What is Chi-Square?

Chi-square test checks relationship between categorical variables.

Used for:

* Independence test
* Goodness of fit

---

# 1️⃣3️⃣ How Data is Distributed?

Distribution shows how values are spread.

Common Distributions:

* Normal (bell shape)
* Binomial (success/failure)
* Poisson (event count)
* Uniform (equal probability)
* Exponential (waiting time)
* Chi-square (categorical testing)

Example Normal:

```python
import matplotlib.pyplot as plt
data = np.random.normal(0,1,1000)
plt.hist(data)
plt.show()
```

---

# 1️⃣4️⃣ What is Inferential Statistics?

It uses sample data to make predictions about population.

Examples:

* Regression
* Hypothesis testing
* Correlation

---

# 1️⃣5️⃣ What is Correlation?

Correlation shows relationship between two variables.

Range: -1 to +1

+1 → Strong positive
-1 → Strong negative
0 → No correlation

```python
df = pd.read_csv("iris.csv")
print(df.corr())
```

---

# 1️⃣6️⃣ What is Regression Analysis?

Regression predicts dependent variable using independent variable.

Example:
Predict house price using area.

---

# 1️⃣7️⃣ Independent vs Dependent Variables

Independent Variable → Input (X)
Dependent Variable → Output (Y)

Example:
Area → Independent
Price → Dependent

---

# 1️⃣8️⃣ How Statistics Impacts ML Models?

* Feature selection
* Outlier detection
* Model accuracy
* Bias detection
* Probability calculations

---

# 1️⃣9️⃣ What are Data Attributes?

Attributes are features/columns in dataset.

Example:
Age, Salary, Height

---

# 2️⃣0️⃣ Qualitative vs Quantitative

Qualitative → Categorical data (Gender, Color)
Quantitative → Numerical data (Height, Weight)

---

# 2️⃣1️⃣ Continuous vs Categorical

Continuous → Any value in range (Height)
Categorical → Fixed categories (Male/male)

---

# 2️⃣2️⃣ What is Data?

Data is raw information.

Types:

* Structured (tables, SQL)
* Unstructured (images, videos, text)
* Semi-structured (JSON, XML)

---

# 2️⃣3️⃣ What are Outliers?

Outliers are extreme values far from normal data.

They affect:

* Mean
* Model performance
* Regression results

---

# 2️⃣4️⃣ How to Find Outliers?

1. Using Z-score:

```python
from scipy import stats
z = np.abs(stats.zscore(data))
print(data[z > 3])
```

2. Using IQR:

Lower = Q1 - 1.5*IQR
Upper = Q3 + 1.5*IQR

```python
Q1 = np.percentile(data,25)
Q3 = np.percentile(data,75)
IQR = Q3 - Q1

lower = Q1 - 1.5*IQR
upper = Q3 + 1.5*IQR

outliers = data[(data < lower) | (data > upper)]
print(outliers)
```
