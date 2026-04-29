# Tulip-automate Workspace

## Project Overview

This directory serves as a workspace for automating data extraction and reporting tasks for the "Tulip" project. It contains Python scripts designed to connect securely to a production PostgreSQL database via an SSH tunnel, extract relevant data, and generate high-quality visualization graphs for reporting purposes. Additionally, the workspace includes custom Gemini CLI skills that integrate with these scripts and templates to automate end-to-end report generation workflows.

## Key Files & Structure

*   `scripts/`: Contains executable Python scripts.
    *   `test_db_connection.py`: Establishes an SSH tunnel and connects to the `tulip_crm_prod` database.
    *   `generate_*_graph.py`: Scripts using `pandas` and `matplotlib` to generate specific data visualization charts.
    *   `analyze_pptx.py`: Helper script for inspecting PowerPoint template layouts.
*   `graph/`: Directory where the high-resolution output graphs (e.g., `line_friends_report_graph.png`) are saved.
*   `payloads/`: Contains extracted JSON data payloads used for graph generation and analysis.
*   `conductor/`: Contains the overall project plan and orchestration documentation (e.g., `monthly-report.md`).
*   `Tulip_example.pptx` & `Monthly_Report_Test.pptx`: The PowerPoint templates and output files.
*   `ssh-guest-*.pem`: SSH private keys used for securely tunneling into the database network.

### Gemini CLI Skills
*   `postgres-query`: Fetches PostgreSQL data securely via SSH tunnel.
*   `graph-maker`: Automates the generation of `.png` graphs from provided data.
*   `data-analyzer`: Analyzes extracted data to generate key finding bullet points.
*   `pptx-builder`: Inserts generated graphs and text insights into the `.pptx` template.

## Building and Running

To run the tools in this workspace, ensure you have Python 3 installed along with the required dependencies:

```bash
# Install required Python packages
python3 -m pip install pandas matplotlib psycopg2-binary sshtunnel python-pptx
```

**Testing the Database Connection:**
Run the connection script to verify access to the database:
```bash
python3 scripts/test_db_connection.py
```

**Generating a Report Graph:**
Execute a report generator to create a visualization:
```bash
python3 scripts/generate_line_friends_graph.py
```

## Development Conventions

*   **Data Processing:** `pandas` is the standard library used for structuring and manipulating data within scripts.
*   **Database Access:** Connections to the production database MUST be routed through an SSH tunnel (using `sshtunnel` and `psycopg2`). Direct connections are not supported.
*   **Visualizations:** Graphs are generated using `matplotlib`, applying custom formatting (clear labels, specific color palettes) and saved at 300 DPI for presentation quality into the `graph/` folder.
*   **Automation:** Repeated workflows are encapsulated into Gemini CLI skills (e.g., `data-analyzer`, `pptx-builder`) to allow the agent to execute them autonomously upon request in coordination with the conductor track plans.