from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from logic import calcular_reparto_comparado

app = FastAPI(title="API Reparto Justo según TFG (sin proporcional)")

class Entrada(BaseModel):
    x1: float
    x2: float
    tiempo: float

@app.post("/reparto_comparado/")
def reparto_comparado(entrada: Entrada) -> Dict:
    return calcular_reparto_comparado(entrada.x1, entrada.x2, entrada.tiempo)
