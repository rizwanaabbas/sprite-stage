"""Make a fresh OpenVoice and MeloTTS checkout usable for English lines only."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text()
    if new in text:
        print("already", label)
        return
    if old not in text:
        raise SystemExit(f"Could not patch {label}. Upstream {path.name} changed.")
    path.write_text(text.replace(old, new, 1))
    print("patched", label)


def main() -> None:
    replace_once(
        ROOT / "vendor/OpenVoice/openvoice/api.py",
        "    def __init__(self, *args, **kwargs):\n        super().__init__(*args, **kwargs)\n\n        if kwargs.get('enable_watermark', True):",
        "    def __init__(self, *args, **kwargs):\n        enable_watermark = kwargs.pop('enable_watermark', True)\n        super().__init__(*args, **kwargs)\n\n        if enable_watermark:",
        "openvoice watermark",
    )
    replace_once(
        ROOT / "vendor/MeloTTS/melo/text/cleaner.py",
        "from . import chinese, japanese, english, chinese_mix, korean, french, spanish\n"
        "from . import cleaned_text_to_sequence\nimport copy\n\n"
        "language_module_map = {\"ZH\": chinese, \"JP\": japanese, \"EN\": english, 'ZH_MIX_EN': chinese_mix, 'KR': korean,\n"
        "                    'FR': french, 'SP': spanish, 'ES': spanish}\n\n\n"
        "def clean_text(text, language):\n    language_module = language_module_map[language]",
        "from . import cleaned_text_to_sequence\nimport copy\nimport importlib\n\n"
        "_LANGUAGE_MODULES = {\n"
        '    "ZH": "chinese", "JP": "japanese", "EN": "english", "ZH_MIX_EN": "chinese_mix",\n'
        '    "KR": "korean", "FR": "french", "SP": "spanish", "ES": "spanish",\n}\n\n\n'
        "def _language_module(language):\n"
        "    return importlib.import_module('.' + _LANGUAGE_MODULES[language], __package__)\n\n\n"
        "def clean_text(text, language):\n    language_module = _language_module(language)",
        "melo cleaner",
    )
    replace_once(
        ROOT / "vendor/MeloTTS/melo/text/cleaner.py",
        "def clean_text_bert(text, language, device=None):\n    language_module = language_module_map[language]",
        "def clean_text_bert(text, language, device=None):\n    language_module = _language_module(language)",
        "melo cleaner bert",
    )
    replace_once(
        ROOT / "vendor/MeloTTS/melo/text/japanese.py",
        "model_id = 'tohoku-nlp/bert-base-japanese-v3'\ntokenizer = AutoTokenizer.from_pretrained(model_id)\ndef g2p(norm_text):\n\n    tokenized = tokenizer.tokenize(norm_text)",
        "model_id = 'tohoku-nlp/bert-base-japanese-v3'\n_tokenizer = None\n\n\n"
        "def _japanese_tokenizer():\n    global _tokenizer\n    if _tokenizer is None:\n"
        "        _tokenizer = AutoTokenizer.from_pretrained(model_id)\n    return _tokenizer\n\n\n"
        "def g2p(norm_text):\n\n    tokenized = _japanese_tokenizer().tokenize(norm_text)",
        "melo japanese",
    )
    bert = ROOT / "vendor/MeloTTS/melo/text/__init__.py"
    text = bert.read_text()
    if "def get_bert" in text and "english_bert" in text.split("def get_bert", 1)[1][:800]:
        start = text.index("def get_bert")
        text = text[:start] + (
            "def get_bert(norm_text, word2ph, language, device):\n"
            "    if language == 'EN':\n"
            "        from .english_bert import get_bert_feature as bert_fn\n"
            "    elif language == 'ZH':\n"
            "        from .chinese_bert import get_bert_feature as bert_fn\n"
            "    elif language == 'JP':\n"
            "        from .japanese_bert import get_bert_feature as bert_fn\n"
            "    elif language == 'ZH_MIX_EN':\n"
            "        from .chinese_mix import get_bert_feature as bert_fn\n"
            "    elif language in ('SP', 'ES'):\n"
            "        from .spanish_bert import get_bert_feature as bert_fn\n"
            "    elif language == 'FR':\n"
            "        from .french_bert import get_bert_feature as bert_fn\n"
            "    elif language == 'KR':\n"
            "        from .korean import get_bert_feature as bert_fn\n"
            "    else:\n"
            "        raise KeyError(language)\n"
            "    return bert_fn(norm_text, word2ph, device)\n"
        )
        bert.write_text(text)
        print("patched melo bert")
    else:
        print("already melo bert")


if __name__ == "__main__":
    main()
