import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data extracted from BigQuery
data = [
    { "date_record": "2025-05-01", "gain_friends_ad": 0, "add_friend_urls": 1117, "other_sources": 34 },
    { "date_record": "2025-06-01", "gain_friends_ad": 0, "add_friend_urls": 913, "other_sources": 15 },
    { "date_record": "2025-07-01", "gain_friends_ad": 0, "add_friend_urls": 828, "other_sources": 33 },
    { "date_record": "2025-08-01", "gain_friends_ad": 3032, "add_friend_urls": 702, "other_sources": 75 },
    { "date_record": "2025-09-01", "gain_friends_ad": 2612, "add_friend_urls": 848, "other_sources": 117 },
    { "date_record": "2025-10-01", "gain_friends_ad": 2918, "add_friend_urls": 771, "other_sources": 121 },
    { "date_record": "2025-11-01", "gain_friends_ad": 0, "add_friend_urls": 900, "other_sources": 92 },
    { "date_record": "2025-12-01", "gain_friends_ad": 4786, "add_friend_urls": 1116, "other_sources": 113 },
    { "date_record": "2026-01-01", "gain_friends_ad": 5801, "add_friend_urls": 879, "other_sources": 61 },
    { "date_record": "2026-02-01", "gain_friends_ad": 1853, "add_friend_urls": 827, "other_sources": 71 }
]

# Convert to DataFrame
df = pd.DataFrame(data)
df['date_record'] = pd.to_datetime(df['date_record'])

# Create the plot
plt.figure(figsize=(14, 8))

# Using a higher-contrast, distinct color palette
color_ad = '#1f77b4'      # Strong Blue
color_urls = '#ff7f0e'    # Bright Orange
color_other = '#d62728'   # Strong Red

# Plot the lines
plt.plot(df['date_record'], df['gain_friends_ad'], label='Gain Friends Ad', marker='o', linewidth=3, color=color_ad)
plt.plot(df['date_record'], df['add_friend_urls'], label='Add Friend URLs', marker='o', linewidth=3, color=color_urls)
plt.plot(df['date_record'], df['other_sources'], label='Other', marker='o', linewidth=3, color=color_other)

# Add labels to the points
for i in range(len(df)):
    # Gain Friends Ad
    lbl1 = f"{int(df['gain_friends_ad'][i]):,}"
    plt.text(df['date_record'][i], df['gain_friends_ad'][i] + 300, lbl1, ha='center', va='bottom', fontsize=12, color=color_ad, fontweight='bold')
    
    # Add Friend URLs
    lbl2 = f"{int(df['add_friend_urls'][i]):,}"
    plt.text(df['date_record'][i], df['add_friend_urls'][i] - 300, lbl2, ha='center', va='top', fontsize=12, color=color_urls, fontweight='bold')
    
    # Other Sources
    lbl3 = f"{int(df['other_sources'][i]):,}"
    plt.text(df['date_record'][i], df['other_sources'][i] - 150, lbl3, ha='center', va='top', fontsize=12, color=color_other, fontweight='bold')

# Formatting
plt.title('TULIP TRAFFIC SOURCE (May 2025 - Feb 2026)', fontsize=18)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Friends Gained', fontsize=14)

# Adjust y-axis limit to start at 0 and make room for text
ymin, ymax = plt.ylim()
plt.ylim(0, ymax + 1000)

# Adjust x-axis limit and explicit labels
plt.xlim(df['date_record'].min() - pd.Timedelta(days=15), df['date_record'].max() + pd.Timedelta(days=15))
plt.xticks(df['date_record'], df['date_record'].dt.strftime('%B -%y'), rotation=45, fontsize=12)
plt.yticks(fontsize=12)

plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot as a high-resolution image
output_filename = 'graph/traffic_sources_graph.png'
plt.savefig(output_filename, dpi=300)
print(f"Graph saved successfully as '{output_filename}'")

