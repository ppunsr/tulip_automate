import psycopg2
from sshtunnel import SSHTunnelForwarder
import pandas as pd
import json
import sys
import argparse

# SSH Bastion Details
SSH_HOST = "43.208.228.160"
SSH_USER = "ssh-guest"
SSH_KEY_PATH = "/Users/sboora01/Tulip project/Tulip-automate/ssh-guest-openssh.pem"

# Database Details
DB_HOST = "postgres-production-merkle-thailand.c3o6ew0mggoz.ap-southeast-7.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "tulip_crm_prod"
DB_USER = "tulip_crm_view"
DB_PASSWORD = "=Yps+ox3Asj_NvjEC2g_dCEQq"

def run_query(sql_query):
    try:
        with SSHTunnelForwarder(
            (SSH_HOST, 22),
            ssh_username=SSH_USER,
            ssh_pkey=SSH_KEY_PATH,
            remote_bind_address=(DB_HOST, DB_PORT)
        ) as tunnel:
            conn = psycopg2.connect(
                host='127.0.0.1',
                port=tunnel.local_bind_port,
                user=DB_USER,
                password=DB_PASSWORD,
                dbname=DB_NAME
            )
            
            df = pd.read_sql_query(sql_query, conn)
            # Output as CSV so it's easily readable by the CLI
            print(df.to_csv(index=False))
            conn.close()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run SQL query on Postgres via SSH tunnel.')
    parser.add_argument('json_params', type=str, help='JSON string containing the SQL query e.g. {"sql": "SELECT * FROM..."}')
    args = parser.parse_args()
    
    try:
        params = json.loads(args.json_params)
        sql_query = params.get('sql')
        if not sql_query:
            print("Error: 'sql' key not found in JSON string.", file=sys.stderr)
            sys.exit(1)
        
        run_query(sql_query)
    except json.JSONDecodeError:
        print("Error: Invalid JSON string provided.", file=sys.stderr)
        sys.exit(1)
