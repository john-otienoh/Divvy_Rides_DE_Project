import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  

import duckdb
from config import DB_PATH
from storage.models import RAW_RIDES_DDL, INGESTION_LOG_DDL

def get_connection(read_only=False):
    conn = duckdb.connect(str(DB_PATH), read_only=read_only)
    conn.execute("SET threads TO 4")
    conn.execute("SET memory_limit = '4GB'")
    return conn

def create_all(conn):
    conn.execute(RAW_RIDES_DDL)
    conn.execute(INGESTION_LOG_DDL)
