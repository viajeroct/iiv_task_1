"""МОДЕЛЬНЫЕ данные пилота (не измерения!). Сид 20261023. Помечаются synthetic=true."""
import json
from pathlib import Path
import numpy as np
RAW = Path(__file__).resolve().parents[1] / "results/raw"; RAW.mkdir(parents=True, exist_ok=True)
for f in RAW.glob("*.json"): f.unlink()
rng = np.random.default_rng(20261023)
T = {("blocking", 200): (42.5, 5.1), ("virtual", 200): (40.0, 2.4), ("blocking", 500): (303.0, 41.0), ("virtual", 500): (112.6, 6.7)}
plan = [(i, u, r) for i in ("blocking", "virtual") for u in (200, 500) for r in range(10)]
rng.shuffle(plan)
for order, (i, u, r) in enumerate(plan, 1):
    m, iqr = T[(i, u)]
    rid = f"{i}_u{u}_r{r}_syn{order:02d}"
    (RAW / f"{rid}.json").write_text(json.dumps({"run_id": rid, "params": {"impl": i, "users": u}, "repetition": r, "order": order,
        "p95": float(max(5, rng.normal(m, iqr / 1.35))), "synthetic": True}, indent=1))
print("written", len(plan), "synthetic runs")
