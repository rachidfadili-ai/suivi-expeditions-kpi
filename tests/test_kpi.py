import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from kpi import delay_hours, on_time, summarize, score, alerts
from generate import generate
from report import build

def row(prev, reel, statut="livre", car="A", km=100, cout=700):
    return {"statut": statut, "livraison_prevue": prev, "livraison_reelle": reel,
            "transporteur": car, "km": km, "cout_mad": cout}

class T(unittest.TestCase):
    def test_delay(self):
        self.assertEqual(delay_hours(row("2026-01-01T10:00", "2026-01-01T12:30")), 2.5)
        self.assertEqual(delay_hours(row("2026-01-01T10:00", "2026-01-01T09:00")), -1.0)
    def test_lost_has_no_delay(self):
        self.assertIsNone(delay_hours(row("2026-01-01T10:00", "", "perdu")))
        self.assertIsNone(on_time(row("2026-01-01T10:00", "", "perdu")))
    def test_tolerance(self):
        self.assertTrue(on_time(row("2026-01-01T10:00", "2026-01-01T11:00")))
        self.assertFalse(on_time(row("2026-01-01T10:00", "2026-01-01T11:01")))
    def test_summary(self):
        rows = [row("2026-01-01T10:00", "2026-01-01T10:00"), row("2026-01-01T10:00", "2026-01-01T15:00"),
                row("2026-01-01T10:00", "", "perdu")]
        s = summarize(rows)["TOTAL"]
        self.assertEqual((s["expeditions"], s["livrees"], s["perdues"]), (3, 2, 1))
        self.assertEqual(s["otd_pct"], 50.0); self.assertEqual(s["retard_moyen_h"], 5.0)
        self.assertEqual(s["cout_km_mad"], 7.0)
    def test_score_bounds(self):
        s = summarize([row("2026-01-01T10:00", "2026-01-01T10:00")])["TOTAL"]
        self.assertEqual(score(s), 100.0)
    def test_generate_deterministic(self):
        self.assertEqual(generate(50, 1), generate(50, 1))
        self.assertEqual(len(generate(50)), 50)
    def test_alerts_and_report(self):
        rows = generate(400)
        self.assertIsInstance(alerts(rows), list)
        self.assertIn("Classement transporteurs", build(rows))
    def test_weak_carrier_flagged(self):
        self.assertIn("Sahel Logistique", alerts(generate(1000)))

if __name__ == "__main__":
    unittest.main()
