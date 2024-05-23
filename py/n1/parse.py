import json
import os
import sys
from dataclasses import dataclass
from pprint import pprint

import genanki

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import anki_cli


@dataclass
class Card:
    VocabularyKanji: str = ""
    Expression: str = ""  # html: 例句

    Reading: str = ""
    Meaning: str = ""  # html: 解释，例句
    EngTag: str = ""  # if english
    VoiceRead: str = ""  # tts
    Notes: str = ""
    Tags: list[str] = None


def get_data():
    with open("bb.json", "r") as f:
        s = f.read()
        s = json.loads(s)
        print(len(s))
        # pprint(s[:100])
        cards = []
        for word in s:
            try:
                card = Card()
                card.VocabularyKanji = word["formOrg"] # 单词
                card.Reading = word["formKana"] # 读音
                card.VoiceRead = word["formOrg"] # tts
                frontMeanHtml = ""
                backMeanHtml = ""
                for meaning in word["meanings"]:
                    sentences = meaning["sentences"]
                    frontSentenceHtml = ""
                    backSentenceHtml = ""
                    backSentenceHtml += f"""<div class="back-content">{meaning["content"]}</div>"""
                    for sentence in sentences:
                        formOrg = sentence["formOrg"]
                        if not formOrg.endswith("。"):
                            formOrg += "。"
                        frontSentenceHtml += f"""<div class="front-formOrg">{formOrg}</div>"""

                        backSentenceHtml += f"""<div class="back-formOrg">{formOrg}</div>"""
                        backSentenceHtml += f"""<div class="back-formKana">{sentence["formKana"]}</div>"""
                        backSentenceHtml += f"""<div class="back-formLocal">{sentence["formLocal"]}</div>"""

                    frontMeanHtml += f"""<div class="front-express">{frontSentenceHtml}</div>"""
                    backMeanHtml += f"""<div class="back-express">{backSentenceHtml}</div>"""

                card.Expression = frontMeanHtml
                card.Meaning = backMeanHtml

                card.Tags = []
                for type in word["types"]:
                    type = type.strip()
                    if type.startswith("英 ") or type.startswith("英（"):
                        card.EngTag = type
                    else:
                        card.Tags.append(type)

                cards.append(card)
            except Exception as e:
                print("err", e)
                pprint(word)
                raise e
        return cards


def create_anki(cards: list[Card]):
    # 创建一个Anki模型
    with open("model.css", "r") as f:
        css = f.read()
    my_model = genanki.Model(
        202401251554,
        'japanese_jlpt_n1',
        fields=[
            {'name': 'VocabularyKanji'},
            {'name': 'Reading'},
            {'name': 'VoiceRead'},
            {'name': 'Expression'},
            {'name': 'Meaning'},
            {'name': 'EngTag'},
            {'name': 'Notes'},
        ],
        templates=[
            {
                'name': 'japanese_jlpt_n1',
                'qfmt': """
<div class="center">
  <span style="font-family: irohamaru mikami; font-size: 50px;">{{VocabularyKanji}}</div>

<hr id="answer" class="separator" />
<div class="expression">
{{Expression}}
</div>
                """,
                'afmt': """
<div class="card-content center">
<div class="center">
  <span style="font-family: irohamaru mikami; font-size: 50px;">{{VocabularyKanji}}</span>
</div>

<!--  <hr id="answer" class="separator" /> -->
  <span style="font-size: 40px;">{{furigana:Reading}}</span>

  <div class="card-tags-container"> 
    <span class="tags">{{Tags}}</span>

    <span class="entag">{{EngTag}}</span>
 </div>

  <div class="center">
    <span style="font-size: 30px;">{{furigana:Meaning}}</span>
  </div>


  <div class="left">
    <span style="font-size: 30px;">{{furigana:Notes}}</span>
  </div>


</div>

{{tts ja_JP voices=Apple_O-ren,Microsoft_Haruka:VocabularyKanji}}
{{tts ja_JP voices=Apple_O-ren,Microsoft_Haruka:Reading}}
{{tts ja_JP voices=Apple_O-ren,Microsoft_Haruka:Expression}}

                """,
            },
        ],
        css=css)

    # 创建一个Anki牌组
    my_deck = genanki.Deck(
        202401251555,
        '日本語能力試験N1')

    for card in cards:
        # 创建一个卡片
        my_note = genanki.Note(
            model=my_model,
            fields=[card.VocabularyKanji, card.Reading, card.VoiceRead, card.Expression, card.Meaning,
                    card.EngTag, card.Notes],
            tags=card.Tags
        )

        # 将卡片添加到牌组中
        my_deck.add_note(my_note)

    # 导出为.apkg文件
    genanki.Package(my_deck).write_to_file('日本語能力試験N1.apkg')


def sample():
    with open("bb.json", "r") as f:
        s = f.read()
        s = json.loads(s)
        print(len(s))
        for word in s:
            try:
                skip = True
                for x in word["types"]:
                    if " " in x.strip():
                        skip = False
                if not skip:
                    print(word["types"])
                # print(word["formOrg"])
                # for meaning in word["meanings"]:
                #     print(meaning["content"])
                #     for sentence in meaning["sentences"]:
                #         print(sentence["formOrg"])
            except Exception as e:
                print("err", e)
                pprint(word)
                raise e


data = get_data()
create_anki(data)
# sample()
