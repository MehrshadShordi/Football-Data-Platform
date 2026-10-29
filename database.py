import os
import psycopg2
from psycopg2.extras import Json
from contextlib import closing


def get_connection():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    return psycopg2.connect(database_url)


def init_db():
    with closing(get_connection()) as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS match_cache (
                        id SMALLINT PRIMARY KEY CHECK (id = 1),
                        payload JSONB NOT NULL,
                        fetched_at TIMESTAMPTZ NOT NULL
                    )
                """)


def load_cache():
    with closing(get_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT payload, fetched_at
                FROM match_cache
                WHERE id = 1
            """)
            return cur.fetchone()


def save_cache(data):
    with closing(get_connection()) as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO match_cache (id, payload, fetched_at)
                    VALUES (1, %s, NOW())
                    ON CONFLICT (id)
                    DO UPDATE SET
                        payload = EXCLUDED.payload,
                        fetched_at = EXCLUDED.fetched_at
                """, (Json(data),))
