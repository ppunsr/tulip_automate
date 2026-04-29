import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data extracted from BigQuery
data = [
    { "date_record": "2025-06-30", "target_reach": 37955, "blocked_count": 6950 },
    { "date_record": "2025-07-31", "target_reach": 38280, "blocked_count": 7138 },
    { "date_record": "2025-08-31", "target_reach": 40909, "blocked_count": 7928 },
    { "date_record": "2025-09-30", "target_reach": 43244, "blocked_count": 8667 },
    { "date_record": "2025-10-31", "target_reach": 45518, "blocked_count": 9680 },
    { "date_record": "2025-11-30", "target_reach": 45572, "blocked_count": 10224 },
    { "date_record": "2025-12-31", "target_reach": 50281, "blocked_count": 11066 },
    { "date_record": "2026-01-31", "target_reach": 55197, "blocked_count": 12345 },
    { "date_record": "2026-02-28", "target_reach": 56433, "blocked_count": 13411 },
    { "date_record": "2026-03-31", "target_reach": 59108, "blocked_count": 14607 },
    { "date_record": "2026-04-27", "target_reach": 59161, "blocked_count": 14829 }
]

# Convert to DataFrame
df = pd.DataFrame(data)
df['date_record'] = pd.to_datetime(df['date_record'])
df['total_friend'] = df['target_reach'] + df['blocked_count']

# Calculate Month-over-Month differences and percentages
for col in ['total_friend', 'target_reach', 'blocked_count']:
    df[f'{col}_diff'] = df[col].diff()
    df[f'{col}_pct'] = (df[col].pct_change() * 100).round(1)

# Function to format the label
def format_label(val, diff, pct):
    if pd.isna(diff):
        return f"{int(val):,}"
    sign = "+" if diff > 0 else ""
    return f"{int(val):,}\n{sign}{int(diff):,} ({sign}{pct}%)"

# Create the plot
plt.figure(figsize=(14, 8))

# Using a higher-contrast, distinct color palette (Dark Blue, Orange, Dark Red)
color_total = '#1f77b4'   # Strong Blue
color_reach = '#ff7f0e'   # Bright Orange
color_blocked = '#d62728' # Strong Red

plt.plot(df['date_record'], df['total_friend'], label='Total Friend (Friends + Blocked)', marker='o', linewidth=3, color=color_total)
plt.plot(df['date_record'], df['target_reach'], label='Friends (target_reach)', marker='o', linewidth=3, color=color_reach)
plt.plot(df['date_record'], df['blocked_count'], label='Blocked (blocked_count)', marker='o', linewidth=3, color=color_blocked)

# Add labels to the points
for i in range(len(df)):
    # Total Friends label
    lbl_total = format_label(df['total_friend'][i], df['total_friend_diff'][i], df['total_friend_pct'][i])
    plt.text(df['date_record'][i], df['total_friend'][i] + 2500, lbl_total, ha='center', va='bottom', fontsize=10, color=color_total, fontweight='bold')
    
    # Target Reach label
    lbl_reach = format_label(df['target_reach'][i], df['target_reach_diff'][i], df['target_reach_pct'][i])
    plt.text(df['date_record'][i], df['target_reach'][i] - 2500, lbl_reach, ha='center', va='top', fontsize=10, color=color_reach, fontweight='bold')
    
    # Blocked Count label
    lbl_blocked = format_label(df['blocked_count'][i], df['blocked_count_diff'][i], df['blocked_count_pct'][i])
    plt.text(df['date_record'][i], df['blocked_count'][i] - 2500, lbl_blocked, ha='center', va='top', fontsize=10, color=color_blocked, fontweight='bold')

# Formatting
plt.title('Line Friends Growth (June 2025 - April 2026)', fontsize=18)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Count', fontsize=14)

# Adjust y-axis limit to make room for text
ymin, ymax = plt.ylim()
plt.ylim(ymin - 4000, ymax + 8000)

# Adjust x-axis limit to avoid extending into the next month
plt.xlim(df['date_record'].min() - pd.Timedelta(days=15), df['date_record'].max() + pd.Timedelta(days=15))

# Explicitly set the x-axis ticks to ensure every data point's month is labelled
plt.xticks(df['date_record'], df['date_record'].dt.strftime('%B -%y'), rotation=45)

plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot as a high-resolution image for the report
output_filename = 'line_friends_report_graph.png'
plt.savefig(output_filename, dpi=300)
print(f"Graph saved successfully as '{output_filename}'")
