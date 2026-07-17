# anki-cloze-cards

**English** · [Русский](#русский)

An [agent skill](https://docs.claude.com/en/docs/claude-code/skills) for [Claude Code](https://claude.com/claude-code) that turns any English word, phrase, idiom, collocation, or phrasal verb into a ready-to-import **Anki cloze card in context** — built for Russian-speaking learners (B1–C1).

Drop a word into the chat — get a TSV file for Anki:

```
> разбери слово oatmeal
✓ Saved: new_words/oatmeal.tsv (1 meaning), added to All_Words.csv
```

## Why cloze-in-context

The card trains **production, not translation**:

- **Front** — a natural sentence with a gap: `{{c1::oatmeal::o___ cooked oats}}`. You recall the word inside living context; the hint (first letter + a short English cue) narrows the answer to exactly one form.
- **Back** — definition, part of speech and irregular forms, IPA (BrE + AmE), collocations, a block of 3–6+ varied examples, and an image-association prompt.
- **Russian translations** (of the sentence, the definition, every example, and the word itself) are on the back **behind collapsible spoilers** — a safety net you open only when stuck, so the card stays monolingual-first.

## What the skill handles

- **Deduplication** — every request is first checked against `All_Words.csv`, the running dictionary of everything you've already studied. A repeated word never produces a second card.
- **Polysemy** — a word with several important meanings gets one card per meaning, all rows in a single file.
- **Contrast pairs** (*interesting / interested*, *affect / effect*, *say / tell*) — two separate cards in natural sentences where only one form fits, with the contrast explained on the back (`✗ … → ✓ …` examples).
- **Phrasal verbs** — the card stores the government pattern (*claw sth back*) and marks separability.
- **Slang and non-standard senses** — flagged explicitly (*slang*, *vulgar*, *internet*, *old-fashioned*) with the source when it isn't Cambridge.
- **Clean chat** — the card itself never appears in the chat, only a short confirmation; the single artifact is the TSV file.

## Installation

Clone into your skills folder — personal or per-project:

```bash
# available in every project
git clone https://github.com/CompleWin/anki-cloze-cards ~/.claude/skills/anki-cloze-cards

# or for a single project only
git clone https://github.com/CompleWin/anki-cloze-cards <project>/.claude/skills/anki-cloze-cards
```

That's it — Claude Code picks the skill up automatically whenever you ask for a card or simply drop an English word into the chat.

## Anki setup (one time)

1. Install the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on (Tools → Add-ons → Get Add-ons → code `2055492159`) and restart Anki.
2. With Anki running, execute:

   ```bash
   python scripts/create_anki_notetype.py
   ```

   This creates the **"Cloze EN Helper"** note type: 13 fields, spoiler-styled Russian fields, dark-mode support. Re-running the script updates the template and styling in place.

## Importing cards

Import `new_words/*.tsv` with Anki's standard importer:

| Setting | Value |
|---------|-------|
| Note type | Cloze EN Helper |
| Field separator | Tab |
| Allow HTML in fields | ON |
| Columns 1–13 | fields in order (Target, Sentence, SentenceRU, Definition, DefinitionRU, Form, IPA, Collocations, Example2, Example2RU, RU, Image, ImagePrompt) |
| Column 14 | Tags |

The Image field arrives empty by design — add your own picture after import, using the ImagePrompt text shown on the back of the card.

## Repository structure

```
anki-cloze-cards/
├── SKILL.md                          # the skill: workflow + card rules (in Russian)
├── references/
│   └── card-template.md              # full field spec, reference cards, TSV conversion table
├── scripts/
│   └── create_anki_notetype.py       # one-time note type setup via AnkiConnect
└── evals/
    └── evals.json                    # test cases the skill was validated against
```

In your working folder the skill creates and maintains:

```
All_Words.csv    # dictionary of everything studied (dedup source of truth)
new_words/       # one .tsv per word — files ready for Anki import
```

## Requirements

- [Claude Code](https://claude.com/claude-code)
- Anki + [AnkiConnect](https://ankiweb.net/shared/info/2055492159) (only for the one-time note type setup)
- Python 3 (only for the setup script)

## License

[MIT](LICENSE)

---

# Русский

Агентский [скилл](https://docs.claude.com/en/docs/claude-code/skills) для [Claude Code](https://claude.com/claude-code): превращает любое английское слово, фразу, идиому, коллокацию или фразовый глагол в готовую **cloze-карточку Anki в контексте** — для русскоязычного ученика уровня B1–C1.

Кидаешь слово в чат — получаешь файл на импорт в Anki:

```
> разбери слово oatmeal
✓ Сохранено: new_words/oatmeal.tsv (1 значение), слово добавлено в All_Words.csv
```

## Почему cloze-в-контексте

Карточка тренирует **продакшн, а не перевод**:

- **Лицевая сторона** — живое предложение с пропуском: `{{c1::oatmeal::o___ cooked oats}}`. Слово вспоминается внутри контекста; подсказка (первая буква + короткий английский ориентир) сужает ответ до единственной формы.
- **Оборот** — определение, часть речи и неправильные формы, IPA (BrE + AmE), коллокации, блок из 3–6+ разнообразных примеров и промпт картинки-ассоциации.
- **Русские переводы** (предложения, определения, всех примеров и самого слова) — на обороте **под раскрывающимися спойлерами**: страховка, которую открываешь, только если завис. Карточка остаётся monolingual-first.

## Что умеет скилл

- **Защита от дублей** — каждый запрос сначала проверяется по `All_Words.csv`, общему словарю всего уже разобранного. Повторное слово второй карточки не создаст.
- **Многозначность** — слово с несколькими важными значениями получает по карточке на значение, все строки в одном файле.
- **Контрастные пары** (*interesting / interested*, *affect / effect*, *say / tell*) — две отдельные карточки в естественных предложениях, где подходит только одна форма; контраст объясняется на обороте (примеры «✗ … → ✓ …»).
- **Фразовые глаголы** — карточка хранит шаблон управления (*claw sth back*) и помечает разделяемость.
- **Сленг и нестандартные значения** — помечаются явно (*slang*, *vulgar*, *internet*, *old-fashioned*), с источником, если это не Cambridge.
- **Чистый чат** — сама карточка в чат никогда не выводится, только короткое подтверждение; единственный артефакт — TSV-файл.

## Установка

Склонируй репозиторий в папку скиллов — личную или проектную:

```bash
# для всех проектов
git clone https://github.com/CompleWin/anki-cloze-cards ~/.claude/skills/anki-cloze-cards

# или только для одного проекта
git clone https://github.com/CompleWin/anki-cloze-cards <проект>/.claude/skills/anki-cloze-cards
```

Всё — Claude Code подхватывает скилл автоматически, когда просишь карточку или просто кидаешь английское слово в чат.

## Настройка Anki (один раз)

1. Установи аддон [AnkiConnect](https://ankiweb.net/shared/info/2055492159) (Tools → Add-ons → Get Add-ons → код `2055492159`) и перезапусти Anki.
2. При запущенном Anki выполни:

   ```bash
   python scripts/create_anki_notetype.py
   ```

   Скрипт создаст note type **«Cloze EN Helper»**: 13 полей, русские поля под спойлерами, поддержка тёмной темы. Повторный запуск обновляет шаблон и стили на месте.

## Импорт карточек

Файлы `new_words/*.tsv` импортируются штатным импортом Anki:

| Настройка | Значение |
|-----------|----------|
| Note type | Cloze EN Helper |
| Разделитель полей | Tab |
| Allow HTML in fields | ON |
| Колонки 1–13 | поля по порядку (Target, Sentence, SentenceRU, Definition, DefinitionRU, Form, IPA, Collocations, Example2, Example2RU, RU, Image, ImagePrompt) |
| Колонка 14 | Tags |

Поле Image приходит пустым намеренно — картинку добавляешь сам после импорта, ориентируясь на текст ImagePrompt на обороте карточки.

## Структура репозитория

```
anki-cloze-cards/
├── SKILL.md                          # сам скилл: рабочий цикл + правила карточки
├── references/
│   └── card-template.md              # полная спецификация полей, эталоны, таблица конверсии в TSV
├── scripts/
│   └── create_anki_notetype.py       # однократная настройка note type через AnkiConnect
└── evals/
    └── evals.json                    # тест-кейсы, на которых скилл проверялся
```

В рабочей папке пользователя скилл создаёт и ведёт:

```
All_Words.csv    # словарь всего разобранного (источник истины для проверки дублей)
new_words/       # по одному .tsv на слово — файлы на импорт
```

## Требования

- [Claude Code](https://claude.com/claude-code)
- Anki + [AnkiConnect](https://ankiweb.net/shared/info/2055492159) (только для однократной настройки note type)
- Python 3 (только для скрипта настройки)

## Лицензия

[MIT](LICENSE)
