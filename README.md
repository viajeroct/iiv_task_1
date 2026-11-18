# pyweb2025 — практические работы

Материалы по курсу «Проектирование и развёртывание веб-решений
в экосистеме Python»: статический сайт, агент на VPS, проект
и реализация экспериментального стенда.

Опубликованные сайты:

- Helios ИТМО — <https://se.ifmo.ru/~s334969/>
- GitHub Pages — <https://viajeroct.github.io/iiv_task_1/>

## Состав

| Каталог | Работа | Что внутри |
|---|---|---|
| [`pr1-static-sites`](pr1-static-sites) | ПР1 | MkDocs-сайт, T1 и P2, CI GitHub Actions, деплой на Helios |
| [`pr2-agent`](pr2-agent) | ПР2 | `compose.yaml` для Hermes Agent, навык, конфигурация окружения |
| [`pr3-stand-design`](pr3-stand-design) | ПР3 | отчёт по проектированию стенда: статьи, RQ, гипотезы, план |
| [`pr4-research-stand`](pr4-research-stand) | ПР4 | Docker Compose, Kotlin SUT, k6, раннер, анализ |
| [`reports`](reports) | ПР1–ПР4 | отчёты в формате `.docx` |

## Быстрый старт

### ПР1 — сайт

```bash
cd pr1-static-sites
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python scripts/damped_fit.py && python scripts/make_plotly.py
mkdocs build --strict
mkdocs serve
```

### ПР2 — агент

```bash
cd pr2-agent
cp .env.example .env      # заполнить токен Telegram и ключ LLM
docker compose up -d
docker compose logs -f
```

Навык ежедневного дайджеста публикаций — `pr2-agent/skills/daily-digest.md`.

### ПР4 — стенд

```bash
cd pr4-research-stand
make up && make smoke
make experiment CONFIG=configs/pilot.yaml
make analyze
```

Параметры эксперимента — в `configs/*.yaml`; каждый прогон сохраняет
сырые данные и JSON-манифест в `results/raw`.

## Публикация

| Площадка | Workflow | Триггер |
|---|---|---|
| GitHub Pages | `.github/workflows/static.yml` | push в `main` |
| Helios ИТМО | `.github/workflows/deploy-helios.yml` | `workflow_dispatch` |

Оба workflow собирают сайт из `pr1-static-sites` в режиме
`mkdocs build --strict`. Для Helios нужны секреты `HELIOS_HOST`,
`HELIOS_PORT`, `HELIOS_USER`, `HELIOS_SSH_KEY`, `HELIOS_KNOWN_HOSTS`.
Базовый URL передаётся в `mkdocs.yml` через `SITE_URL`: на Helios —
корень пользовательского каталога, на GitHub Pages — подкаталог
`/iiv_task_1/`.

## Лицензии

Код и конфигурации — MIT (`pr1-static-sites/LICENSE`).
Тексты и иллюстрации — CC BY 4.0 (`pr1-static-sites/LICENSE-CONTENT`).
