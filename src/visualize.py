import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

# Load your merged data
df = pd.read_csv("data/cleaned/merged_tasca_airbnb.csv")

# Create a scatter plot
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    data=df, 
    x='airbnb_count', 
    y='tascas_count',  # or use your actual column name
    hue='neighbourhood',
    alpha=0.7,
    s=100
)

# Add correlation line
z = np.polyfit(df['airbnb_count'], df['tascas_count'], 1)
p = np.poly1d(z)
plt.plot(df['airbnb_count'], p(df['airbnb_count']), "r--", label=f"Trend Line (r={z[0]:.2f})")

# Labels and title
plt.xlabel('Number of Airbnbs in Neighborhood')
plt.ylabel('Number of Tascas')
plt.title('Tasca Density vs Airbnb Tourist Density by Neighborhood')
plt.legend()
plt.grid(True, alpha=0.3)

# Save the figure
plt.savefig("results/scatter_airbnb_vs_tasca.png", dpi=300)


plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='airbnb_count', y='tascas_count', hue='neighbourhood', s=100, alpha=0.7)

# Add regression line
sns.regplot(data=df, x='airbnb_count', y='tascas_count', scatter=False, color='red', label='Trend')

# Annotate stats
r, p = stats.pearsonr(df['airbnb_count'], df['tascas_count'])
plt.text(0.75, 0.95, f'r = {r:.2f}\np = {p:.3e}', transform=plt.gca().transAxes, 
         bbox=dict(facecolor='white', alpha=0.8))

plt.xlabel('Airbnb Listings (Tourist Density Proxy)')
plt.ylabel('Number of Traditional Tascas')
plt.title('Hypothesis: Does Tourism Displace Traditional Culture?')
plt.savefig("results/scatter_hypothesis.png")

plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='airbnb_count', y='avg_price_level', hue='neighbourhood', s=100, alpha=0.7)

# Add regression line
sns.regplot(data=df, x='airbnb_count', y='avg_price_level', scatter=False, color='red', label='Trend')

# Annotate stats
r, p = stats.pearsonr(df['airbnb_count'], df['avg_price_level'])
plt.text(0.75, 0.95, f'r = {r:.2f}\np = {p:.3e}', transform=plt.gca().transAxes, 
         bbox=dict(facecolor='white', alpha=0.8))

plt.xlabel('Airbnb Listings (Tourist Density Proxy)')
plt.ylabel('Average price level of tascas')
plt.title('Hypothesis: Does Tourism Increase Local Prices?')
plt.savefig("results/scatter_avg_price.png")


plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='avg_Nreviews_airbnb', y='tascas_count', hue='neighbourhood', s=100, alpha=0.7)

# Add regression line
sns.regplot(data=df, x='avg_Nreviews_airbnb', y='tascas_count', scatter=False, color='red', label='Trend')

# Annotate stats
r, p = stats.pearsonr(df['avg_Nreviews_airbnb'], df['tascas_count'])
plt.text(0.75, 0.95, f'r = {r:.2f}\np = {p:.3e}', transform=plt.gca().transAxes, 
         bbox=dict(facecolor='white', alpha=0.8))

plt.xlabel('Number of airbnb reviews (which area is more touristic)')
plt.ylabel('Tascas count')
plt.title('Hypothesis: Does Tourism Increase Local Prices?')
plt.savefig("results/scatter_number_reviews.png")