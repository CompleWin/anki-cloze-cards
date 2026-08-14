# -*- coding: utf-8 -*-
"""
Create / update the Anki note type "Cloze EN Helper" used by this project.

Prerequisites
-------------
1. Anki is running.
2. The AnkiConnect add-on is installed (Tools -> Add-ons -> Get Add-ons ->
   code 2055492159) and Anki was restarted.

Run
---
    python create_anki_notetype.py

What it does
------------
- Creates a Cloze note type with 15 fields matching the TSV columns
  (Tags is the 16th TSV column and is mapped to Anki's Tags on import,
  so it is NOT a field).
- Field order == TSV column order, so import is a straight 1:1 mapping:
  Target, Sentence, SentenceRU, Definition, DefinitionRU, Form, IPA,
  Collocations, Example2, Example2RU, RU, Image, ImagePrompt, Related,
  MyExample.
- The front asks you to TYPE the missing word ({{type:cloze:Sentence}});
  the back shows Anki's character-by-character comparison.
- Related renders on the back as a block of neighbouring words you have
  already studied (filled in by the skill from All_Words.csv).
- MyExample is empty on import: it is the field YOU fill in during review
  (press E / Edit) with your own sentence. Until it is filled, the back
  shows a placeholder reminding you to write one.
- Russian fields (SentenceRU, DefinitionRU, Example2RU, RU) render on the
  back under <details> spoilers -> click to reveal.
- If the note type already exists, missing fields are added, field order is
  repaired, and template + styling are updated in place.
"""

import json
import urllib.request

MODEL_NAME = "Cloze EN Helper"
ANKICONNECT_URL = "http://127.0.0.1:8765"

FIELDS = [
    "Target", "Sentence", "SentenceRU", "Definition", "DefinitionRU",
    "Form", "IPA", "Collocations", "Example2", "Example2RU",
    "RU", "Image", "ImagePrompt", "Related", "MyExample",
]

FRONT = """<div class="ec">
  <div class="sentence">{{cloze:Sentence}}</div>
  <div class="typebox">{{type:cloze:Sentence}}</div>
</div>"""

BACK = """<div class="ec">
  <div class="sentence">{{cloze:Sentence}}</div>

  <div class="typebox">{{type:cloze:Sentence}}</div>

  {{#SentenceRU}}<details class="ru"><summary>Перевод предложения</summary><div class="ru-body">{{SentenceRU}}</div></details>{{/SentenceRU}}

  <hr>

  <div class="headword">
    <span class="target">{{Target}}</span>
    {{#IPA}}<span class="ipa">{{IPA}}</span>{{/IPA}}
    {{#Form}}<span class="form">{{Form}}</span>{{/Form}}
  </div>

  {{#Image}}<div class="image">{{Image}}</div>{{/Image}}
  {{^Image}}{{#ImagePrompt}}<div class="image-pending"><span class="ip-label">image prompt</span>{{ImagePrompt}}</div>{{/ImagePrompt}}{{/Image}}

  {{#Definition}}<div class="definition">{{Definition}}</div>{{/Definition}}
  {{#DefinitionRU}}<details class="ru"><summary>Перевод определения</summary><div class="ru-body">{{DefinitionRU}}</div></details>{{/DefinitionRU}}

  {{#Collocations}}<div class="block"><div class="label">collocations</div><div class="value">{{Collocations}}</div></div>{{/Collocations}}

  {{#Related}}<div class="block"><div class="label">related — уже в колоде</div><div class="value related">{{Related}}</div></div>{{/Related}}

  {{#Example2}}<div class="block"><div class="label">examples</div><div class="value example2">{{Example2}}</div></div>{{/Example2}}
  {{#Example2RU}}<details class="ru"><summary>Перевод примеров</summary><div class="ru-body">{{Example2RU}}</div></details>{{/Example2RU}}

  <div class="audio">{{tts en_US:Target}}</div>

  {{#RU}}<details class="ru"><summary>Слово (RU)</summary><div class="ru-body">{{RU}}</div></details>{{/RU}}

  <hr>

  {{#MyExample}}<div class="block"><div class="label">твой пример</div><div class="value my-example">{{MyExample}}</div></div>{{/MyExample}}
  {{^MyExample}}<div class="my-example-pending"><span class="me-label">твой пример</span>Составь своё предложение с этим словом и запиши его в поле <b>MyExample</b> — клавиша <b>E</b> (Edit) на десктопе, карандаш в мобильном.</div>{{/MyExample}}
</div>"""

