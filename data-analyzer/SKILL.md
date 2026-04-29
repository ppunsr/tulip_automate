
---
name: data-analyzer
description: Analyzes extracted data (e.g., JSON payloads, BigQuery/PostgreSQL results) to generate 2-3 key finding bullet points for monthly reports. Use when asked to summarize data or extract key insights for the pptx-builder.
---

# Data Analyzer Skill

This skill provides the procedural workflow for acting as a data analyst. It instructs you on how to examine extracted report data and synthesize it into concise, impactful "Key Findings" suitable for executive PowerPoint presentations.

## Objective

Given a dataset (typically in JSON format containing time-series data, bar chart data, or a SQL query description), your goal is to extract the most important insights and format them as 2-3 high-level bullet points. These bullet points will be inserted into the final monthly report presentation by the `pptx-builder` skill.

## Workflow

When tasked with analyzing data using this skill, strictly follow these steps:

### 1. Data Ingestion
*   Read the provided data source. This may be a JSON file located in the `payloads/` directory, or raw data extracted via `bigquery-data` or `postgres-query`.
*   Pay close attention to the data schema:
    *   **Time-series (Line charts):** Look for trends over time, seasonal peaks, or sudden drops.
    *   **Categorical (Bar charts):** Compare the relative sizes of different categories or funnels.
*   Read any accompanying `description` or `sql` fields in the JSON to understand the context of the data.

### 2. Analysis & Synthesis
Analyze the data to identify the most significant takeaways. Look for:
*   **Major Trends:** Is the overall metric growing, shrinking, or stable?
*   **Anomalies & Spikes:** Are there specific months with unusually high or low activity? (e.g., "A massive spike in December due to ad campaigns").
*   **Baselines:** What is the steady, reliable contributor? (e.g., "Organic URLs provide a consistent baseline of ~900 users/month").
*   **Comparisons:** How do different categories or funnels compare? (e.g., "Registrations are growing steadily, but active point collectors are cyclical").

### 3. Formatting Output
Generate exactly **2 to 3 bullet points**.
*   **Tone:** Professional, analytical, and concise. Avoid conversational filler.
*   **Structure:** Start each bullet point with a short, bolded summary phrase, followed by the explanation.
*   **Length:** Each bullet point should be 1-2 sentences maximum.

**Example Output:**
*   **Ad-Driven Spikes:** The "Gain friends ad" channel is the most significant driver of new users, peaking heavily in December (4,786) and January (5,801).
*   **Consistent Organic Baseline:** "Add Friend URLs" provide a remarkably stable baseline of user acquisition, reliably bringing in an average of ~900 new friends every month.
*   **Recent Slowdown:** Following the massive January ad spike, there was a sharp 68% drop-off in ad-driven acquisitions in February.

## Next Steps
Once the key findings are generated, pass them along with the corresponding generated graph image (from `graph-maker`) to the `pptx-builder` skill to assemble the final slide.