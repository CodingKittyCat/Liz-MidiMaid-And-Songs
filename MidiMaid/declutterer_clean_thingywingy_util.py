# declutterer_clean_thingywingy_util.py
# Declutters MIDI by reducing simultaneous notes (preserving rhythm)
# Written by Elizabeth Grimthane

from collections import defaultdict

def declutter_midi_tracks_by_index(notes, max_simultaneous=6):
    # Reduce chords per timestamp while keeping durations intact
    grouped = defaultdict(list)
    for note in notes:
        grouped[note.start].append(note)
    
    cleaned = []
    for start_time, group in grouped.items():
        # Prioritize by velocity, then pitch
        group.sort(key=lambda n: (-n.velocity, n.pitch))
        cleaned.extend(group[:max_simultaneous])
    
    return sorted(cleaned, key=lambda n: n.start)
