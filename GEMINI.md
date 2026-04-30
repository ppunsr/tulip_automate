# Tulip-automate Workspace

## Project Overview

This directory serves as a workspace for automating data extraction and reporting tasks for the "Tulip" project. It contains Python scripts designed to connect securely to a production PostgreSQL database via an SSH tunnel, extract relevant data, and generate high-quality visualization graphs for reporting purposes. Additionally, the workspace includes custom Gemini CLI skills that integrate with these scripts and templates to automate end-to-end report generation workflows.

## Key Files & Structure

*   `scripts/`: Contains executable Python scripts.
    *   `test_db_connection.py`: Establishes an SSH tunnel and connects to the `tulip_crm_prod` database.
    *   `analyze_pptx.py`: Helper script for inspecting PowerPoint template layouts.
*   `Graph_Month/` (e.g., `Graph_March/`, `Graph_February/`): Directories where the high-resolution output graphs are saved and archived by month.
*   `payloads/`: Contains extracted JSON data payloads used for graph generation (via `graph-maker` skill) and analysis.
*   `queries/`: Contains raw `.json` files storing complex SQL queries for execution against the database.
*   `fonts/`: Contains official fonts (like TH Sarabun New) used for generating graphs with proper Thai character support.
*   `conductor/`: Contains the overall project plan and orchestration documentation (e.g., `monthly-report.md`).
*   `config/`: Contains mapping configuration (e.g., `slide_mapping.json`) connecting PowerPoint slide numbers to their required data.
*   `Tulip_example.pptx`: The PowerPoint template used as the base for generated reports.
*   `ssh-guest-*.pem`: SSH private keys used for securely tunneling into the database network.

### Gemini CLI Skills
*   `powerpoint-data-contain`: Manages the layout blueprint for each PowerPoint slide (defining what text, graphs, and data go on which page).
*   `query-orchestrator`: Manages mapping between report slides and the specific SQL queries, data, and graphs needed for that slide.
*   `postgres-query`: Fetches PostgreSQL data securely via SSH tunnel.
*   `graph-maker`: Automates the generation of `.png` graphs from provided JSON payloads in the `payloads/` folder.
*   `data-analyzer`: Analyzes extracted data to generate key finding bullet points.

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
Graphs are generated using the `graph-maker` skill by passing the appropriate JSON payload:
```bash
python3 .gemini/skills/graph-maker/scripts/make_graph.py "$(cat payloads/graph_line_friends.json)"
```

## Development Conventions

*   **Data Processing:** `pandas` is the standard library used for structuring and manipulating data within scripts.
*   **Database Access:** Connections to the production database MUST be routed through an SSH tunnel (using `sshtunnel` and `psycopg2`). Direct connections are not supported.
*   **Visualizations:** Graphs are generated programmatically via the `graph-maker` skill using `matplotlib`, applying custom formatting (clear labels, specific color palettes), and saving at 300 DPI for presentation quality into their respective month folders (e.g., `Graph_March/`).
*   **Automation:** Repeated workflows are encapsulated into Gemini CLI skills (e.g., `powerpoint-data-contain`, `query-orchestrator`, `data-analyzer`) to allow the agent to execute them autonomously upon request in coordination with the conductor track plans.