import json



data = {
    "hairPinLoop": ["UCCG", "GCAA", "UUCG"],
    "kissingLoop": [
        ["AAAGCGGUA", "AAACCGCUA"]
    ]
}



with open("default.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)