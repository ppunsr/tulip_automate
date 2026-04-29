import psycopg2
from sshtunnel import SSHTunnelForwarder
import pandas as pd

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

try:
    print("Opening SSH tunnel...")
    with SSHTunnelForwarder(
        (SSH_HOST, 22),
        ssh_username=SSH_USER,
        ssh_pkey=SSH_KEY_PATH,
        remote_bind_address=(DB_HOST, DB_PORT)
    ) as tunnel:
        print(f"SSH tunnel established. Local port bound: {tunnel.local_bind_port}")
        
        print("Connecting to PostgreSQL database...")
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=tunnel.local_bind_port,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        
        print("Connection successful! Testing query...")
        # Query to list views
        query = """
        SELECT table_schema, table_name 
        FROM information_schema.views 
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY table_schema, table_name;
        """
        df = pd.read_sql_query(query, conn)
        print("\nAvailable Views:")
        pd.set_option('display.max_rows', None) # Show all rows
        print(df)
        
        conn.close()
        print("Database connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")
