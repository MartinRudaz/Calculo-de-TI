from __future__ import annotations

from datetime import datetime, timezone
import json
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from TI import calculate_transformer_values

DB_PATH = Path(__file__).resolve().parent / "calculations.db"

app = FastAPI(title="Calculo de Transformadores de Corriente")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TransformerInput(BaseModel):
    txt: float = Field(..., description="Prestacion")
    txt2: float = Field(..., description="Corriente Primaria")
    txt3: float = Field(..., description="Corriente Secundaria")
    txt4: float = Field(..., description="FS")
    txt5: float = Field(..., description="Frecuencia")
    txt6: float = Field(..., description="Factor de Apilado")
    txt7: float = Field(..., description="Diam. Conductor")
    txt8: float = Field(..., description="Diam. Interno")
    txt9: float = Field(..., description="Espiras")
    txt10: float = Field(..., description="PF")
    txt11: float = Field(..., description="Ancho de Fleje")
    txt12: float = Field(..., description="Apilado")


class CalculationRecord(BaseModel):
    id: int
    created_at: str
    inputs: TransformerInput
    results: dict


def _db_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _init_db() -> None:
    with _db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                inputs_json TEXT NOT NULL,
                results_json TEXT NOT NULL
            )
            """
        )


@app.on_event("startup")
def startup_event() -> None:
    _init_db()


def _save_calculation(input_data: TransformerInput, results: dict) -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    with _db_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO calculations (created_at, inputs_json, results_json) VALUES (?, ?, ?)",
            (created_at, input_data.model_dump_json(), json.dumps(results)),
        )
        return int(cursor.lastrowid)


@app.post("/calculate")
async def calculate_transformer(input_data: TransformerInput):
    try:
        results = calculate_transformer_values(**input_data.model_dump())
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    calculation_id = _save_calculation(input_data, results)
    return {
        "id": calculation_id,
        "inputs": input_data,
        "results": results,
    }


@app.get("/calculations", response_model=list[CalculationRecord])
async def get_calculations(limit: int = 20):
    max_items = max(1, min(limit, 100))

    with _db_connection() as conn:
        rows = conn.execute(
            "SELECT id, created_at, inputs_json, results_json FROM calculations ORDER BY id DESC LIMIT ?",
            (max_items,),
        ).fetchall()

    records = []
    for row in rows:
        records.append(
            CalculationRecord(
                id=row["id"],
                created_at=row["created_at"],
                inputs=TransformerInput.model_validate_json(row["inputs_json"]),
                results=json.loads(row["results_json"]),
            )
        )
    return records
