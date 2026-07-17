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
- Creates a Cloze note type with 13 fields matching the TSV columns
  (Tags is the 14th TSV column and is mapped to Anki's Tags on import,
  so it is NOT a field).
- Field order == TSV column order, so import is a straight 1:1 mapping:
  Target, Sentence, SentenceRU, Definition, DefinitionRU, Form, IPA,
  Collocations, Example2, Example2RU, RU, Image, ImagePrompt.
- Russian fields (SentenceRU, DefinitionRU, Example2RU, RU) render on the
  back under <details> spoilers -> click to reveal. Same for ImagePrompt.
- If the note type already exists, its template + styling are updated in place.
"""

import json
import urllib.request

MODEL_NAME = "Cloze EN Helper"
ANKICONNECT_URL = "http://127.0.0.1:8765"

FIELDS = [
    "Target", "Sentence", "SentenceRU", "Definition", "DefinitionRU",
    "Form", "IPA", "Collocations", "Example2", "Example2RU",
    "RU", "Image", "ImagePrompt",
]

FRONT = """<div class="ec">
  <div class="sentence">{{cloze:Sentence}}</div>
</div>"""

BACK = """<div class="ec">
  <div class="sentence">{{cloze:Sentence}}</div>

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

  {{#Example2}}<div class="block"><div class="label">examples</div><div class="value example2">{{Example2}}</div></div>{{/Example2}}
  {{#Example2RU}}<details class="ru"><summary>Перевод примеров</summary><div class="ru-body">{{Example2RU}}</div></details>{{/Example2RU}}

  <div class="audio">{{tts en_US:Target}}</div>

  {{#RU}}<details class="ru"><summary>Слово (RU)</summary><div class="ru-body">{{RU}}</div></details>{{/RU}}
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

.ec .headword { display: flex; align-items: baseline; flex-wrap: wrap; gap: 8px; margin-bottom: 4px; }
.ec .target { font-size: 28px; font-weight: 600; }
.ec .ipa { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 17px; color: #6a6a6a; }
.ec .form { font-size: 14px; color: #555; background: #f0f0ee; border-radius: 6px; padding: 2px 8px; }

.ec .definition { font-size: 20px; margin: 10px 0 0; }
.ec .block { margin-top: 12px; }
.ec .label { font-size: 14px; color: #9a9a9a; margin-bottom: 2px; }
.ec .value { font-size: 18px; color: #444; }
.ec .example2 { font-style: italic; }
.ec .audio { margin-top: 14px; }

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


def main():
    existing = invoke("modelNames")
    template = {"Name": "Cloze", "Front": FRONT, "Back": BACK}

    if MODEL_NAME in existing:
        print('Note type "%s" already exists -> updating template + styling.' % MODEL_NAME)
        current_fields = invoke("modelFieldNames", modelName=MODEL_NAME)
        if current_fields != FIELDS:
            print("  WARNING: fields differ from the expected layout.")
            print("    existing: %s" % current_fields)
            print("    expected: %s" % FIELDS)
            print("  Add/rename fields manually (Tools -> Manage Note Types -> Fields),")
            print("  or delete the note type and re-run this script for a clean setup.")
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
    print("  - Map columns 1-13 to the fields above (in order), column 14 -> Tags.")


if __name__ == "__main__":
    main()
