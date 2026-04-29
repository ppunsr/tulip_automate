import matplotlib.pyplot as plt
import pandas as pd

# This is a reference template for how the graph-maker skill should style and format output.
# Replace data and columns as needed based on the user's request.

data = [
    { "date": "2026-01", "value1": 100, "value2": 50 },
    { "date": "2026-02", "value1": 120, "value2": 60 }
]

df = pd.DataFrame(data)
# df['date'] = pd.to_datetime(df['date']) # Ensure dates are formatted correctly

plt.figure(figsize=(12, 7))

# Plot lines
plt.plot(df['date'], df['value1'], label='Metric 1', marker='o', linewidth=2, color='#36a2eb')
plt.plot(df['date'], df['value2'], label='Metric 2', marker='o', linewidth=2, color='#ff6384')

# Add labels to the points
for i in range(len(df)):
    plt.text(df['date'][i], df['value1'][i] + 5, f"{df['value1'][i]:,}", ha='center', va='bottom', fontsize=9, color='#36a2eb')
    plt.text(df['date'][i], df['value2'][i] - 5, f"{df['value2'][i]:,}", ha='center', va='top', fontsize=9, color='#ff6384')

# Formatting
plt.title('Graph Title', fontsize=16)
plt.xlabel('Date / X-Axis Label', fontsize=12)
plt.ylabel('Count / Y-Axis Label', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save
plt.savefig('output_graph.png', dpi=300)
