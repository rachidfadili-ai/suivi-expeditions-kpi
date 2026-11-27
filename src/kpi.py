"""Calcul des KPI transport: OTD, retard moyen, cout/km, score transporteur."""
import csv
from collections import defaultdict
from datetime import datetime

TOLERANCE_H = 1.0  # retard tolere avant de compter "en retard"

def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def delay_hours(row):
    """Retard en heures (negatif = en avance). None si non livre."""
    if row["statut"] != "livre" or not row["livraison_reelle"]:
        return None
    p = datetime.fromisoformat(row["livraison_prevue"])
    a = datetime.fromisoformat(row["livraison_reelle"])
    return (a - p).total_seconds() / 3600

def on_time(row, tol=TOLERANCE_H):
    d = delay_hours(row)
    return None if d is None else d <= tol

def summarize(rows, key=None, tol=TOLERANCE_H):
    groups = defaultdict(list)
    for r in rows:
        groups[r[key] if key else "TOTAL"].append(r)
    out = {}
    for name, rs in groups.items():
        delivered = [r for r in rs if r["statut"] == "livre"]
        delivery_delays = [delay_hours(row) for row in delivered]
        recorded_delays = [delay for delay in delivery_delays if delay is not None]
        ontime = sum(delay <= tol for delay in recorded_delays)
        delays = [delay for delay in recorded_delays if delay > tol]
        km = sum(float(r["km"]) for r in rs)
        cost = sum(float(r["cout_mad"]) for r in rs)
        out[name] = {
            "expeditions": len(rs),
            "livrees": len(delivered),
            "perdues": len(rs) - len(delivered),
            "otd_pct": round(100 * ontime / len(recorded_delays), 1) if recorded_delays else 0.0,
            "retard_moyen_h": round(sum(delays) / len(delays), 1) if delays else 0.0,
            "cout_km_mad": round(cost / km, 2) if km else 0.0,
            "cout_total_mad": round(cost, 2),
        }
    return out

def score(s):
    """Score /100: 70% ponctualite, 20% pertes, 10% retard moyen."""
    loss = s["perdues"] / s["expeditions"] if s["expeditions"] else 0
    pen = min(s["retard_moyen_h"], 30) / 30
    return round(0.7 * s["otd_pct"] + 0.2 * 100 * (1 - min(loss * 10, 1)) + 0.1 * 100 * (1 - pen), 1)

def ranking(rows):
    s = summarize(rows, "transporteur")
    return sorted(((n, v, score(v)) for n, v in s.items()), key=lambda t: -t[2])

def alerts(rows, otd_min=85.0):
    """Transporteurs sous le seuil de ponctualite."""
    return [n for n, v, _ in ranking(rows) if v["otd_pct"] < otd_min]
