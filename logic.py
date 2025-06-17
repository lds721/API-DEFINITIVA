from typing import List, Dict
from scipy.integrate import quad

# Interés por tramos agresivos
def r(x: float) -> float:
    if x < 20000:
        return 0.020
    elif x < 50000:
        return 0.025
    elif x < 100000:
        return 0.030
    else:
        return 0.035

# Ley financiera compuesta
def F(x: float, t: float) -> float:
    return x * (1 + r(x)) ** t

# Derivada de F(x) respecto a x
def F_prime(x: float, t: float) -> float:
    base = 1 + r(x)
    dr = (r(x + 1e-4) - r(x - 1e-4)) / (2e-4)
    return base ** t + x * t * base ** (t - 1) * dr

# Reparto justo del capítulo 4 del TFG
def reparto_justo_tfg(x1: float, x2: float, t: float) -> List[float]:
    total = x1 + x2
    F_total = F(total, t)

    def integrando(x):
        num = F_prime(2 * x1 + x, t) - F_prime(x1 + x, t)
        den = F(x1, t) + F(x1 + x, t)
        return (num / den) * F(x1, t)

    integral, _ = quad(integrando, 0, x2 - x1, limit=100, epsabs=1e-6)
    reparto1 = F(2 * x1, t) / 2 + integral
    reparto2 = F_total - reparto1

    return [round(reparto1, 2), round(reparto2, 2)]

# Función principal de la API
def calcular_reparto_comparado(x1: float, x2: float, t: float) -> Dict:
    total = x1 + x2
    F_total = round(F(total, t), 2)
    interes = round(r(total), 5)

    reparto_justo = reparto_justo_tfg(x1, x2, t)

    F_ind_1 = round(F(x1, t), 2)
    F_ind_2 = round(F(x2, t), 2)

    return {
        "capital_total": total,
        "interes_aplicado": interes,
        "beneficio_total": F_total,
        "reparto_justo": reparto_justo,
        "beneficio_individual": [F_ind_1, F_ind_2],
        "ganancia_por_cooperar": round(F_total - F_ind_1 - F_ind_2, 2),
        "explicacion": (
            "El reparto justo se calcula aplicando el método del TFG "
            "Se compara con el beneficio que cada inversor habría obtenido si hubiese invertido por separado "
            ". Se elimina el reparto proporcional para centrarse en la equidad real "
            "basada en el impacto marginal de cada aportación sobre el rendimiento total."
        )
    }
