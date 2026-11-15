"""Анализ: медиана, IQR, bootstrap-интервал, Манн-Уитни, дельта Клиффа, поправка Холма."""
import json
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]; RAW = ROOT / "results/raw"; OUT = ROOT / "results/processed"; OUT.mkdir(parents=True, exist_ok=True)
rows = []
for m in RAW.glob("*.json"):
    d = json.loads(m.read_text())
    if "p95" in d: rows.append({**d["params"], "rep": d["repetition"], "order": d.get("order"), "p95": d["p95"], "synthetic": d.get("synthetic", False)})
df = pd.DataFrame(rows); df.to_csv(OUT / "runs.csv", index=False)
if df.synthetic.any(): print("ВНИМАНИЕ: в данных есть МОДЕЛЬНЫЕ прогоны (synthetic=true)")
def ci(x):
    r = stats.bootstrap((np.asarray(x),), np.median, confidence_level=.95, random_state=0)
    return round(r.confidence_interval.low, 1), round(r.confidence_interval.high, 1)
summ = df.groupby(["impl", "users"])["p95"].agg(n="count", median="median", iqr=lambda s: s.quantile(.75) - s.quantile(.25)).reset_index()
summ["ci95"] = [ci(df[(df.impl == r.impl) & (df.users == r.users)].p95) for r in summ.itertuples()]
summ.to_csv(OUT / "summary.csv", index=False); print(summ.round(1))
tests = []
for u, g in df.groupby("users"):
    a = g[g.impl == "blocking"].p95.values; b = g[g.impl == "virtual"].p95.values
    _, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    tests.append({"users": u, "diff_pct": (np.median(a) - np.median(b)) / np.median(a) * 100, "p": p, "cliffs_delta": np.sign(np.subtract.outer(a, b)).mean()})
t = pd.DataFrame(tests).sort_values("p").reset_index(drop=True); m = len(t); prev = 0; ph = []
for k, p in enumerate(t.p):                      # поправка Холма
    prev = max(prev, min(1, (m - k) * p)); ph.append(prev)
t["p_holm"] = ph; t.to_csv(OUT / "tests.csv", index=False); print(t.round(5))
fig, ax = plt.subplots(figsize=(7, 4)); pos = 0; ticks = []; labs = []
for u in sorted(df.users.unique()):
    for i in ("blocking", "virtual"):
        x = df[(df.impl == i) & (df.users == u)].p95.values; ax.boxplot(x, positions=[pos], widths=.5, showfliers=False)
        ax.scatter(np.full(len(x), pos), x, s=12, zorder=3); ticks.append(pos); labs.append(f"{i}\n{u} VU"); pos += 1
ax.set_xticks(ticks); ax.set_xticklabels(labs); ax.set_ylabel("p95, мс"); fig.tight_layout(); fig.savefig(OUT / "box.png", dpi=200)