CSS = """.card { text-align: left; }

.ec {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 23px;
  line-height: 1.6;
  color: #1a1a1a;
  max-width: 860px;
  margin: 0 auto;
  padding: 8px 16px;
}
.ec .sentence { font-size: 24px; }
.ec .cloze { font-weight: 600; color: #1565c0; }
.ec hr { border: none; border-top: 1px solid #e3e3e3; margin: 18px 0; }

.ec .typebox { margin-top: 14px; }
.ec .typebox input {
  font-family: inherit;
  font-size: 21px;
  width: 100%;
  max-width: 460px;
  padding: 6px 10px;
  color: #1a1a1a;
  background: #fff;
  border: 1px solid #d0d0d0;
  border-radius: 6px;
}
.ec .typebox code#typeans { font-size: 21px; }

.ec .headword { display: flex; align-items: baseline; flex-wrap: wrap; gap: 8px; margin-bottom: 4px; }
.ec .target { font-size: 28px; font-weight: 600; }
.ec .ipa { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 17px; color: #6a6a6a; }
.ec .form { font-size: 14px; color: #555; background: #f0f0ee; border-radius: 6px; padding: 2px 8px; }

.ec .definition { font-size: 20px; margin: 10px 0 0; }
.ec .block { margin-top: 12px; }
.ec .label { font-size: 14px; color: #9a9a9a; margin-bottom: 2px; }
.ec .value { font-size: 18px; color: #444; }
.ec .example2 { font-style: italic; }
.ec .related { line-height: 1.7; }
.ec .audio { margin-top: 14px; }

.ec .my-example { font-style: italic; color: #2e7d32; }
.ec .my-example-pending { margin-top: 14px; font-size: 15px; color: #9a9a9a; border: 1px dashed #d8d8d8; border-radius: 8px; padding: 8px 10px; }
.ec .me-label { display: block; font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; color: #b5b5b5; margin-bottom: 2px; }

.ec .image { margin-top: 14px; }
.ec .image img { max-width: 100%; max-height: 320px; border-radius: 8px; display: block; }
.ec .image-pending { margin-top: 14px; font-size: 15px; color: #9a9a9a; font-style: italic; border: 1px dashed #d8d8d8; border-radius: 8px; padding: 8px 10px; }
.ec .ip-label { font-style: normal; font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; color: #b5b5b5; margin-right: 6px; }

.ec details.ru { margin-top: 10px; }
.ec details.ru summary { font-size: 15px; color: #9a9a9a; cursor: pointer; list-style: none; user-select: none; }
.ec details.ru summary::-webkit-details-marker { display: none; }
.ec .ru-body { font-size: 18px; color: #555; margin: 6px 0 4px; padding-left: 10px; border-left: 2px solid #e3e3e3; }

b { font-weight: 600; }

/* Тёмная тема Anki */
.nightMode .ec, .night_mode .ec { color: #e0e0e0; }
.nightMode .ec .cloze, .night_mode .ec .cloze { color: #6db3f2; }
.nightMode .ec .target, .night_mode .ec .target { color: #f0f0f0; }
.nightMode .ec .form, .night_mode .ec .form { color: #cfcfcf; background: #3a3a3a; }
.nightMode .ec .ipa, .night_mode .ec .ipa { color: #b0b0b0; }
.nightMode .ec .value, .night_mode .ec .value,
.nightMode .ec .ru-body, .night_mode .ec .ru-body { color: #c4c4c4; }
.nightMode .ec .label, .night_mode .ec .label,
.nightMode .ec details.ru summary, .night_mode .ec details.ru summary { color: #8a8a8a; }
.nightMode .ec hr, .night_mode .ec hr { border-color: #4a4a4a; }
.nightMode .ec .ru-body, .night_mode .ec .ru-body { border-left-color: #4a4a4a; }
.nightMode .ec .image-pending, .night_mode .ec .image-pending { border-color: #4a4a4a; }
.nightMode .ec .typebox input, .night_mode .ec .typebox input { color: #e0e0e0; background: #2c2c2c; border-color: #4a4a4a; }
.nightMode .ec .my-example, .night_mode .ec .my-example { color: #81c784; }
.nightMode .ec .my-example-pending, .night_mode .ec .my-example-pending { border-color: #4a4a4a; }
"""


