"""Genere un rapport HTML autonome (sans dependance)."""
import sys
from html import escape
from kpi import load, summarize, ranking, alerts

def table(headers, rows):
    h = "".join(f"<th>{escape(x)}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{escape(str(c))}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><tr>{h}</tr>{b}</table>"

def bars(items):
    return "".join(
        f'<div class="b"><span>{escape(n)}</span><i style="width:{v}%"></i><em>{v}%</em></div>' for n, v in items)

def build(rows):
    if not rows:
        return ('<!doctype html><html lang="fr"><meta charset="utf-8">'
                '<title>KPI Transport</title><h1>Tableau de bord KPI transport</h1>'
                '<p>Aucune expédition dans le fichier CSV.</p></html>')
    tot = summarize(rows)["TOTAL"]
    rk = ranking(rows)
    dest = summarize(rows, "destination")
    al = alerts(rows)
    cards = "".join(f'<div class="c"><b>{v}</b><small>{k}</small></div>' for k, v in [
        ("Expeditions", tot["expeditions"]), ("Ponctualite (OTD)", f'{tot["otd_pct"]}%'),
        ("Retard moyen", f'{tot["retard_moyen_h"]} h'), ("Cout / km", f'{tot["cout_km_mad"]} MAD'),
        ("Perdues", tot["perdues"])])
    alert = ("<p class='a'>Alerte: " + ", ".join(escape(name) for name in al) + " sous 85% de ponctualite.</p>") if al else ""
    return f"""<!doctype html><meta charset="utf-8"><title>KPI Transport</title>
<style>body{{font:15px system-ui;margin:2rem auto;max-width:900px;color:#1d2433}}
.c{{display:inline-block;background:#eef3fb;border-radius:10px;padding:12px 18px;margin:4px}}
.c b{{display:block;font-size:22px}}table{{border-collapse:collapse;width:100%;margin:1rem 0}}
td,th{{border-bottom:1px solid #dde;padding:6px;text-align:left}}.a{{color:#b3261e;font-weight:600}}
.b{{display:flex;align-items:center;gap:8px;margin:3px 0}}.b span{{width:150px}}
.b i{{height:12px;background:#2f6fdb;border-radius:6px;display:block}}</style>
<h1>Tableau de bord KPI transport</h1><p>Donnees fictives de demonstration.</p>{cards}{alert}
<h2>Ponctualite par transporteur</h2>{bars([(n, v["otd_pct"]) for n, v, _ in rk])}
<h2>Classement transporteurs</h2>{table(["Transporteur","Livrees","OTD %","Retard moyen h","Cout/km MAD","Perdues","Score"],
 [(n, v["livrees"], v["otd_pct"], v["retard_moyen_h"], v["cout_km_mad"], v["perdues"], s) for n, v, s in rk])}
<h2>Par destination</h2>{table(["Destination","Expeditions","OTD %","Cout/km MAD"],
 [(n, v["expeditions"], v["otd_pct"], v["cout_km_mad"]) for n, v in sorted(dest.items())])}"""

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "data/expeditions_demo.csv"
    out = sys.argv[2] if len(sys.argv) > 2 else "rapport.html"
    open(out, "w", encoding="utf-8").write(build(load(src)))
    print(out, "genere")
