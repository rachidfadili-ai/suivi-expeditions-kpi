"""Genere un jeu de donnees fictif d'expeditions (aucune donnee reelle)."""
import csv, os, random
from datetime import date, datetime, timedelta

CARRIERS = {  # nom: (fiabilite, cout_km_MAD)
    "Transport Atlas": (0.93, 7.5), "Rif Express": (0.85, 6.8),
    "Nord Cargo": (0.78, 6.2), "Med Trans": (0.90, 7.9), "Sahel Logistique": (0.70, 5.9),
}
ROUTES = {  # destination: km
    "Casablanca": 340, "Rabat": 250, "Fes": 300, "Marrakech": 590,
    "Tetouan": 60, "Agadir": 780, "Oujda": 620,
}
FIELDS = ["id", "date_depart", "transporteur", "destination", "km", "poids_kg",
          "livraison_prevue", "livraison_reelle", "cout_mad", "statut"]

def generate(n=500, seed=42, start=date(2026, 1, 1)):
    rnd = random.Random(seed)
    rows = []
    for i in range(1, n + 1):
        car = rnd.choice(list(CARRIERS)); rel, cpk = CARRIERS[car]
        dest = rnd.choice(list(ROUTES)); km = ROUTES[dest]
        dep = datetime.combine(start + timedelta(days=rnd.randint(0, 180)), datetime.min.time()).replace(hour=rnd.randint(5, 16))
        planned = dep + timedelta(hours=km / 60 + 4)
        if rnd.random() < 0.03:
            actual, statut = "", "perdu"
        else:
            late = 0 if rnd.random() < rel else rnd.uniform(1, 30)
            actual = (planned + timedelta(hours=late - rnd.uniform(0, 1))).isoformat(timespec="minutes")
            statut = "livre"
        rows.append({"id": f"EXP{i:05d}", "date_depart": dep.isoformat(timespec="minutes"),
                     "transporteur": car, "destination": dest, "km": km,
                     "poids_kg": rnd.randint(200, 24000),
                     "livraison_prevue": planned.isoformat(timespec="minutes"),
                     "livraison_reelle": actual,
                     "cout_mad": round(km * cpk * rnd.uniform(0.9, 1.15), 2), "statut": statut})
    return rows

def write_csv(rows, path):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)

if __name__ == "__main__":
    write_csv(generate(), "data/expeditions_demo.csv")
    print("data/expeditions_demo.csv genere")
