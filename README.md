# 🌸 The MIDI Maid 🌸  
#### Your faithful music-servant for cleaning up messy MIDIs ~  
Written and maintained with love by **Elizabeth Grimthane**  

---

## 💡 What is The MIDI Maid?

**The MIDI Maid** is a charming little command-line helper designed to clean, tidy, and prep your MIDI files for use in things like *Final Fantasy XIV* performances.  
She sweeps up cluttered notes, gently remaps pitch ranges, and ensures everything sounds lovely for your in-game concerts!

Maids, however, aren't miracle beings! It'll still require some fine-tuning here and there to create the perfect track.  
But you should be well on your way with The MIDI Maid by your side. ✨

---

## ✨ Features

Here’s everything The MIDI Maid can do for your messy little MIDI files:

---

### 🎼 Pitch Remapping to C3–C6
- Ensures all notes fall within the FFXIV play-safe range (C3–C6)
- Notes outside this range are transposed up or down by octaves
- Keeps everything musically intact and playable

---

### 🧹 Decluttering (Chord Reduction)
- Reduces dense or unplayable chords down to a maximum of **4 notes at once**
- Keeps essential harmony while improving MIDI performance usability
- Perfect for mimicking solo/duet performance constraints

---

### 🧠 Key-Aware Remapping
- Preserves musical key signatures while shifting notes into a playable range
- Great for ensuring transposed MIDIs still *sound* right
- Smart selection of octave shifts per note to avoid dissonance

---

### 🎛 Track-by-Track Control
- Lets you choose **specific tracks** to clean, or just say `"all"`
- Gives you a quick overview of each track's note count
- Useful for splitting out instruments, percussion, or vocals

---

### 🧺 Simple, Guided Workflow
- File picker: Choose your input MIDI
- Folder picker: Select output destination
- Menu: Choose how you’d like to clean it
- Prompt: Pick which tracks to clean

---

### 🍰 Cute & Custom Output Naming
- Automatically names cleaned files like:  
  `(Elizabeth Grimthane) Song Name.mid`  
- This will include a custom author name in the future!

---

## 🧹 How Does It Work?

It's super simple! Once you open the program, The MIDI Maid will guide you through her cleaning ritual, one dainty step at a time:

---

### 🪞 Step 1: Select Your MIDI File  
When prompted, a file picker will magically appear.  
Just select the `.mid` file you want The Maid to work on.

---

### 🧺 Step 2: Choose a Destination Folder  
Next, she'll ask where you want to save the cleaned-up version.  
A folder picker will appear – pick your favorite tidy space!

---

### 📑 Step 3: View the Tracks  
You'll see a list of tracks inside your MIDI file, along with their note counts.  
Each track has an index number like `[0]`, `[1]`, etc.

---

### ✨ Step 4: Pick a Cleaning Mode

Choose how you want The Maid to help:

```
[1] Declutter and Remap – Trim messy chords, fit to FFXIV play range (C3–C6)
[2] Just Remap – Gently shift all notes into C3–C6
[3] Just Declutter – Trim chords and clutter without changing pitches
[4] Remap with Preserved Keys – Advanced option to retain musical key
[5] Declutter then Remap with Key Awareness – Combo cleaning!
```

Just enter the number you like! 💕

---

### 🎻 Step 5: Select Tracks to Clean

Want to clean everything?  
Type:

```
all
```

Only want specific tracks?  
Type their numbers, like:

```
0, 1
```

The Maid will handle the rest with poise and grace. 🌟

---

## 🍰 Output

Once she’s finished tidying, you’ll find a polished new file saved in your chosen folder, with a lovely name like:

```
(Elizabeth Grimthane) Your Song.mid
```

Now it’s ready to perform — no clutter, no out-of-range notes, just magic!

---

## 💌 From The Author

This was made with care, stardust, and many cups of tea.  
If you enjoy The MIDI Maid, let her know with a song 🎶

Thank you for letting her help you with your music.  
She'll be waiting, feather duster in hand.

— *Elizabeth Grimthane*

---

_This repository also includes my personal MIDI files for demonstration or performance use._
