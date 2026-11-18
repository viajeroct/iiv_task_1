# ПР1. Статический сайт на MkDocs

Сайт с результатами ПР1–ПР4: сравнительная матрица генераторов (T1),
страница-стресс-тест научного контента (P2), краткие описания стенда
ПР3/ПР4 и отчёты в формате `.docx`.

## Состав

```
mkdocs.yml                 конфигурация сайта
docs/
  index.md                 главная
  t1.md                    T1: матрица «критерий × генератор»
  p2.md                    P2: формула, таблица, графики, листинг
  pr3.md, pr4.md           описания стенда
  reports.md               ссылки на отчёты
  reports/*.docx           отчёты ПР1–ПР4
  assets/js/mathjax/       MathJax (локально, без CDN)
  assets/js/plotly.min.js  Plotly (локально, без CDN)
  assets/img/damped.png    график matplotlib
  plotly-damped.html       интерактивный график
scripts/
  damped_fit.py            расчёт и статический график
  make_plotly.py           интерактивный график
(workflows лежат в корне репозитория)
.github/workflows/static.yml         сборка и публикация на GitHub Pages
.github/workflows/deploy-helios.yml  ручная публикация на Helios по rsync
```

## Локальная сборка

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python scripts/damped_fit.py
python scripts/make_plotly.py
mkdocs build --strict
mkdocs serve
```

`--strict` превращает битые ссылки и предупреждения в ошибку сборки —
именно этот режим используется в CI.

## Публикация

- **GitHub Pages** — автоматически из `.github/workflows/static.yml`
  при push в `main`. В настройках репозитория: Pages → Source =
  GitHub Actions. Сайт собирается в `pr1-static-sites/site` и
  публикуется в подкаталог `/iiv_task_1/`; базовый URL передаётся
  через переменную `SITE_URL`.
- **Helios ИТМО** — вручную или через `.github/workflows/deploy-helios.yml`
  (`workflow_dispatch`, нужны секреты `HELIOS_HOST`, `HELIOS_PORT`,
  `HELIOS_USER`, `HELIOS_SSH_KEY`, `HELIOS_KNOWN_HOSTS`). Сайт
  размещается в `~/public_html`, адрес — <https://se.ifmo.ru/~s334969/>.

Базовый URL задан в `mkdocs.yml` через `!ENV [SITE_URL, ...]`: по
умолчанию используется адрес на Helios, в CI для GitHub Pages
подставляется адрес подкаталога. Пути к ресурсам в собранном сайте
относительные, поэтому один и тот же билд работает в обоих местах.

## Лицензии

- код и конфигурации — MIT (`LICENSE`);
- тексты, иллюстрации и данные — CC BY 4.0 (`LICENSE-CONTENT`).
