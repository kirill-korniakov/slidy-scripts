# Slidy TODO

- Implement macroses:
  - `{{toc}}`
  - `{{date}}` автоматически печатать дату генерации слайдов
  - {{author}}

- Build
  - Move `publish-html` to this repo (switch devtools and agile)
  - create and move here travis commands
  - autogenerate list of slides using JS
  - rename `slides-py` to `scripts`
  - create single SSH key for slide publishing
  - learn how to generate and publish PDF using TravisCI

## Validation

- Содержимое
  - Соблюдается единый формат содержания
    (содержание+toc, контрольные вопросы, м.б. ключевые идеи, демонстрация)
  - Проверять, что контрольные вопросы в слайдах и сводном документе совпадают
  - Снести все ссылки в конец Markdown-файлов

- Markdown Checks
  - Каким-то образом валидировать Markdown (<http://habrahabr.ru/post/235611/>)
  - Используются стандартные маркеры списков (- и 1.)
  - Использовать двойное подчеркивание для выделения жирным
  - detect unused links
  - Можно проверять, что картинки имеют стандартную высоту, например 500 пикселов

## Style

- Add line numbers to code
- Add syntax highlighting to code
- Change style for quotes
- implement command for resizing images to standard size
- Заголовки разных уровней должны визуально отличаться друг от друга

## Backlog

- Попробовать интеграцию `reveal.js` с pandoc
- Check <https://code.google.com/p/io-2012-slides/>
- global links and pictures (may be just use a single folder)
- Код
  - В блоках кода должно быть одинаковое выравнивание (4 пробела)
  - По идее можно вырезать все куски кода и проверять их на соответствие
    некоторым общим соглашениям (запускать какие-то тулы)
- Реализовать поддержку
  - plantuml
  - latex formulas
  - Try Graphvis
- Избавиться от папки `graphics`
- Изучить диалект pandoc <http://johnmacfarlane.net/pandoc/demo/example9/pandocs-markdown.html>
