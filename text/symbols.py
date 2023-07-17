# From https://github.com/kdrkdrkdr/AronaSpeaker/blob/main/ms_istft_vits/text/symbols.py
""" from https://github.com/keithito/tacotron """
# Yes this is copied twice!

"""
Defines the set of symbols used in text input to the model.
"""
# japanese_cleaners2
_pad = "_"
_punctuation = ",.!?-~…"
_letters = "AEINOQUabdefghijkmnoprstuvwyzʃʧʦ↓↑ "


# Export all symbols:
symbols = [_pad] + list(_punctuation) + list(_letters)

# Special symbol ids
SPACE_ID = symbols.index(" ")
