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


def create_logger(quiet):
    if quiet:
        return lambda *_: None
    return print


if __name__ == "__main__":
    import json
    import sys
    import requests as r
    import argparse

    parser = argparse.ArgumentParser(description="Send to anki deck")
    parser.add_argument("deck", type=str, help="Name of the deck to send notes to")
    parser.add_argument(
        "--quiet", action="store_true", help="Decrease output verbosity"
    )
    parser.add_argument(
        "--dry", action="store_true", help="Don't actually send to anki"
    )

    args = parser.parse_args()

    json_str = sys.stdin.read().strip()

    log = create_logger(args.quiet)
    log(json_str)
    log()
    data = json.loads(json_str)
    log("\n" + ("-" * 10) + "\n")

    phraseFurigana = data["furigana"]
    phrase = data["phrase"]
    phraseTranslation = data["translation"]

    for word, word_data in data["words"].items():
        anki_action = prepare_anki_action(
            deckname="dummy",
            word=word,
            data=word_data,
            phrase=phrase,
            phraseFurigana=phraseFurigana,
            phraseTranslation=phraseTranslation,
        )
        log(json.dumps(anki_action, ensure_ascii=False))

        if not args.dry:
            # send to anki
            response = r.post("http://localhost:8765", json=anki_action)
            log("\n")
            log("Response Body:", response.json())

        log("\n" + ("-" * 10) + "\n")
