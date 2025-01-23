"""
sample_data = {
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
    },
}
"""


def prepare_anki_action(
    deck,
    model,
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
                "deckName": deck,
                "modelName": model,
                "fields": {
                    "Word": word,
                    "Word Reading": reading,
                    "Word Meaning": data["definition"],
                    "Word Furigana": furigana.strip(),
                    "Sentence": phrase,
                    "Sentence Furigana": phraseFurigana,
                    "Sentence Meaning": phraseTranslation,
                },
                "tags": ["custom_autobot"],
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
    parser.add_argument("--deck", type=str, help="Deck name")
    parser.add_argument("--model", type=str, default="Kaishi 1.5k", help="Model name")
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
            deck=args.deck,
            model=args.model,
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
