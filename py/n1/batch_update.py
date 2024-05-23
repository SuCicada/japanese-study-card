import json
import os
import sys
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import anki_cli

noteIds = anki_cli.invoke('findNotes', **{
    "query": "deck:1日本語能力試験N1"
    # "note": notes[0],
})
# print(noteIds)
notes = anki_cli.invoke('notesInfo', **{
    "notes": noteIds
    # "note": notes[0],
})

word_dict = {}
with open("bb.json", "r") as f:
    s = f.read()
    words = json.loads(s)
    for word in words:
        word_dict[word["formOrg"]] = word

# pprint(notes[:10])
def updateNotes():
    for note in notes:
        pprint(note)
        VocabularyKanji = note["fields"]["VocabularyKanji"]["value"]
        word = word_dict[VocabularyKanji]
        frontMeanHtml = ""
        for meaning in word["meanings"]:
            sentences = meaning["sentences"]
            frontSentenceHtml = ""
            for sentence in sentences:
                formOrg = sentence["formOrg"]
                if not formOrg.endswith("。"):
                    formOrg += "。"
                frontSentenceHtml += f"""<div class="front-formOrg">{formOrg}</div>"""
            frontMeanHtml += f"""<div class="front-express">{frontSentenceHtml}</div>"""
        Expression = frontMeanHtml
        updateNote = {
            "note": {
                "id": note["noteId"],
                "fields": {
                    'VocabularyKanji': VocabularyKanji,
                    'Reading':   note["fields"]["Reading"]["value"],
                    'VoiceRead':   VocabularyKanji,
                    'Expression':   Expression,
                    'Meaning':   note["fields"]["Meaning"]["value"],
                    'EngTag':  note["fields"]["EngTag"]["value"],
                    'Notes':  note["fields"]["Notes"]["value"],
                },
                # "tags": ["new", "tags"]
            }
        }
        result = anki_cli.invoke('updateNote', **updateNote)
        if result:
            # pprint(updateNote)
            print(VocabularyKanji)
            pprint(result)
            # print(result)
            # print(note["fields"]["Expression"]["value"], result)

updateNotes()
