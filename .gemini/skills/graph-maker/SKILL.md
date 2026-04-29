---
name: graph-maker
description: Generates high-quality, labeled data visualization graphs (line charts, bar charts) and saves them as image files (e.g., .png) using Python, pandas, and matplotlib. Use when the user requests a chart or graph to be created from data for a report.
---

# Graph Maker Skill

This skill allows you to programmatically generate high-resolution data visualization graphs using a generic Python script.

## Usage

Use the `run_shell_command` tool to execute the `make_graph.py` script. The script accepts a single JSON string argument detailing the data and required formatting.

**Bash:**
```bash
python3 <skill_dir>/scripts/make_graph.py '<JSON_CONFIG_STRING>'
```

### JSON Configuration Format

The JSON string must contain the following keys:
*   `output_filename`: (Required) The desired path for the generated `.png` graph (e.g., "line_friends_report_graph.png").
*   `title`: (Optional) The title of the graph.
*   `x_label`: (Optional) The label for the x-axis.
*   `y_label`: (Optional) The label for the y-axis.
*   `chart_type`: (Optional) "line" or "bar". Defaults to "line".
*   `calculate_mom`: (Optional) Boolean. If true, adds Month-over-Month difference and percentage growth labels to the data points.
*   `x_axis_col`: (Required) The name of the column in the `data` array to use for the x-axis.
*   `data`: (Required) An array of objects representing the raw data (e.g., from BigQuery or Postgres).
*   `series`: (Required) An array of objects defining which columns to plot.

**Series Object Fields:**
*   `column`: The name of the key in the `data` array.
*   `label`: The display name for the legend.
*   `color`: The hex color code (e.g., "#36a2eb", "#4bc0c0", "#ff6384").

**Example Configuration:**
```json
{
  "output_filename": "line_friends_report_graph.png",
  "title": "Line Friends Growth",
  "x_label": "Date",
  "y_label": "Count",
  "chart_type": "line",
  "calculate_mom": true,
  "x_axis_col": "date_record",
  "data": [
    { "date_record": "2026-03-31", "target_reach": 59108, "blocked_count": 14607 }
  ],
  "series": [
    {"column": "target_reach", "label": "Friends", "color": "#4bc0c0"},
    {"column": "blocked_count", "label": "Blocked", "color": "#ff6384"}
  ]
}
```

## Bundled Resources

*   `scripts/make_graph.py`: The Python script that parses the JSON configuration and generates the graph using `matplotlib`.