# Automated Monthly Report Generation Plan

## Objective
To build an automated, multi-agent workflow orchestrated by Gemini CLI that generates a comprehensive, single-page monthly PowerPoint report. This report will combine data from Google BigQuery and a secure PostgreSQL database, visualize it using Python-generated graphs, provide AI-driven analytical insights, and assemble the final output using a user-provided `.pptx` template.

## Key Files & Context
*   **Data Sources:**
    *   Google BigQuery (`dentsu-merkle-tulip:tulip_dataset`)
    *   PostgreSQL (`tulip_crm_prod` via SSH Tunnel)
*   **Existing Skills:**
    *   `bigquery-data`: To fetch BigQuery data.
    *   `postgres-query`: To fetch PostgreSQL data securely.
    *   `graph-maker`: To generate `.png` charts from data.
*   **New Components Required:**
    *   User-provided `.pptx` template.
    *   `pptx-builder` skill (to be developed).

## Scope & Impact
The report will cover a dynamic set of metrics requiring precise coordination between data extraction, graph generation, analysis, and PPTX population. Example metrics include (but are not limited to):
*   **Tulip Line Friends:** Time-series graph (June 2025 - Report Month). Source: BigQuery.
*   **Tulip Line Traffic Sources:** Time-series graph of friends gained by source. Source: BigQuery / Postgres.
*   **Tulip Line Registers:** Bar chart comparing registration steps vs. points collected. Source: Postgres.
*   **Tulip Line Redeem (1):** Number of rewards redeemed. Source: Postgres.
*   **Tulip Line Redeem (2):** Bar graph of points used in redemptions. Source: Postgres.
*   **Additional Metrics:** The workflow is designed to be extensible to accommodate additional time-series and bar charts as needed.

## Implementation Steps

### Phase 1: PPTX Builder Skill Development
1.  **Template Analysis:** Analyze the uploaded `.pptx` template to identify slide layouts, image placeholders, and text box naming conventions.
2.  **Create Skill:** Initialize a `pptx-builder` Gemini CLI skill.
3.  **Develop Python Script:** Write a Python script within the skill using `python-pptx` that can:
    *   Open the template.
    *   Navigate to specific slides.
    *   Insert generated `.png` graphs (line charts, bar charts) into predefined coordinate boxes or placeholders.
    *   Insert Gemini-generated "Key Findings" strings into specific text boxes.
    *   Save the modified presentation as a new file (e.g., `Monthly_Report_YYYY_MM.pptx`).

### Phase 2: Orchestration Workflow (Execution)
When the user requests the monthly report, Gemini will execute the following sequence:
1.  **Data Extraction:** Execute predefined SQL queries against BigQuery and PostgreSQL for all required report sections using the respective skills.
2.  **Visualization:** Pass the extracted DataFrames to the `graph-maker` skill to generate the required `.png` charts (Line, Bar, etc.).
3.  **Analysis:** Analyze the extracted data to generate 1-2 bullet points of "Key Findings" for each section.
4.  **Assembly:** Pass the generated `.png` file paths and the "Key Findings" text strings to the `pptx-builder` skill to generate the final presentation.

## Verification & Testing
*   **Skill Test:** The `pptx-builder` skill will be tested with dummy data and a dummy graph to ensure successful `.pptx` generation without corrupting the template.
*   **End-to-End Test:** A full run of the orchestration workflow will be executed to verify data accuracy, graph formatting, insight generation, and final slide layout.