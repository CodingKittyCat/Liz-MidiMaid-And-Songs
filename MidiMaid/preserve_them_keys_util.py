# preserve_them_keys_util.py
# Helper functions for FFXIV MIDI processing (mainly preserving the key as the fucker would go off key :SilvervalePouts:)
# Written by Elizabeth Grimthane

import pretty_midi

def detect_key_signature(pm):
    # Checks MIDI key signature metadata for global key
    if pm.key_signature_changes:
        return pm.key_signature_changes[0].key_number
    return 0  # default to C major

def smart_transpose_preserving_key(instrument, base_key):
    # Shifts notes into C3–C6 range while keeping melody
    for note in instrument.notes:
        while note.pitch < 48:
            note.pitch += 12
        while note.pitch > 84:
            note.pitch -= 12
