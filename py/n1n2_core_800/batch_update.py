import json
import os
import re
import sys
from pprint import pprint

from tqdm import tqdm

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import anki_cli

noteIds = anki_cli.invoke('findNotes', **{
    "query": "deck:N1考试800核心词汇"
    # "note": notes[0],
})
# print(noteIds)
notes = anki_cli.invoke('notesInfo', **{
    "notes": noteIds
    # "note": notes[0],
})


# word_dict = {}
# with open("bb.json", "r") as f:
#     s = f.read()
#     words = json.loads(s)
#     for word in words:
#         word_dict[word["formOrg"]] = word

# pprint(notes[:10])
def updateNotes():
    for note in tqdm(notes):
        pprint(note)
        Expression = note["fields"]["Expression"]["value"]
        newExpression = re.sub(r'\[(\w+)]', r'<span class="express-word">\1</span>', Expression)

        updateNote = {
            "note": {
                "id": note["noteId"],
                "fields": {
                    'VocabularyKanji': note["fields"]["VocabularyKanji"]["value"],
                    'Reading': note["fields"]["Reading"]["value"],
                    'VoiceRead': note["fields"]["VoiceRead"]["value"],
                    'Expression': newExpression,
                    'ExpressionZH': note["fields"]["ExpressionZH"]["value"],
                    'Meaning': note["fields"]["Meaning"]["value"],
                },
            }
        }
        # continue
        result = anki_cli.invoke('updateNote', **updateNote)
        if result:
            # pprint(updateNote)
            print(note["fields"]["VocabularyKanji"]["value"])
            # pprint(result)
            # print(result)
            # print(note["fields"]["Expression"]["value"], result)


updateNotes()