def invoke(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = urllib.request.Request(ANKICONNECT_URL, payload)
    try:
        resp = json.load(urllib.request.urlopen(req))
    except urllib.error.URLError as e:
        raise SystemExit(
            "Cannot reach AnkiConnect at %s.\n"
            "Make sure Anki is running and the AnkiConnect add-on (2055492159) "
            "is installed.\nDetails: %s" % (ANKICONNECT_URL, e)
        )
    if resp.get("error") is not None:
        raise RuntimeError(resp["error"])
    return resp["result"]


def sync_fields():
    """Add fields the note type is missing and repair their order.

    Adding a field is non-destructive: existing notes simply get it empty,
    which is exactly what Related / MyExample need on old cards.
    """
    current = invoke("modelFieldNames", modelName=MODEL_NAME)
    if current == FIELDS:
        return True

    for name in [f for f in FIELDS if f not in current]:
        try:
            invoke("modelFieldAdd", modelName=MODEL_NAME, fieldName=name, index=FIELDS.index(name))
            print("  + field added: %s" % name)
        except RuntimeError as e:
            print("  ! could not add field %s: %s" % (name, e))
            print("    Add it by hand: Tools -> Manage Note Types -> %s -> Fields." % MODEL_NAME)
            return False

    current = invoke("modelFieldNames", modelName=MODEL_NAME)
    extra = [f for f in current if f not in FIELDS]
    if extra:
        print("  ! unexpected extra fields: %s" % extra)
        print("    Leaving field order alone — fix it by hand so TSV columns still line up.")
        return False

    for idx, name in enumerate(FIELDS):
        if current.index(name) != idx:
            try:
                invoke("modelFieldReposition", modelName=MODEL_NAME, fieldName=name, index=idx)
                current = invoke("modelFieldNames", modelName=MODEL_NAME)
                print("  ~ field moved to position %d: %s" % (idx + 1, name))
            except RuntimeError as e:
                print("  ! could not move field %s: %s" % (name, e))
                return False

    return invoke("modelFieldNames", modelName=MODEL_NAME) == FIELDS


def main():
    existing = invoke("modelNames")
    template = {"Name": "Cloze", "Front": FRONT, "Back": BACK}

    if MODEL_NAME in existing:
        print('Note type "%s" already exists -> syncing fields, template, styling.' % MODEL_NAME)
        if not sync_fields():
            print("  WARNING: fields do not match the expected layout:")
            print("    current:  %s" % invoke("modelFieldNames", modelName=MODEL_NAME))
            print("    expected: %s" % FIELDS)
        invoke("updateModelTemplates", model={"name": MODEL_NAME, "templates": {"Cloze": {"Front": FRONT, "Back": BACK}}})
        invoke("updateModelStyling", model={"name": MODEL_NAME, "css": CSS})
        print("  Done: template and styling updated.")
    else:
        invoke(
            "createModel",
            modelName=MODEL_NAME,
            inOrderFields=FIELDS,
            css=CSS,
            isCloze=True,
            cardTemplates=[template],
        )
        print('Created cloze note type "%s" with %d fields.' % (MODEL_NAME, len(FIELDS)))

    print()
    print("Import settings for new_words/*.tsv:")
    print("  - Type: Cloze EN Helper")
    print("  - Field separator: Tab")
    print("  - Allow HTML in fields: ON")
    print("  - Map columns 1-15 to the fields above (in order), column 16 -> Tags.")
    print("  - Columns Image (12) and MyExample (15) arrive empty by design:")
    print("    the picture and your own sentence are added by hand after import.")


if __name__ == "__main__":
    main()
