import psycopg2

DB_HOST = "aws-1-sa-east-1.pooler.supabase.com"
DB_PORT = 6543
DB_NAME = "postgres"
DB_USER = "postgres.hkjglbnpfbadeouilvkh"
DB_PASSWORD = "ReAgXgIcI6KDPYnw"
DB_SSL = "require"

def conectar():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            sslmode=DB_SSL
        )
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None
