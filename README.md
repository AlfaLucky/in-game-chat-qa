# Внутриигровой чат · QA-разбор

Разбор макета чата «Кафе» и 34 тест-кейса. Описание интерфейса основано на скриншоте из задания. Правила работы чата, которые нужно уточнить, отмечены в отчёте. На игровом билде кейсы не запускали.

- Русский: [сайт](https://alfalucky.github.io/in-game-chat-qa/) · [PDF](docs/in-game-chat-qa.pdf)
- English: [site](https://alfalucky.github.io/in-game-chat-qa/en/) · [PDF](docs/en/in-game-chat-qa-en.pdf)

## Исходники и локальный просмотр

Русский отчёт и связи между правилами и кейсами находятся в `src/report.json`, перевод — в `src/report.en.json`. Подписи и навигация для обоих языков находятся в `src/interface.json`. После редактирования шаблона или данных выполните:

```sh
python3 scripts/build.py
python3 -m http.server 4173 --directory docs
```

Откройте [локальный сайт](http://localhost:4173/). Переключатель RU / EN открывает отчёт на выбранном языке. Кнопка скачивания выгружает PDF этой версии. Чтобы обновить PDF после правок, откройте нужную страницу в Chrome, вызовите печать, выберите «Сохранить как PDF», формат A4 и отключите колонтитулы браузера. Сохраните русский PDF в `docs/in-game-chat-qa.pdf`, английский — в `docs/en/in-game-chat-qa-en.pdf`.

Сайт публикуется из ветки `main`, папки `/docs`. [Документация GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
