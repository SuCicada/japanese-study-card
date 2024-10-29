import json
import os
import re
import sys
from pprint import pprint
from time import sleep

from nltk.corpus import words
from tqdm import tqdm

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import anki_cli

noteIds = anki_cli.invoke('findNotes', **{
    "query": "deck:N2考试800核心词汇"
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
res = []
def updateNotes():
    for note in tqdm(notes):
        # pprint(note)
        Expression = note["fields"]["Expression"]["value"]
        ExpressionRead = note["fields"]["ExpressionRead"]["value"]
        # if ExpressionRead != "":
        #     continue
        # newExpression = re.sub(r'\[(\w+)]', r'<span class="express-word">\1</span>', Expression)
        # newExpression = get_furigana(Expression)
        # sleep(0.1)
        updateNote = {
            "note": {
                "id": note["noteId"],
                "fields": {
                    'VocabularyKanji': note["fields"]["VocabularyKanji"]["value"],
                    'Reading': note["fields"]["Reading"]["value"],
                    'VoiceRead': note["fields"]["VoiceRead"]["value"],
                    'Expression': Expression,
                    'ExpressionRead': ExpressionRead,
                    'ExpressionZH': note["fields"]["ExpressionZH"]["value"],
                    'Meaning': note["fields"]["Meaning"]["value"],
                    'Tags': note ["tags"][0],
                },
            }
        }
        res.append(updateNote["note"]["fields"])
        # continue
        # result = anki_cli.invoke('updateNote', **updateNote)
        # result = False
        # print(result)
        # if result:
        #     # pprint(updateNote)
        #     print(note["fields"]["VocabularyKanji"]["value"])
            # pprint(result)
            # print(result)
            # print(note["fields"]["Expression"]["value"], result)


updateNotes()

with open("words2_lesson_furi.json", "w") as f:
    f.write(json.dumps(res, indent=4, ensure_ascii=False))
