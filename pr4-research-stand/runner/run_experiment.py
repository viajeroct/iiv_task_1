"""Оркестрация прогонов: план x повторения, рандомизация по сиду, манифест на каждый прогон."""
import argparse, itertools, json, os, platform, random, subprocess, time, uuid
from datetime import datetime, timezone
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(); ap.add_argument("--config", default="configs/experiment.yaml")
cfg = yaml.safe_load((ROOT / ap.parse_args().config).read_text())
def sh(*a, env=None):
    return subprocess.run(a, check=True, capture_output=True, text=True, cwd=ROOT, env={**os.environ, **(env or {})}).stdout.strip()
def k6(users, seconds, prefix):
    sh("docker", "compose", "--profile", "run", "run", "--rm", "-e", f"USERS={users}", "-e", f"SECONDS={seconds}", "load",
       "run", "--summary-export", f"/results/{prefix}_summary.json", "/scripts/script.js")
plan = [dict(zip(cfg["factors"], c), rep=r) for c in itertools.product(*cfg["factors"].values()) for r in range(cfg["repetitions"])]
if cfg.get("randomize_order"): random.Random(cfg["seed"]).shuffle(plan)
out = ROOT / "results/raw"; out.mkdir(parents=True, exist_ok=True)
for i, p in enumerate(plan, 1):
    run_id = f"{p['impl']}_u{p['users']}_r{p['rep']}_{uuid.uuid4().hex[:6]}"
    print(f"[{i}/{len(plan)}] {run_id}", flush=True)
    sh("docker", "compose", "up", "-d", "--force-recreate", "--build", "db", "sut", env={"IMPL": p["impl"]})
    time.sleep(10)
    k6(p["users"], cfg["warmup_seconds"], f"warmup_{run_id}")   # прогрев, в анализ не идёт
    k6(p["users"], cfg["duration_seconds"], run_id)
    m = json.loads((out / f"{run_id}_summary.json").read_text())["metrics"]["http_req_duration"]
    man = {"run_id": run_id, "params": {"impl": p["impl"], "users": p["users"]}, "repetition": p["rep"], "order": i,
           "seed": cfg["seed"], "p95": m["p(95)"], "p50": m["med"], "synthetic": False,
           "git_commit": sh("git", "rev-parse", "HEAD") if (ROOT / ".git").exists() else None,
           "images": sh("docker", "compose", "images", "--format", "json"),
           "host": {"os": platform.platform(), "cpu_count": os.cpu_count(), "machine": platform.machine()},
           "started_at": datetime.now(timezone.utc).isoformat()}
    (out / f"{run_id}.json").write_text(json.dumps(man, indent=2))
    time.sleep(cfg.get("pause_between_runs_seconds", 10))
