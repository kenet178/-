from contextlib import closing
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def connect(db_path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(str(db_path), isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def initialize(connection: sqlite3.Connection, with_seed: bool = True) -> None:
    connection.executescript((ROOT / "schema.sql").read_text(encoding="utf-8"))
    if with_seed and not connection.execute("SELECT 1 FROM flights LIMIT 1").fetchone():
        connection.executescript((ROOT / "seed.sql").read_text(encoding="utf-8"))

def init_database(db_path: str, with_seed: bool = True) -> None:
    with closing(connect(db_path)) as connection:
        initialize(connection, with_seed=with_seed)

if __name__ == '__main__':
    init_database(str(ROOT / 'airline.db'))
    print('База авиакомпании создана:', ROOT / 'airline.db')
