# Шаблон cloze-карточки: поля, эталоны, конверсия в TSV

Этот файл — полная спецификация карточки. Читай его перед сборкой первой карточки в сессии; дальше держи поля в голове.

## Поля и порядок (= порядок колонок TSV)

1. **Target** — headword / лемма (для phrasal verb — шаблон управления: *claw sth back*)
2. **Sentence** — естественное предложение с `{{c1::ответ::англ. подсказка}}`; на лицевой стороне = пропуск
3. **SentenceRU** — русский перевод предложения `Sentence` целиком (с раскрытым ответом). На обороте скрыт под спойлером — страховка, если ученик не понял контекст.
4. **Definition** — короткое определение по-английски (ОДНО значение)
5. **DefinitionRU** — русский перевод поля `Definition`. Под спойлером — на случай незнакомых слов в определении.
6. **Form** — POS / неправильные формы / разделяемость / управление / исчисляемость
7. **IPA** — оба варианта: BrE + AmE
8. **Collocations** — типичные сочетания, разбираемое слово жирным
9. **Example2** — блок из 3–6+ примеров именно этого значения (предложения через `<br>`); для контрастных пар один из них показывает вторую форму
10. **Example2RU** — русский перевод всех примеров из `Example2` (тот же порядок, через `<br>`). Под спойлером.
11. **RU** — краткий перевод самого слова (страховка; под спойлером)
12. **Image** — **всегда пустое**: картинку пользователь вставляет сам после импорта, ориентируясь на ImagePrompt
13. **ImagePrompt** — англ. промпт картинки-ассоциации (картинка рисуется на обороте)
14. **Related** — 2–4 соседа этого значения **из `All_Words.csv`** (синонимы, `<i>opp:</i>`, `<i>cf:</i>`), у каждого короткое англ. различение; если соседей в словаре нет — пустое
15. **MyExample** — **всегда пустое**: своё предложение ученик пишет сам во время review через редактор Anki (клавиша `E`)
16. **Tags** — теги через пробел (последняя колонка; при импорте мапится на Tags Anki)

Русские поля (SentenceRU, DefinitionRU, Example2RU, RU) на обороте отображаются под спойлером `<details>` — это обеспечивает note type (см. `scripts/create_anki_notetype.py`). В TSV кладётся только текст, без всяких `<details>`.

Лицевая сторона, кроме предложения с пропуском, содержит поле ввода (своё JS-поле вместо `{{type:}}` — работает и на AnkiWeb, Enter открывает ответ): ответ **вписывается**, на обороте ошибочные буквы зачёркнуты рядом с правильным ответом. Со стороны генерации это ничего не требует — только естественную подсказку, по которой ответ восстанавливается однозначно.

## Эталон (markdown) — внутренняя рабочая модель

В чат НЕ выводится; из него механически собирается TSV-строка.

```markdown
### Target
**claw back** — phrasal verb

### Sentence
`Verstappen managed to {{c1::claw back::c___ b___ recover gradually}} the eight-second gap over the final stint.`

### SentenceRU
Ферстаппен сумел отыграть восьмисекундный отрыв на последнем отрезке гонки.

### Definition
To gradually recover something you had lost — a lead, a deficit, money — through steady, deliberate effort.

### DefinitionRU
Постепенно вернуть то, что было потеряно — преимущество, отставание, деньги — за счёт упорных, целенаправленных усилий.

### Form
Phrasal verb · separable · *claw sth back* / *claw back sth* · с местоимением объект в середине: *claw it back*.

### IPA
/klɔː bæk/ (BrE), /klɑː bæk/ (AmE)

### Collocations
**claw back** a deficit / a gap / lost ground · **claw** the gap **back** · **claw back** losses

### Example2
The government is trying to **claw back** overpaid benefits.
After a disastrous first half, the team slowly **clawed back** the deficit to draw 3–3.
It took years of austerity to **claw back** the money lost in the crisis.
She **clawed** her way **back** into contention after falling to last place.

### Example2RU
Правительство пытается вернуть переплаченные пособия.
После провального первого тайма команда медленно отыграла отставание и свела матч вничью 3:3.
Понадобились годы жёсткой экономии, чтобы вернуть деньги, потерянные в кризис.
Она пробилась обратно в борьбу за победу, опустившись было на последнее место.

### RU
отыграть, постепенно вернуть (отставание, деньги)

### Image

### ImagePrompt
Photorealistic shot from behind: a red Formula 1 car closing in on a rival just ahead on a race track, heavy motion blur, the gap between them almost gone, dramatic late-afternoon light.

### Related
**retrieve** — get a thing back, one action, no struggle · *opp:* **squander** — lose it carelessly

### MyExample

### Tags
phrasal-verb
```

