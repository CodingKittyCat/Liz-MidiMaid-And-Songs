import mido
import pretty_midi
import tkinter as tk
from tkinter import filedialog
import os

# === File Picker ===
def pick_midi_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a MIDI file",
        filetypes=[("MIDI files", "*.mid")]
    )
    return file_path

# === Convert Mido Tracks into PrettyMIDI Instruments with original names and tempo ===
def reconstruct_tracks_with_names_and_tempo(midi_path):
    mid = mido.MidiFile(midi_path)
    track_instruments = []
    track_names = {}
    tempo = 500000  # Default MIDI tempo

    # First pass: extract names and tempo
    for i, mido_track in enumerate(mid.tracks):
        for msg in mido_track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
            elif msg.type == 'track_name':
                track_names[i] = msg.name

    # Second pass: extract note data
    for i, mido_track in enumerate(mid.tracks):
        instrument = pretty_midi.Instrument(program=0, name=track_names.get(i, f"Track {i}"))
        current_tick = 0
        note_on_events = {}

        for msg in mido_track:
            current_tick += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                note_on_events[msg.note] = (current_tick, msg.velocity)
            elif (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)) and msg.note in note_on_events:
                start_tick, velocity = note_on_events.pop(msg.note)
                start_sec = mido.tick2second(start_tick, mid.ticks_per_beat, tempo)
                end_sec = mido.tick2second(current_tick, mid.ticks_per_beat, tempo)
                note = pretty_midi.Note(velocity=velocity, pitch=msg.note, start=start_sec, end=end_sec)
                instrument.notes.append(note)

        track_instruments.append(instrument)
    return track_instruments, tempo

# === Declutter Notes to Max Polyphony per Timestamp ===
def declutter_notes(instrument, max_notes=3, threshold=0.02, normalize_velocity=True, clamp_range=False):
    cleaned_notes = []
    chord_buffer = []
    last_start = None

    for note in sorted(instrument.notes, key=lambda n: n.start):
        if last_start is None or abs(note.start - last_start) <= threshold:
            chord_buffer.append(note)
            last_start = note.start
        else:
            cleaned_notes.extend(process_chord(chord_buffer, max_notes, normalize_velocity, clamp_range))
            chord_buffer = [note]
            last_start = note.start

    if chord_buffer:
        cleaned_notes.extend(process_chord(chord_buffer, max_notes, normalize_velocity, clamp_range))

    instrument.notes = cleaned_notes

# === Chord Processing Logic ===
def process_chord(notes, max_notes, normalize_velocity, clamp_range):
    notes.sort(key=lambda n: n.pitch)
    selected = []

    if len(notes) <= max_notes:
        selected = notes
    else:
        selected.append(notes[0])  # lowest
        selected.append(notes[-1])  # highest
        mid = [n for n in notes[1:-1]]
        selected += mid[:max_notes - len(selected)]

    if normalize_velocity:
        for n in selected:
            n.velocity = 100

    if clamp_range:
        for n in selected:
            while n.pitch < 48:
                n.pitch += 12
            while n.pitch > 84:
                n.pitch -= 12

    return selected

# === Main Script ===
def main():
    file_path = pick_midi_file()
    if not file_path:
        print("❌ No file selected. Exiting.")
        return

    instruments, tempo = reconstruct_tracks_with_names_and_tempo(file_path)
    print("\n🎼 Tracks based on MIDI file:")
    for i, inst in enumerate(instruments):
        print(f"  [{i}] {inst.name} | Notes: {len(inst.notes)}")

    try:
        targets = input("\n🎯 Enter track indexes to declutter (comma-separated, or 'all'): ").strip()
        if targets.lower() == "all":
            selected_indexes = list(range(len(instruments)))
        else:
            selected_indexes = [int(i.strip()) for i in targets.split(",")]

        max_polyphony = int(input("🎚️  Max notes per chord (1-3): ").strip())
        if not 1 <= max_polyphony <= 3:
            raise ValueError

        clamp_input = input("🗺️  Force notes into C3–C6 range? (y/n): ").strip().lower()
        clamp_range = clamp_input in ['y', 'yes']

    except Exception:
        print("❌ Invalid input. Exiting.")
        return

    # Create new PrettyMIDI file and inject tempo manually via mido
    base = os.path.basename(file_path)
    dir_name = os.path.dirname(file_path)
    output_name = f"Decluttered_FFXIV_Final_{base}"
    output_path = os.path.join(dir_name, output_name)

    pm_out = pretty_midi.PrettyMIDI()
    for idx in range(len(instruments)):
        if idx in selected_indexes:
            declutter_notes(instruments[idx], max_notes=max_polyphony, clamp_range=clamp_range)
        pm_out.instruments.append(instruments[idx])

    # Save PrettyMIDI to temp and inject tempo meta manually
    temp_path = os.path.join(dir_name, "_temp_output.mid")
    pm_out.write(temp_path)

    mid_final = mido.MidiFile(temp_path)
    tempo_meta = mido.MetaMessage('set_tempo', tempo=tempo, time=0)

    if len(mid_final.tracks) == 0:
        mid_final.tracks.append(mido.MidiTrack())

    mid_final.tracks[0].insert(0, tempo_meta)
    mid_final.save(output_path)
    os.remove(temp_path)

    print(f"\n✅ Decluttered file saved as: {output_path}")

if __name__ == "__main__":
    main()
