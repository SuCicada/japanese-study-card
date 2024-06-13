import os
import sys
from pathlib import Path
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import anki_cli

data_dir = os.path.join(os.path.dirname(__file__), "")
# data_dir = os.path.abspath(Path(__file__)
print("data_dir", data_dir)


def parse_txt(name):
    with open(os.path.join(data_dir, name), "r", encoding="utf-8") as f:
        gram_block = f.read().split("\n\n")
        res = []
        for gram in gram_block:
            # print(gram)
            try:
                parts = gram.split("---")
                print(parts)
                if len(parts) == 1 and parts[0].strip() == "":
                    continue
                examples = parts[1].strip().splitlines()
                example = examples[0]
                example_reading = ""
                if len(examples) > 1:
                    example_reading = examples[1]
                name = os.path.basename(name).split(".")[0]
                tag = name.replace("　", "-").replace(" ", "-")
                note = {
                    "Expression": parts[0].strip(),
                    "Example": example.strip(),
                    "Reading": example_reading.strip(),
                    "Meaning": parts[2].strip(),
                    "Tags": [tag]
                }
                res.append(note)
            except Exception as e:
                print("err", gram, e)
                raise e
        return res


def addNotes(notes):
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


def build_notes(note_data):
    notes = []
    for note in note_data:
        notes.append({
            "deckName": "N1文法",
            "modelName": "japanese_n1_grammar",
            "tags": note["Tags"],
            "fields": {
                "Expression": note["Expression"],
                "Example": note["Example"],
                "Reading": note["Reading"],
                "Meaning": note["Meaning"],
            },
        })
    return notes


def addNotes(notes):
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


import_list = [
    # Path("../../data/grammar/1 オクトーバーフェスト.txt"),
    # Path("../../data/grammar/2 産業医を増やそう.txt"),
    # Path("../../data/grammar/3 飯食わぬ女房_1.txt"),
    # Path("../../data/grammar/3 飯食わぬ女房_2.txt"),
    # Path("../../data/grammar/4 上司との付き合い方.txt"),
    # Path("../../data/grammar/4 上司との付き合い方_2.txt"),
    Path("../../data/grammar/5 ドラマのシナリオを読む.txt"),
]
for path in import_list:
    note_data = parse_txt(path)
    notes = build_notes(note_data)
    # for note in notes:
    #     print(note)
    # pprint(notes)
    addNotes(notes)
