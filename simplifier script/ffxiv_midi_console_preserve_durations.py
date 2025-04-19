
def declutter_midi_tracks_by_index(notes, max_simultaneous=6):
    if not notes:
        return []
    sorted_notes = sorted(notes, key=lambda n: (n.start, -n.velocity))
    active_notes = []
    result = []

    current_time = sorted_notes[0].start
    i = 0
    while i < len(sorted_notes):
        batch = []
        current_time = sorted_notes[i].start
        while i < len(sorted_notes) and sorted_notes[i].start == current_time:
            batch.append(sorted_notes[i])
            i += 1

        batch = sorted(batch, key=lambda n: (-n.velocity, n.pitch))
        batch = batch[:max_simultaneous]

        result.extend(batch)

    return result
