
import os

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://", "postgresql://", 1
    )


def _connect():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is missing. Configure it in .env."
        )

    return psycopg.connect(
        DATABASE_URL,
        connect_timeout=10,
        row_factory=dict_row,
    )


def init_db():
    """Create the fresh AgroFusion recommendations table."""
    with _connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                n DOUBLE PRECISION NOT NULL,
                p DOUBLE PRECISION NOT NULL,
                k DOUBLE PRECISION NOT NULL,
                temperature DOUBLE PRECISION NOT NULL,
                humidity DOUBLE PRECISION NOT NULL,
                ph DOUBLE PRECISION NOT NULL,
                rainfall DOUBLE PRECISION NOT NULL,
                soil_moisture DOUBLE PRECISION,
                soil_type TEXT,
                growth_stage TEXT,
                recommended_crop TEXT,
                crop_ranking_json JSONB,
                fertilizer_summary TEXT,
                irrigation_advice TEXT
            );
        """)


def save_recommendation(v, soil_type, growth_stage, result):
    with _connect() as con:
        con.execute("""
            INSERT INTO recommendations (
                n, p, k, temperature, humidity, ph, rainfall,
                soil_moisture, soil_type, growth_stage,
                recommended_crop, crop_ranking_json,
                fertilizer_summary, irrigation_advice
            )
            VALUES (
                %(n)s, %(p)s, %(k)s, %(temperature)s,
                %(humidity)s, %(ph)s, %(rainfall)s,
                %(soil_moisture)s, %(soil_type)s, %(growth_stage)s,
                %(recommended_crop)s, %(crop_ranking_json)s,
                %(fertilizer_summary)s, %(irrigation_advice)s
            );
        """, {
            "n": v["N"],
            "p": v["P"],
            "k": v["K"],
            "temperature": v["temperature"],
            "humidity": v["humidity"],
            "ph": v["ph"],
            "rainfall": v["rainfall"],
            "soil_moisture": v["soil_moisture"],
            "soil_type": soil_type,
            "growth_stage": growth_stage,
            "recommended_crop": result["crop"],
            "crop_ranking_json": psycopg.types.json.Jsonb(
                result["ranking"]
            ),
            "fertilizer_summary": result["fertilizer"],
            "irrigation_advice": result["irrigation"]["advice"],
        })


def recent_recommendations(limit=8):
    with _connect() as con:
        rows = con.execute("""
            SELECT
                id,
                to_char(
                    created_at AT TIME ZONE 'UTC',
                    'YYYY-MM-DD"T"HH24:MI:SS'
                ) AS created_at,
                recommended_crop,
                soil_type,
                growth_stage
            FROM recommendations
            ORDER BY id DESC
            LIMIT %s;
        """, (limit,)).fetchall()

        return rows
