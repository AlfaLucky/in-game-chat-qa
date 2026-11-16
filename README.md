# Внутриигровой чат · QA-разбор

Спецификация и 34 тест-кейса по предоставленному макету. В отчёте отмечено, какие элементы видны на скриншоте и какие правила требуют согласования. Прогоны в игровом билде не выполнялись.

- [Сайт GitHub Pages](https://alfalucky.github.io/in-game-chat-qa/)
- [PDF с полным отчётом](docs/in-game-chat-qa.pdf)

## Исходники и локальный просмотр

Тексты, правила и трассировка берутся из `src/report.json`. После редактирования шаблона или данных выполните:

```sh
python3 scripts/build.py
python3 -m http.server 4173 --directory docs
```

Откройте [локальный сайт](http://localhost:4173/). Кнопка «Скачать PDF» выгружает полный отчёт. Для обновления файла после изменения текста откройте страницу в Chrome, вызовите печать, выберите «Сохранить как PDF», формат A4 и отключите колонтитулы браузера. Сохраните результат как `docs/in-game-chat-qa.pdf`.

Сайт публикуется из ветки `main`, папки `/docs`. [Документация GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
