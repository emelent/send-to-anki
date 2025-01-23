#### Send to anki japanese

I made this script to just make the creation of japanese anki cards a bit easier
for myself.


This script takes json data and turns it into japanese anki cards.


I mainly use this with some terminal-based chatgpt command to get 
data from a phrase into the required format, then use that to
create anki cards.

I use a tool like [mods](https://github.com/charmbracelet/mods) with a bashscript:


```bash

function jsonify_jp() {
        data='give me this as a list of words and definition and the furigana in json data in the format {"phrase":"<original phrase>", "translation":"<phrase translation>", "furigana": "<phrase furigana>","words": {"<word>": {"furigana": {"<kana 1>":"<furigana 1>", "<kana 2>": "<furigana 2>"}}, ...}, "definition": "<word definition>"}} here is an example result from the phrase "犬は病院います": {"phrase": "犬は病院います", "translation":"The dog is in the hospital", "furigana":"犬[いぬ] は 病[びょう] 院[いん] います", "words": {"犬": {"furigana": {"犬":"いぬ"}, "definition": "dog"}, "病 院": {"furigana": {" 病":"びょう":,"院" :"いん", "definition": "hospital"}, "います":{"furigana": "います", "definition":"to exist, to be"}}'
        mods "take this japanese phrase, give the phrase with furigana in square brackets then also provide the translation in english, and give me a list of all the separate words in their dictionary form along with their meanings in english. Do not include particles and other word modifiers in this list or any 'お' put in front of word for respect, meaning phrases like '働いている' should just result one word '働く' which is the dictionary form : '$*'\n $data"
}
```

which gives me the json data in this format:

```json
{
    "phrase": "危険が伴う恐れがあるからここにいる17人の多数決で決めようと思う",
    "translation": "I think we should decide by majority vote of the 17 people here because there is a possibility of danger.",
    "furigana": "危険[きけん] が 伴[ともな]う 恐[おそ]れ が あ[あ]る から ここ に い[い]る 17[じゅうなな] 人[にん] の 多数決[たすうけつ] で 決[き]めよう と 思[おも]う",
    "words": {
        "危険": {"furigana": {"危険": "きけん"}, "definition": "danger"},
        "伴う": {
            "furigana": {"伴": "ともな"},
            "definition": "to accompany, to come with",
        },
        "恐れ": {"furigana": {"恐れ": "おそれ"}, "definition": "fear, anxiety, worry"},
        "ある": {"furigana": {"ある": "ある"}, "definition": "to exist, to have"},
        "ここ": {"furigana": {"ここ": "ここ"}, "definition": "here"},
        "いる": {
            "furigana": {"いる": "いる"},
            "definition": "to exist (animate), to be (present)",
        },
        "17": {"furigana": {"17": "じゅうなな"}, "definition": "seventeen"},
        "人": {"furigana": {"人": "にん"}, "definition": "person"},
        "多数決": {"furigana": {"多数決": "たすうけつ"}, "definition": "majority vote"},
        "決める": {"furigana": {"決め": "きめ"}, "definition": "to decide"},
        "思う": {"furigana": {"思": "おも"}, "definition": "to think"},
    }
}

```

Then I pipe that into this main.py to create anki cards. There are some less useful cards generated like for simple words like 'いる' or even '17' in this example, so after that I filter out the 'custom_autobot' tagged cards and delete the ones I don't need in my deck.


#### Usage

```
 py main.py --help
usage: main.py [-h] [--quiet] [--dry] deck

Send to anki deck

positional arguments:
  deck        Deck name

options:
  -h, --help  show this help message and exit
  --quiet     Decrease output verbosity
  --dry       Don't actually send to anki
```
