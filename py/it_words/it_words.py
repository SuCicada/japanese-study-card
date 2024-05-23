import os
import re
from pathlib import Path
from pprint import pprint

import anki_cli

data_dir = os.path.join(os.path.dirname(__file__), "")


def parse_txt(name):
    with open(os.path.join(data_dir, name), "r", encoding="utf-8") as f:
        it_words = f.read().splitlines()

        res = []
        for line in it_words:
            line = line.strip()
            if line == "":
                continue
            try:
                arr = line.split("　")
                # print(line)
                name = os.path.basename(name).split(".")[0]
                tag = name.replace("　", "-").replace(" ", "-")
                note = {
                    "Expression": arr[0],
                    "Reading": arr[1],
                    "Meaning": arr[2] if len(arr) > 2 else "",
                    "Tags": [tag]
                }
                res.append(note)
            except Exception as e:
                print("err", line, e)
                raise e
        return res


def createDeck():
    result = anki_cli.invoke('getDeckStats', **{
        "decks": ["IT情報技術"],
    })
    # result = anki_cli.invoke('createDeck', deck='test1')
    pprint(result)


def createModel():
    result = anki_cli.invoke('createModel', **{
        "modelName": "japanese_it_words",
        "inOrderFields": ["Expression", "Reading", "Meaning", "Notes", "Tags"],
        # "css": "Optional CSS with default to builtin css",
        "isCloze": False,
        "cardTemplates": [
            {
                "Name": "My Card 1",
                "Front": "{{Expression}}",
                "Back": """{{Expression}}<hr id="answer">{{Reading}}"""
            }
        ]
    })
    pprint(result)


def modelNamesAndIds():
    result = anki_cli.invoke('modelNamesAndIds')
    pprint(result)


def findModelsByName():
    result = anki_cli.invoke('findModelsByName', **{
        "modelNames": ["japanese_it_words"],
    })
    pprint(result)


def getDeckConfig():
    result = anki_cli.invoke('getDeckConfig', **{
        "deck": "IT情報技術",
    })
    pprint(result)


def addNotes(notes):
    # notes = [
    #     {
    #         "deckName": "IT情報技術",
    #         "modelName": "japanese_it_words",
    #         "fields": {
    #             "Question": "補助記憶装置",
    #             "Answer": "ほじょきおくそうち"
    #         },
    #         # "options": {
    #         #     "allowDuplicate": False,
    #         #     "duplicateScope": "deck",
    #         #     "duplicateScopeOptions": {
    #         #         "deckName": "Default",
    #         #         "checkChildren": False,
    #         #         "checkAllModels": False
    #         #     }
    #         # },
    #         # "tags": [
    #         #     "yomichan"
    #         # ],
    #     }]
    for note in notes:
        try:
            result = anki_cli.invoke('addNote', **{
                "note": note,
                # "note": notes[0],
            })
            # print(note)
            print(note["fields"]["Expression"], result)
        except Exception as e:
            print("err", note["fields"]["Expression"], e)


def sync():
    result = anki_cli.invoke('sync')
    pprint(result)


def build_notes(note_data):
    notes = []
    for note in note_data:
        notes.append({
            "deckName": "IT情報技術",
            "modelName": "japanese_it_words",
            "tags": note["Tags"],
            "fields": {
                "Expression": note["Expression"],
                "Reading": note["Reading"],
                "Meaning": note["Meaning"],
                "Notes": "",
                "VoiceRead": note["Expression"],
            },
        })
    return notes


import_list = [
    # Path("../data/1 ハードウェア.txt"),
    # Path("../data/2 CPU.txt"),
    # Path("../data/3 主記憶装置.txt"),
    # Path("../data/4 補助記憶装置.txt"),
    # Path("../data/5 入出力装置.txt"),
    # Path("../data/6 入出力インタフェース.txt"),
    # Path("../data/2-1 OS.txt"),
    # Path("../data/2-2 ファイルの管理.txt"),
    # Path("../data/2-3 表計算ソフト.txt"),
    # Path("../data/2-4 関数.txt"),
    Path("../data/it/3-1 ２進数.txt"),
    Path("../data/it/3-2 マルチメディア.txt"),
]
for path in import_list:
    note_data = parse_txt(path.resolve())
    notes = build_notes(note_data)
    addNotes(notes)
    # pprint(notes)
# note_data = parse_txt(Path("../data/1 ハードウェア.txt").resolve())
# notes = build_notes(note_data)
# addNotes(notes)
# sync()
# print(notes)
