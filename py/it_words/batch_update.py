import os
import sys
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import anki_cli

#
# {
#     "action": "updateNote",
#     "version": 6,
#     "params": {
#         "note": {
#             "id": 1514547547030,
#             "fields": {
#                 "Front": "new front content",
#                 "Back": "new back content"
#             },
#             "tags": ["new", "tags"]
#         }
#     }
# }

noteIds = anki_cli.invoke('findNotes', **{
    "query": "deck:IT情報技術"
    # "note": notes[0],
})
# print(noteIds)
notes = anki_cli.invoke('notesInfo', **{
    "notes": noteIds
    # "note": notes[0],
})


# pprint(notes[:10])
def updateNotes():
    for note in notes:
        pprint(note)
        updateNote = {
            "note": {
                "id": note["noteId"],
                "fields": {
                    'Expression': note["fields"]["Expression"]["value"],
                    'Meaning':   note["fields"]["Meaning"]["value"],
                    'Notes':  note["fields"]["Notes"]["value"],
                    'Reading':   note["fields"]["Reading"]["value"],
                    'VoiceRead':   note["fields"]["Expression"]["value"],
                },
                # "tags": ["new", "tags"]
            }
        }
        result = anki_cli.invoke('updateNote', **updateNote)
        if result:
            pprint(updateNote)
            pprint(result)
            print(result)
            # print(note["fields"]["Expression"]["value"], result)

updateNotes()
