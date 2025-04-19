# The Midi Maid
# Script to declutter and transpose MIDI files for in-game play
# Written and maintained by Elizabeth Grimthane

print("=" * 40)
print("         The MIDI Maid")
print("     by Elizabeth Grimthane")
print("  Performing all midi maid cleaning duties for you!")
print("=" * 40 + "\n")

import os
import tkinter as tk
from tkinter import filedialog
import pretty_midi
import preserve_them_keys_util as pres_keys_util
import declutterer_clean_thingywingy_util as declutterer_utils
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


# Opens the file picker so you can grab a MIDI file from wherever
def get_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid")])

# lets you choose a folder to save the edited MIDI file into
def get_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()

# Prints out each track's name and how many notes it contains
def show_tracks(mid):
    print("\nTracks in the MIDI file:")
    for i, inst in enumerate(mid.instruments):
        print(f"[{i}] {inst.name or 'Untitled'} | Notes: {len(inst.notes)}")

# Makes sure every note fits within C3–C6 range for FFXIV play
def fix_range(note):
    while note.pitch < 48:
        note.pitch += 12
    while note.pitch > 84:
        note.pitch -= 12

# Main logic for loading the MIDI, letting the user pick what to fix,
# and applying the selected operations to the chosen tracks.
def run():
    midipath = get_file()
    if not midipath:
        print("No file selected.")
        return
    outfolder = get_folder()
    if not outfolder:
        print("No folder selected.")
        return

    midi = pretty_midi.PrettyMIDI(midipath)
    show_tracks(midi)

    print("\nMode Select (pick number):")
    print("[1] Declutter and Remap")                      
    print("[2] Just Remap")                               
    print("[3] Just Declutter")                           
    print("[4] Remap with Preserved Keys (fucking cunt of a code)")                 
    print("[5] Declutter Remap (with preserved keys)")

    valid_modes = {"1", "2", "3", "4", "5"}
    mode = input("Choose a number (1-5): ").strip()
    while mode not in valid_modes:
        mode = input("Invalid choice. Choose a number from 1 to 5: ").strip()

    pick = input("Tracks to fix? (comma-separated or 'all'): ").strip().lower()
    if pick == "all":
        targets = list(range(len(midi.instruments)))
    else:
        try:
            targets = [int(x) for x in pick.split(",") if x.strip().isdigit()]
            if not all(0 <= i < len(midi.instruments) for i in targets):
                raise ValueError
        except ValueError:
            print("Invalid track numbers given. Exiting.")
            return
 
    # Detect key if needed
    key = pres_keys_util.detect_key_signature(midi) if mode in ["4", "5"] else None

    # Go through each track the user picked and apply the chosen fix
    for i in targets:
        inst = midi.instruments[i]
        notes = inst.notes

        if mode == "1":
            # Tidy up busy chords, then shift everything to C3–C6 range
            cleaned = declutterer_utils.declutter_midi_tracks_by_index(notes)
            for n in cleaned:
                fix_range(n)
            inst.notes = cleaned

        elif mode == "2":
            # Skip decluttering, just squish notes into the FFXIV-safe range
            for n in notes:
                fix_range(n)

        elif mode == "3":
            # Only reduce chords, no pitch shifting
            inst.notes = declutterer_utils.declutter_midi_tracks_by_index(notes)

        elif mode == "4":
            # Keep the key signature intact while shifting notes
            pres_keys_util.smart_transpose_preserving_key(inst, key)

        elif mode == "5":
            # Declutter first, then preserve the key while remapping range
            inst.notes = declutterer_utils.declutter_midi_tracks_by_index(notes)
            pres_keys_util.smart_transpose_preserving_key(inst, key)
        inst = midi.instruments[i]
        notes = inst.notes

        if mode == "1":
            cleaned = declutterer_utils.declutter_midi_tracks_by_index(notes)
            for n in cleaned:
                fix_range(n)
            inst.notes = cleaned

        elif mode == "2":
            for n in notes:
                fix_range(n)

        elif mode == "3":
            inst.notes = declutterer_utils.declutter_midi_tracks_by_index(notes)

        elif mode == "4":
            pres_keys_util.smart_transpose_preserving_key(inst, key)

        elif mode == "5":
            inst.notes = declutterer_utils.declutter_midi_tracks_by_index(notes)
            pres_keys_util.smart_transpose_preserving_key(inst, key)

    outname = os.path.basename(midipath).replace("_", " ")
    # Clean output name + save to user-picked folder
    outpath = os.path.join(outfolder, f"(Elizabeth Grimthane) {outname}")
    # Done, write it out
    midi.write(outpath)
    print(f"Saved to: {outpath}")

run()
