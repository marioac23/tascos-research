import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Arguments for running code",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-i", "--input", default=None, type = str, help="input list of restaurants/tascas")
parser.add_argument("-o", "--output", default=None, type = str, help="output file")


args = vars(parser.parse_args())


input    = args["input"]
output      = args["output"]

# Load the master dataset
df = pd.read_csv(input)


# === VARIABLE DEFINITIONS ===
y = df['avg_price_level']           # Dependent Variable: Price
X = df[['airbnb_count', 'avg_rating', 'tascas_count']] # Independent Variables

# Add constant term (intercept) for regression
X = sm.add_constant(X)

# === RUN THE REGRESSION ===
model = sm.OLS(y, X).fit()

print(model.summary())

# === INTERPRETATION ===
# Look for the coefficient under 'airbnb_count'
coeff_airbnb = model.params['airbnb_count']
p_val = model.pvalues['airbnb_count']

print(f"\n--- KEY FINDINGS ---")
print(f"Coefficient for Airbnb Count: {coeff_airbnb:.4f}")
print(f"P-value: {p_val:.4f}")

if p_val < 0.05:
    print("✅ Statistically Significant! Higher Airbnb density predicts higher Tasca prices.")
    direction = "increase" if coeff_airbnb > 0 else "decrease"
    print(f"Interpretation: For every additional 10 Airbnbs, avg price level {direction} by {abs(coeff_airbnb)*10:.2f}.")
else:
    print("⚠️ Not statistically significant. Other factors may dominate.")

# === VISUALIZATION: The Scatter Plot with Fit Line ===
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='airbnb_count', y='avg_price_level', alpha=0.6, label='Data Points')

# Add the regression line
x_vals = np.linspace(df['airbnb_count'].min(), df['airbnb_count'].max(), 100)
y_pred = model.params['const'] + model.params['airbnb_count']*x_vals + model.params['avg_rating']*df['avg_rating'].mean() + model.params['tascas_count']*df['tascas_count'].mean()
# Better approach: Just plot simple trend line for visualization
z = np.polyfit(df['airbnb_count'], df['avg_price_level'], 1)
p = np.poly1d(z)
plt.plot(x_vals, p(x_vals), "r--", label=f"Trend (r={np.corrcoef(df['airbnb_count'], df['avg_price_level'])[0,1]:.2f})")

plt.title('Impact of Airbnb Density on Traditional Tasca Prices\n(Lisbon, Portugal)')
plt.xlabel('Number of Airbnb Listings per Neighborhood')
plt.ylabel('Average Tasca Price Level ($$$ Scale)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(output, dpi=300)
plt.show()