---
name: postgres-query
description: Queries the Tulip CRM PostgreSQL production database via a secure SSH tunnel. Use this skill when the user provides a SQL query or asks to extract data from the PostgreSQL database tables or views.
---

# PostgreSQL Query Skill

This skill allows you to securely query the `tulip_crm_prod` database by automatically handling the SSH tunnel and connection details.

## Usage

When you need to run a query against the PostgreSQL database, use the `run_shell_command` tool to execute the provided Python script.

**Important:** The script accepts a single argument which must be a JSON string containing the `sql` key. The output will be formatted as CSV for easy reading.

**Bash:**
```bash
python3 <skill_dir>/scripts/query.py '{"sql": "<YOUR_SQL_QUERY_HERE>"}'
```

**Example:**
```bash
python3 <skill_dir>/scripts/query.py '{"sql": "SELECT * FROM member_point LIMIT 5;"}'
```

## Workflow

1.  **Formulate Query:** Based on the user's request, formulate the standard PostgreSQL query. Note that you have access to various views like `member_point`, `member_transaction_point`, `reward_redemption`, etc.
2.  **Execute Script:** Call the `scripts/query.py` script as shown above using `run_shell_command`. Make sure to properly escape the JSON string.
3.  **Process Result:** The script will output the data in CSV format. Read the CSV output and provide the analysis or insight to the user.

## Bundled Resources
* `scripts/query.py`: The python execution script that handles the `sshtunnel` and `psycopg2` logic.