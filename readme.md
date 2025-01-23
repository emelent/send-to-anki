#### Send to anki japanese

I made this script to just make the creation of japanese anki cards a bit easier
for myself, and it requires that you have anki running on your machine and have 
the [ankiconnect plugin](https://ankiweb.net/shared/info/2055492159) installed.


This script takes json data and turns it into japanese anki cards using the
Kaishi 1.5K Note type.


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


#### Generated card example

**Front**

![Anki card front](/example/front.png "Anki card front")

**Back**
![Anki card back](/example/back.png "Anki card back")

#### Usage

```
py main.py --help
usage: main.py [-h] [--quiet] [--dry] deck

Send to anki deck

options:
  -h, --help     show this help message and exit
  --deck DECK    Deck name
  --model MODEL  Model name
  --quiet        Decrease output verbosity
  --dry          Don't actually send to anki
```

So all in all I'd get my japanese text phrase then run this:

`jsonify_jp 今日はいいお天気ですね | python3 -m json.tool --no-ensure-ascii | py main.py --deck "<my-deck-name>"`


and the output would be something like this:

```

{
    "phrase": "今日はいいお天気ですね",
    "translation": "The weather is nice today",
    "furigana": "今日[きょう] は いい お天気[おてんき] です ね",
    "words": {
        "今日": {
            "furigana": {
                "今日": "きょう"
            },
            "definition": "today"
        },
        "いい": {
            "furigana": {
                "いい": "いい"
            },
            "definition": "good"
        },
        "天気": {
            "furigana": {
                "天": "てん",
                "気": "き"
            },
            "definition": "weather"
        }
    }
}


----------

{"action": "addNote", "version": 6, "params": {"note": {"deckName": "dummy", "modelName": "HomeMade", "fields": {"Word": "今日", "Word Reading": "きょう", "Word Meaning": "today", "Word Furigana": "今日[きょう]", "Sentence": "今日はいいお天気ですね", "Sentence Furigana": "今日[きょう] は いい お天気[おてんき] です ね", "Sentence Meaning": "The weather is nice today"}, "tags": ["custom_autobot"]}}}

----------

{"action": "addNote", "version": 6, "params": {"note": {"deckName": "dummy", "modelName": "HomeMade", "fields": {"Word": "いい", "Word Reading": "いい", "Word Meaning": "good", "Word Furigana": "いい", "Sentence": "今日はいいお天気ですね", "Sentence Furigana": "今日[きょう] は いい お天気[おてんき] です ね", "Sentence Meaning": "The weather is nice today"}, "tags": ["custom_autobot"]}}}

----------

{"action": "addNote", "version": 6, "params": {"note": {"deckName": "dummy", "modelName": "HomeMade", "fields": {"Word": "天気", "Word Reading": "てんき", "Word Meaning": "weather", "Word Furigana": "天[てん] 気[き]", "Sentence": "今日は いいお天気ですね", "Sentence Furigana": "今日[きょう] は いい お天気[おてんき] です ね", "Sentence Meaning": "The weather is nice today"}, "tags": ["custom_autobot"]}}}

----------
```

Downside is the formatting of the furigana of the kanji might vary. Sometimes chatgpt does what I want
and splits お天気 into two separate kana with furigana ("てん" and "き"), like the above, and other times it rolls it into one ("てんき"). But I suppose that's not all that bad, it just messes with the spacing in the cards. But it's not too big a deal to edit the single card I'm not satisfied with.

Also, since chatgpt responses are not deterministic, you may get varying responses, but they should all be the same in meaning.


