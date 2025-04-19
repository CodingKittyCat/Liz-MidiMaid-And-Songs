
import pretty_midi

def detect_key_signature(pm):
    # Analyze pitch histogram to find the most likely root
    histogram = [0] * 12
    for instrument in pm.instruments:
        for note in instrument.notes:
            histogram[note.pitch % 12] += 1
    root = max(range(12), key=lambda i: histogram[i])
    return root  # This is the tonic (0=C, 1=C#, ..., 11=B)

def smart_transpose_preserving_key(instrument, tonic, low=48, high=84):
    for note in instrument.notes:
        # Only transpose if the note is outside the target playable range
        if note.pitch < low or note.pitch > high:
            # Preserve intervals, only transpose by full octaves
            while note.pitch < low:
                note.pitch += 12
            while note.pitch > high:
                note.pitch -= 12
    instrument.notes.sort(key=lambda n: n.start)
