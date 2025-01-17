# From https://github.com/kdrkdrkdr/AronaSpeaker/blob/main/ms_istft_vits/text/cleaners.py

import re
from text.japanese import japanese_to_romaji_with_accent
from text.symbols import symbols

_cleaner_cleans = re.compile("[" + "^".join(symbols) + "]")


def japanese_cleaners(text):
    text = japanese_to_romaji_with_accent(text)
    text = re.sub(r"([A-Za-z])$", r"\1.", text)
    return text


def japanese_cleaners2(text):
    text = japanese_cleaners(text).replace("ts", "ʦ").replace("...", "…")
    text = "".join(_cleaner_cleans.findall(text)).replace("_", "").replace(" ", "")
    return text
