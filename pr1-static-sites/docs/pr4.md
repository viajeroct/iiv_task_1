# ПР4. Реализация экспериментального стенда

## Архитектура

```text
┌──────────────────── docker compose ────────────────────┐
│                                                        │
│  k6 (генератор) ──HTTP──▶ SUT: Spring Boot + Kotlin    │
│                              │                         │
│                              ▼                         │
│                        PostgreSQL 16                   │
│                                                        │
│  Prometheus ──scrape──▶ SUT /actuator/prometheus        │
│  cAdvisor   ──scrape──▶ контейнеры                      │
│                                                        │
│  results/raw (JSON-манифесты) ──▶ analysis/analyze.py  │
└────────────────────────────────────────────────────────┘
```

Один и тот же код приложения используется для обеих моделей: режим
выбирается переменной `IMPL` (`blocking` или `virtual`), которая
включает `spring.threads.virtual.enabled`.

## Компоненты

| Компонент | Технология | Версия |
|---|---|---|
| SUT | Spring Boot + Kotlin, JDK 21 | 3.3.5 / Kotlin 2.0.21 |
| БД | PostgreSQL | 16.4 |
| Нагрузка | Grafana k6 | 0.54.0 |
| Метрики | Prometheus + cAdvisor | 2.54.1 / 0.49.1 |
| Анализ | Python: numpy, pandas, scipy, matplotlib | см. `requirements.txt` |

## Запуск

```bash
make up
make smoke
make experiment CONFIG=configs/pilot.yaml
make analyze
```

Параметры вынесены в `configs/pilot.yaml`: факторы, уровни, число
повторений, прогрев, длительность, сид и пауза между прогонами.
Каждый прогон сохраняет в `results/raw` JSON-манифест с параметрами,
номером повтора, сидом, хэшем коммита, версиями образов и
характеристиками машины.

## Анализ {#analysis}

`analysis/analyze.py` считает медиану, IQR, bootstrap-интервал,
тест Манна–Уитни, δ Клиффа и поправку Холма, а также строит boxplot.
Единица наблюдения — p95 одного прогона, поэтому n равно числу
повторений, а не числу запросов.

```bash
make analyze
# results/processed/summary.csv
# results/processed/tests.csv
# results/processed/box.png
```

Проверка конвейера анализа без запуска стенда:

```bash
make synthetic
```

Полная инструкция — в `README.md` репозитория и в отчёте по ПР4.
