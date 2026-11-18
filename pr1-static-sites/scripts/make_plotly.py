"""Интерактивный график Plotly для сайта: JS подключается локально."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import plotly

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
(ASSETS / "js").mkdir(parents=True, exist_ok=True)

t = np.linspace(0, 12, 26)
rng = np.random.default_rng(1)
lam, om = 0.22, 2.0
x = np.exp(-lam * t) * np.cos(om * t) + rng.normal(0, 0.04, t.size)
tt = np.linspace(0, 12, 400)
y = np.exp(-lam * tt) * np.cos(om * tt)

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=x, mode="markers", name="измерения",
                         error_y=dict(type="constant", value=0.04, visible=True)))
fig.add_trace(go.Scatter(x=tt, y=y, mode="lines", name="аппроксимация"))
fig.update_layout(template="plotly_white", margin=dict(l=40, r=20, t=40, b=40),
                  title="Затухающие колебания (интерактивно)",
                  xaxis_title="t, с", yaxis_title="x(t), отн. ед.",
                  legend=dict(orientation="h", y=1.12))

html = fig.to_html(include_plotlyjs=False, full_html=True)
html = html.replace("</head>", '<script src="assets/js/plotly.min.js"></script></head>')
(ROOT / "docs" / "plotly-damped.html").write_text(html, encoding="utf-8")

pkg = Path(plotly.__file__).resolve().parent / "package_data"
for name in ("plotly-basic.min.js", "plotly.min.js"):
    src = pkg / name
    if src.exists():
        (ASSETS / "js" / "plotly.min.js").write_bytes(src.read_bytes())
        print(f"plotly js: {name}")
        break
else:
    raise SystemExit(f"plotly js not found in {pkg}")

print("saved docs/plotly-damped.html")
