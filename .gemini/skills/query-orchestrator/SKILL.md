---
name: query-orchestrator
description: Manages the mapping between report slides and the specific SQL queries, data, and graphs needed for that slide. Use when asked to generate data, run a query, or prepare a report for a specific slide number or section.
---

# Query Orchestrator Skill

This skill acts as the central intelligence for generating the correct data for specific slides in the monthly report. When asked to "get data for Slide X" or "run the query for Slide Y", you should follow this workflow.

## Objective

To map a requested report slide to its underlying data sources (SQL queries), execute those queries, and prepare the necessary insights and visualizations for that slide.

## Workflow

### 1. Slide Identification
* Read `config/slide_mapping.json` to understand the context, title, and purpose of the requested slide.
* Identify what type of data the slide requires (e.g., time-series trend, demographic breakdown, categorical comparison).

### 2. Query Selection & Execution
Based on the slide context, select the appropriate pre-written query from the `queries/` directory and execute it using the `postgres-query` skill.

**Known Mappings:**
* **Slide 8 (Registers vs. Points Collected):** 
  * Needs the overall points collection vs redemption data.
  * *Query:* Use `queries/monthly_trend_collect_redeem.json` for historical data or `queries/monthly_collect_redeem_snapshot.json` for a specific month.
  * *Graph:* Associated with `payloads/graph_registers_collect_points.json`.
* **Slide 14 (Loyalty Program User Types):**
  * Needs the breakdown of collection/redemption behavior grouped by the customer's business type.
  * *Query:* Use `queries/monthly_customer_type_breakdown.json`.

*(Note: If a slide does not have a mapped query, formulate a standard PostgreSQL query based on the database schema and execute it, or use the `bigquery-data` skill if the data source is BigQuery).*

### 3. Data Processing & Visualization
* **Graphs:** If the slide requires a graph (like Slide 8), trigger the `graph-maker` skill using the appropriate configuration in the `payloads/` directory. Update the JSON payload with the newly queried data if necessary.
* **Analysis:** Pass the executed query results to the `data-analyzer` skill to generate the required 2-3 bullet points of "Key Findings".

### 4. Final Output
Provide the user with:
1. The raw query results (in a clean table format).
2. The generated "Key Findings" from the `data-analyzer`.
3. Confirmation of the generated graph (if applicable).
4. Readiness confirmation to pass this data to the `pptx-builder` skill.