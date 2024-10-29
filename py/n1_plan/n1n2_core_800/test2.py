import json
import re
from time import sleep

from n1_plan.n1n2_core_800.batch_update import get_furigana

with open("words2_lesson.json", "r") as f:
    with open("words2_lesson_furi.json", "r") as f2:
        s = f.read()
        s = json.loads(s)
        s2 = json.loads(f2.read())
        res = []
        subcat = []
        s2_map = {ss["Meaning"]: ss for ss in s2}
        for word in s:
            ww = None
            if word["explain"] not in s2_map:
                # subcat.append(word)
                w = word["word"]
                arr = w.split("|")
                Reading, VocabularyKanji = "", ""
                if len(arr) == 2:
                    Reading, VocabularyKanji = arr
                else:
                    VocabularyKanji = arr[0]
                [ExpressionOri, ExpressionZH] = word["example"].split("\n")
                newExpression = re.sub(r'\[(\w+)]', r'<span class="express-word">\1</span>', ExpressionOri)
                ExpressionGood =get_furigana(newExpression)
                tag = f"第{word['lesson']}关"
                Tags = [tag]
                ww = {
                    "VocabularyKanji": VocabularyKanji,
                    "Reading": word["word"],
                    "Meaning": word["explain"],
                    "Expression": ExpressionGood,
                    "ExpressionRead": ExpressionOri,
                    "ExpressionZH": ExpressionZH,
                    "VoiceRead": VocabularyKanji,
                    "Tags": Tags
                }
                subcat.append(ww)
                sleep(0.1)
            else:
                ww = s2_map[word["explain"]]

            res.append(ww)
        print(len(subcat))
        with open("words2_lesson_furi2.json", "w") as ff:
            ff.write(json.dumps(res, ensure_ascii=False, indent=2))