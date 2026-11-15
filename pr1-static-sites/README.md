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
.github/workflows/
  deploy.yml               сборка и публикация на GitHub Pages
  deploy-helios.yml        ручная публикация на Helios по rsync
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

- **GitHub Pages** — автоматически из `.github/workflows/deploy.yml`
  при push в `main`. В настройках репозитория: Pages → Source =
  GitHub Actions.
- **Helios ИТМО** — вручную или через `deploy-helios.yml`
  (`workflow_dispatch`). Сайт размещается в `~/public_html`, адрес —
  <https://se.ifmo.ru/~s334969/>.

Для Helios базовый URL задан в `site_url`; сайт размещён в корне
пользовательского каталога, поэтому пути к ресурсам остаются
относительными.

## Лицензии

- код и конфигурации — MIT (`LICENSE`);
- тексты, иллюстрации и данные — CC BY 4.0 (`LICENSE-CONTENT`).
