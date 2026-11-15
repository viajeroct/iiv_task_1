# research-stand (ПР4)

Стенд сравнения моделей конкурентности: блокирующая и виртуальные потоки
(пилот). Один и тот же код приложения используется для обеих моделей;
режим выбирается переменной `IMPL` (`blocking` или `virtual`), которая
включает `spring.threads.virtual.enabled`.

## Состав

```
docker-compose.yml     SUT, PostgreSQL, Prometheus, cAdvisor, k6
configs/               pilot.yaml, ci.yaml — факторы, повторения, сид
apps/web/              Spring Boot + Kotlin, Dockerfile
load/script.js         сценарий k6
runner/                оркестрация прогонов и smoke-тест
analysis/              анализ и построение графиков
monitoring/            конфигурация Prometheus
db/init.sql            схема и наполнение БД
```

## Воспроизведение

```bash
make up && make smoke
make experiment CONFIG=configs/pilot.yaml
make analyze
```

Требования: Docker Engine 27 и Compose v2, не менее 4 ядер и 8 ГБ памяти.
Результат: `results/processed/summary.csv`, `tests.csv`, `box.png`.

## Проверка конвейера анализа без стенда

```bash
pip install -r requirements.txt
make synthetic
```

## Манифест прогона

Для каждого прогона в `results/raw` сохраняется JSON-манифест:
параметры, номер повтора, сид, хэш коммита, версии образов,
характеристики машины и время запуска.
