
import os
import tkinter as tk
from tkinter import filedialog
import pretty_midi
from ffxiv_midi_fixer_utils import detect_key_signature, smart_transpose_preserving_key

from ffxiv_midi_console_preserve_durations import declutter_midi_tracks_by_index

def pick_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid")])

def pick_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()

def load_midi_and_list_tracks(file_path):
    pm = pretty_midi.PrettyMIDI(file_path)
    print("\n🎼 Tracks in the MIDI:")
    for i, inst in enumerate(pm.instruments):
        print(f"[{i}] {inst.name or 'Untitled'} | Program: {inst.program} | Notes: {len(inst.notes)}")
    return pm

def main():
    file_path = pick_file()
    if not file_path:
        print("❌ No MIDI file selected.")
        return

    output_dir = pick_folder()
    if not output_dir:
        print("❌ No output directory selected.")
        return

    pm = load_midi_and_list_tracks(file_path)
    instruments = pm.instruments

    print("\n🛠️ Mode Select:")
    print("[1] Declutter and Remap")
    print("[2] Smart Remap only (no declutter)")
    print("[3] Declutter only (no remap)")
    print("[4] Smart Remap (Preserve Musical Key) only")
    mode = input("Pick mode [1/2/3/4]: ")

    selected = input("Enter track indexes to process (comma-separated, or 'all'): ")
    if selected.lower() == 'all':
        selected_indexes = list(range(len(instruments)))
    else:
        selected_indexes = [int(x.strip()) for x in selected.split(',') if x.strip().isdigit()]

    grouped = {}
    for idx in selected_indexes:
        grouped[idx] = instruments[idx].notes.copy()

    if mode == "1":
        for idx in selected_indexes:
            instruments[idx].notes = declutter_midi_tracks_by_index(grouped[idx])
    elif mode == "2":
        for idx in selected_indexes:
            for note in instruments[idx].notes:
                while note.pitch < 48:
                    note.pitch += 12
                while note.pitch > 84:
                    note.pitch -= 12
    elif mode == "3":
        for idx in selected_indexes:
            instruments[idx].notes = declutter_midi_tracks_by_index(grouped[idx])
    elif mode == "4":
        tonic = detect_key_signature(pm)
        for idx in selected_indexes:
            smart_transpose_preserving_key(instruments[idx], tonic)
    else:
        print("❌ Invalid mode selected.")
        return

    out_name = os.path.basename(file_path).replace("_", " ")
    out_path = os.path.join(output_dir, f"(Elizabeth Grimthane) {out_name}")
    pm.write(out_path)
    print(f"✅ Saved: {out_path}")

if __name__ == "__main__":
    main()
