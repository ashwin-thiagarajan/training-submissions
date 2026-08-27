import os
from pathlib import Path
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(ENV_PATH)

def postgres_config() -> dict:
    return {
        "host": os.getenv("POSTGRES_HOST","localhost"),
        "port": int(os.getenv("POSTGRES_PORT","5432")),
        "dbname": os.getenv("POSTGRES_DATABASE","learning_store"),
        "user": os.getenv("POSTGRES_USER","postgres"),
        "password": os.getenv("POSTGRES_PASSWORD","postgres")
    }

def run_query(query: str,args: tuple=None) -> list:
    rows = []
    with psycopg.connect(**postgres_config(), row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,(args))
            for row in cursor.fetchall():
                rows.append(row)
    return rows

def get_customers():
    query = """
        SELECT * FROM customers
    """
    for r in run_query(query):
        print(r)

def get_order_totals():
    query = """
        SELECT order_id, SUM(quantity*unit_price)
        FROM order_items 
        GROUP BY order_id
    """
    for r in run_query(query):
        print(r)

def get_customer_by_email(email):
    query = """
        SELECT * FROM customers WHERE email = %s
    """
    for r in run_query(query,(email,)):
        print(r)

def main():
    get_customers()
    get_order_totals()
    get_customer_by_email("vikram.mehta@example.com")

if __name__  == "__main__":
    main()
