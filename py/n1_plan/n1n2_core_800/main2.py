import json
import os
import re
import sys
from dataclasses import dataclass
from pprint import pprint

import genanki

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import anki_cli


@dataclass
class Card:
    VocabularyKanji: str = ""  # 单词
    Expression: str = ""  # html: 例句，显示注音
    ExpressionRead: str = ""  # html: 例句, 发音

    Reading: str = ""  # 显示的读音
    Meaning: str = ""  # html: 解释
    ExpressionZH: str = ""  # html: 例句, 中文
    VoiceRead: str = ""  # 单词 tts
    Tags: list[str] = None


def get_data():
    with open("words2_lesson_furi2.json", "r") as f:
        s = f.read()
        s = json.loads(s)
        print(len(s))
        # pprint(s[:100])
        cards = []
        for word in s:
            try:
                card = Card()
                card.VocabularyKanji = word["VocabularyKanji"]
                card.Expression = word["Expression"]
                card.ExpressionRead = word["ExpressionRead"]
                card.Reading =  word["Reading"]
                card.Meaning =  word["Meaning"]
                card.ExpressionZH =  word["ExpressionZH"]
                card.VoiceRead =  word["VoiceRead"]
                card.Tags =  [word["Tags"]]

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
    with open("front.html", "r") as f:
        front = f.read()
    with open("back.html", "r") as f:
        back = f.read()
    my_model = genanki.Model(
        202410281556,
        'japanese_jlpt_core2',
        fields=[
            {'name': 'VocabularyKanji'},
            {'name': 'Reading'},
            {'name': 'VoiceRead'},
            {'name': 'Expression'},
            {'name': 'ExpressionRead'},
            {'name': 'ExpressionZH'},
            {'name': 'Meaning'},
        ],
        templates=[
            {
                'name': 'japanese_jlpt_core2',
                'qfmt':front,
                'afmt': back,
            },
        ],
        css=css)

    # 创建一个Anki牌组
    my_deck = genanki.Deck(
        202410281556,
        'N2考试800核心词汇')

    for card in cards:
        # 创建一个卡片
        my_note = genanki.Note(
            model=my_model,
            fields=[card.VocabularyKanji,
                    card.Reading,
                    card.VoiceRead,
                    card.Expression,
                    card.ExpressionRead,
                    card.ExpressionZH,
                    card.Meaning,
                    ],
            tags=card.Tags
        )

        # 将卡片添加到牌组中
        my_deck.add_note(my_note)

    # 导出为.apkg文件
    genanki.Package(my_deck).write_to_file('N2考试800核心词汇.apkg')


data = get_data()
create_anki(data)
# sample()