В эталоне `Related` — это реально существующие в `All_Words.csv` строки `Word,retrieve,verb` и `Word,squander,verb`, а не подобранные «по смыслу» слова. Синонимов ровно столько, сколько нашлось в словаре: добирать до красивого числа нечем и не нужно.

## Эталон (TSV) — то, что реально пишется в файл

Пустых колонок две: Image (между RU и ImagePrompt) и MyExample (между Related и Tags) — в обоих местах **две табуляции подряд**.

```tsv
claw back	Verstappen managed to {{c1::claw back::c___ b___ recover gradually}} the eight-second gap over the final stint.	Ферстаппен сумел отыграть восьмисекундный отрыв на последнем отрезке гонки.	To gradually recover something you had lost — a lead, a deficit, money — through steady, deliberate effort.	Постепенно вернуть то, что было потеряно — преимущество, отставание, деньги — за счёт упорных, целенаправленных усилий.	Phrasal verb · separable · <i>claw sth back</i> / <i>claw back sth</i> · с местоимением объект в середине: <i>claw it back</i>.	/klɔː bæk/ (BrE), /klɑː bæk/ (AmE)	<b>claw back</b> a deficit / a gap / lost ground · <b>claw</b> the gap <b>back</b> · <b>claw back</b> losses	The government is trying to <b>claw back</b> overpaid benefits.<br>After a disastrous first half, the team slowly <b>clawed back</b> the deficit to draw 3–3.<br>It took years of austerity to <b>claw back</b> the money lost in the crisis.<br>She <b>clawed</b> her way <b>back</b> into contention after falling to last place.	Правительство пытается вернуть переплаченные пособия.<br>После провального первого тайма команда медленно отыграла отставание и свела матч вничью 3:3.<br>Понадобились годы жёсткой экономии, чтобы вернуть деньги, потерянные в кризис.<br>Она пробилась обратно в борьбу за победу, опустившись было на последнее место.	отыграть, постепенно вернуть (отставание, деньги)		Photorealistic shot from behind: a red Formula 1 car closing in on a rival just ahead on a race track, heavy motion blur, the gap between them almost gone, dramatic late-afternoon light.	<b>retrieve</b> — get a thing back, one action, no struggle · <i>opp:</i> <b>squander</b> — lose it carelessly		phrasal-verb
```

## Конверсия полей → TSV (механическая, формулировки не менять)

| Поле карточки | TSV |
|----------|-----|
| граница между полями | табуляция `\t` |
| Sentence | текст с cloze, без бэктиков |
| SentenceRU / DefinitionRU | русский текст одной строкой |
| Example2 | 3–6+ предложений, склеенных через `<br>` |
| Example2RU | те же переводы в том же порядке, через `<br>` |
| перенос между примерами / буллитами | `<br>` |
| `- ` в начале буллита | удаляется (`<br>` уже разделяет) |
| жирный | `<b>…</b>` (только в англ. полях) |
| курсив | `<i>…</i>` |
| inline-разделитель `·` | сохраняется как есть |
| пустое поле Image | пустая колонка (между RU и ImagePrompt — две табуляции подряд) |
| Related | позиции через ` · `, слово-сосед в `<b>`, метки `<i>opp:</i>` / `<i>cf:</i>`; соседей нет — пустая колонка |
| пустое поле MyExample | пустая колонка (между Related и Tags — две табуляции подряд) |
| Tags | последнее поле, теги через пробел |

Внутри полей не должно остаться «сырых» табуляций и переносов строк — одна карточка = одна строка файла.

## Контрастная пара — пример разделения

Ввод `interesting / interested` → **ДВЕ** карточки, каждая в своём файле (`new_words/interesting.tsv`, `new_words/interested.tsv`), каждая со своей строкой в `All_Words.csv`. Ключевое: естественные предложения, где подходит только одна форма, и англ. подсказка-маркер грамматики (а не перевод):

- `The strategy battle in that race was genuinely {{c1::interesting::i___ the thing causes the feeling}}.`
  → на обороте: `-ing` = вещь-причина (the thing produces the feeling).
- `I'm really {{c1::interested::i___ the person feels it}} in how teams manage tyre degradation.`
  → на обороте: `-ed` = человек-носитель чувства; паттерн *interested **in** sth*.

Каждая — полноценная карточка по шаблону; Example2 у одной показывает вторую форму («✗ interesting in → ✓ interested in»), чтобы контраст был виден. То же для think of / think about: две карточки, Form маркирует «vs think ABOUT = consider over time» и наоборот.

## Регистрация в All_Words.csv

На каждое значение — строка `Type,Word,POS / Info`:
- `Type` — по типу входа: `Word` / `Phrase` / `Phrasal Verb` / `Idiom`.
- `Word` — лемма / шаблон управления / фраза.
- `POS / Info` — часть речи и пометки в стиле существующих строк; если нечего добавить — оставь пустым (строка вида `Word,pull,`).
