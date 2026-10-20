# Павел Насута — персональный сайт

Статический сайт для GitHub Pages.

## Локальный просмотр

```bash
cd /Users/pavelnasuta/pavel-nasuta-site
python3 -m http.server 8080
```

Открыть `http://localhost:8080`.

## Структура

- `index.html` — главная;
- `create/` — C.R.E.A.T.E.;
- `articles/` — архив и статьи;
- `biases/` — каталог когнитивных искажений и карточки материалов;
- `skills/` — Skill Hub: публичный каталог, карточки навыков и генерация из реестра;
- `data/skills.json` — источник данных Skill Hub; после изменения запускать `python tools/build_skills.py --root . --registry data/skills.json`;
- `about/` — об авторе;
- `contact/` — Telegram как публичный канал связи;
- `assets/` — изображения, стили и JavaScript.

## SEO

SEO относится к каждой индексируемой странице и обновляется вместе с её содержанием. Для новой или изменённой страницы обязательны: уникальные `title`, H1, description, canonical на `https://nasuta.ru`, Open Graph и Twitter metadata, корректный JSON-LD, внутренняя ссылка и запись в `sitemap.xml`. `404.html` остаётся `noindex,follow`.
