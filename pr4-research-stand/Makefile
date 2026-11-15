CONFIG ?= configs/experiment.yaml
up:         ; docker compose up -d db prometheus cadvisor
smoke:      ; python3 runner/smoke.py
experiment: ; python3 runner/run_experiment.py --config $(CONFIG)
analyze:    ; python3 analysis/analyze.py
synthetic:  ; python3 analysis/synthetic_pilot.py && python3 analysis/analyze.py
down:       ; docker compose down -v
