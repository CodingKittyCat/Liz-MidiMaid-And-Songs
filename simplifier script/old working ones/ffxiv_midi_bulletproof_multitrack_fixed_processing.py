
import mido
import pretty_midi
import tkinter as tk
from tkinter import filedialog
import os

def pick_midi_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title="Select a MIDI file", filetypes=[("MIDI files", "*.mid")])

def pick_output_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select Output Folder")

def reconstruct_tracks_with_names_and_tempo(midi_path):
    mid = mido.MidiFile(midi_path)
    track_instruments = []
    track_names = {}
    tempo = None

    for i, mido_track in enumerate(mid.tracks):
        for msg in mido_track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
            elif msg.type == 'track_name':
                track_names[i] = msg.name

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
                duration_ticks = current_tick - start_tick
                duration_sec = mido.tick2second(duration_ticks, mid.ticks_per_beat, tempo)
                end_sec = start_sec + duration_sec
                note = pretty_midi.Note(velocity=velocity, pitch=msg.note, start=start_sec, end=end_sec)
                instrument.notes.append(note)

        track_instruments.append(instrument)
    return track_instruments, tempo

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

def process_chord(notes, max_notes, normalize_velocity, clamp_range):
    notes.sort(key=lambda n: n.pitch)
    selected = []

    if len(notes) <= max_notes:
        selected = notes
    else:
        selected.append(notes[0])
        selected.append(notes[-1])
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

def smart_transpose_to_range(instrument, low=48, high=84):
    if not instrument.notes:
        return

    avg_pitch = sum(note.pitch for note in instrument.notes) / len(instrument.notes)
    center_pitch = (low + high) // 2
    shift = int(round(center_pitch - avg_pitch))

    for note in instrument.notes:
        note.pitch += shift

    for note in instrument.notes:
        while note.pitch < low:
            note.pitch += 12
        while note.pitch > high:
            note.pitch -= 12

def main():
    file_path = pick_midi_file()
    if not file_path:
        print("❌ No file selected. Exiting.")
        return

    output_dir = pick_output_folder()
    if not output_dir:
        print("❌ No output folder selected. Exiting.")
        return

    instruments, tempo = reconstruct_tracks_with_names_and_tempo(file_path)
    print("\n🎼 Tracks in the MIDI:")
    for i, inst in enumerate(instruments):
        print(f"[{i}] {inst.name} | Notes: {len(inst.notes)}")

    print("\n🛠️ Mode Select:")
    print("  [1] Declutter and Remap")
    print("  [2] Smart Remap only (no declutter)")
    print("  [3] Declutter only (no remap)")

    mode_input = input("Pick mode [1/2/3]: ").strip()
    if mode_input == "1":
        mode = "declutter_remap"
    elif mode_input == "2":
        mode = "remap_only"
    elif mode_input == "3":
        mode = "declutter_only"
    else:
        print("❌ Invalid mode selected.")
        return

    targets = input("\n🎯 Enter track indexes to process (comma-separated, or 'all'): ").strip()
    if targets.lower() == "all":
        selected_indexes = list(range(len(instruments)))
    else:
        selected_indexes = [int(i.strip()) for i in targets.split(",")]

    max_notes_per_chord = 3
    clamp_range = True

    if mode != "remap_only":
        try:
            max_notes_per_chord = int(input("🎚️  Max Notes per Chord (1-3): ").strip())
            if not 1 <= max_notes_per_chord <= 3:
                raise ValueError
        except ValueError:
            print("❌ Invalid number. Exiting.")
            return

    base = os.path.basename(file_path)
    name_no_ext = os.path.splitext(base)[0]
    output_name = f"(Elizabeth Grimthane) {name_no_ext.replace('_', ' ').title()}.mid"
    output_path = os.path.join(output_dir, output_name)

    mid_final = mido.MidiFile()
    ticks_per_beat = mid_final.ticks_per_beat

    for i, idx in enumerate(range(len(instruments))):
        if idx in selected_indexes:
            if mode == "declutter_remap":
                declutter_notes(instruments[idx], max_notes=max_notes_per_chord, clamp_range=clamp_range)
                smart_transpose_to_range(instruments[idx])
            elif mode == "remap_only":
                smart_transpose_to_range(instruments[idx])
            elif mode == "declutter_only":
                declutter_notes(instruments[idx], max_notes=max_notes_per_chord, clamp_range=clamp_range)
        if idx in selected_indexes:
            track = mido.MidiTrack()
            mid_final.tracks.append(track)

            if i == 0:
                track.append(mido.MetaMessage("set_tempo", tempo=tempo, time=0))

            notes = []
            for note in instruments[idx].notes:
                notes.append((note.start, "on", note.pitch, note.velocity))
                notes.append((note.end, "off", note.pitch, 0))

            notes.sort()
            last_tick = 0
            for timestamp, kind, pitch, velocity in notes:
                tick = int(mido.second2tick(timestamp, ticks_per_beat, tempo))
                delta = tick - last_tick
                last_tick = tick
                if kind == "on":
                    track.append(mido.Message("note_on", note=pitch, velocity=velocity, time=delta))
                elif kind == "off":
                    track.append(mido.Message("note_off", note=pitch, velocity=velocity, time=delta))

    mid_final.save(output_path)
    print(f"\n✅ Final file saved to: {output_path}")

if __name__ == "__main__":
    main()
