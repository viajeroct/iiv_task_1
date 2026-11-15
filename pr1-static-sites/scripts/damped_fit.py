"""Аппроксимация затухающих колебаний и сохранение графика для сайта."""
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)


def model(t, a, lam, om, ph):
    return a * np.exp(-lam * t) * np.cos(om * t + ph)


rng = np.random.default_rng(1)
t = np.linspace(0, 12, 26)
x = model(t, 1.0, 0.22, 2.0, 0.0) + rng.normal(0, 0.04, t.size)
popt, pcov = curve_fit(model, t, x, p0=[1.0, 0.2, 2.0, 0.0])
perr = np.sqrt(np.diag(pcov))
print(f"lambda = {popt[1]:.3f} +/- {perr[1]:.3f} c^-1")

tt = np.linspace(0, 12, 400)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.errorbar(t, x, yerr=0.04, fmt="o", ms=4, color="#C8553D", label="измерения")
ax.plot(tt, model(tt, *popt), color="#2E6FAC", lw=2, label="аппроксимация")
ax.plot(tt, abs(popt[0] * np.exp(-popt[1] * tt)), "--", color="#888", lw=1, label="огибающая")
ax.plot(tt, -abs(popt[0] * np.exp(-popt[1] * tt)), "--", color="#888", lw=1)
ax.set_xlabel("t, с")
ax.set_ylabel("x(t), отн. ед.")
ax.set_title("Затухающие колебания: измерения и модель")
ax.grid(alpha=0.25)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(OUT / "damped.png", dpi=200)
print(f"saved {OUT / 'damped.png'}")
