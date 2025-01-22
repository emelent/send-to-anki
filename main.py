# import sys
# import requests


# json_string = '{"name": "John", "age": 30, "city": "New York"}'
# data = json.loads(json_string)


sample_data = {
    "今日": {"furigana": {"今日": "きょう"}, "definition": "today"},
    "いい": {"furigana": {"いい": "いい"}, "definition": "good"},
    "お天気": {"furigana": {"天": "てん", "気": "き"}, "definition": "weather"},
    "だ": {"furigana": {"だ": "だ"}, "definition": "is (informal)"},
    "ね": {
        "furigana": {"ね": "ね"},
        "definition": "right? (sentence end particle indicating seeking agreement)",
    },
}


def prepare_anki_action(
    deckname,
    word,
    data,
    phrase="",
    phraseFurigana="",
    phraseTranslation="",
):
    furigana = ""
    reading = ""
    for k, v in data["furigana"].items():
        furigana += k if k == v else "{}[{}] ".format(k, v)
        reading += v

    return {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deckname,
                "modelName": "HomeMade",
                "fields": {
                    "Word": word,
                    "Word Reading": reading,
                    "Word Meaning": data["definition"],
                    "Word Furigana": furigana.strip(),
                    "Sentence": phrase,
                    "Sentence Furigana": phraseFurigana,
                    "Sentence Meaning": phraseTranslation,
                },
            }
        },
    }


if __name__ == "__main__":
    import json
    import sys

    json_str = sys.stdin.read().strip()
    print(json_str)
    print()
    data = json.loads(json_str)

    print("reading: {}".format(data["phraseFurigana"]))
    print("translation: {}\n".format(data["phraseTranslation"]))
    print("\n" + ("-" * 10) + "\n")

    phraseFurigana = data["phraseFurigana"]
    phrase = data["originalPhrase"]
    phraseTranslation = data["phraseTranslation"]

    for word, word_data in data["words"].items():
        anki_action = prepare_anki_action(
            deckname="dummy",
            word=word,
            data=word_data,
            phrase=phrase,
            phraseFurigana=phraseFurigana,
            phraseTranslation=phraseTranslation,
        )
        print(json.dumps(anki_action, ensure_ascii=False))
        print("\n" + ("-" * 10) + "\n")
