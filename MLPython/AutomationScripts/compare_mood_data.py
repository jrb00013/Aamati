#compare_mood_data.py

import os
import shutil
import pandas as pd

# Mood data dictionary
mood_table = {
    "chill": {
        "Tempo (BPM)": "60–115",
        "Density": "2–10",
        "Dynamic Range": "10–55",
        "Energy": "2-5",
        "Pitch Mean": "55–72",
        "Avg Polyphony": "1–4",
        "Syncopation": "0.00–0.04",
        "Desc": "Smooth, minimal, mellow tone. Longer notes, soft attack, low fill activity. Often low onset entropy. Think: sitting back, processing."
    },
    "energetic": {
        "Tempo (BPM)": "120–175",
        "Density": "20-40",
        "Dynamic Range": "75–130",
        "Energy": "13–15",
        "Pitch Mean": "55–70",
        "Avg Polyphony": "5–9",
        "Syncopation": "0.00–0.04",
        "Desc": "Driving, aggressive pulse. Punchy transients, dense and layered textures. Strong rhythm. Often minor swing."
    },
    "suspenseful": {
        "Tempo (BPM)": "75–125",
        "Density": "6–18",
        "Dynamic Range": "30–85",
        "Energy": "6–9",
        "Pitch Mean": "45–60",
        "Avg Polyphony": "2–5",
        "Syncopation": "0.01–0.06",
        "Desc": "Tense rhythms, minor scales, stabs and silences. Moderate density with erratic timing or FX presence."
    },
    "uplifting": {
        "Tempo (BPM)": "100–160",
        "Density": "10–26",
        "Dynamic Range": "55–120",
        "Energy": "7–13",
        "Pitch Mean": "62–80",
        "Avg Polyphony": "4–8",
        "Syncopation": "0.03–0.07",
        "Desc": "Bright major/mixolydian harmonies, crisp dynamics, stable pulse. Often swung or syncopated."
    },
    "ominous": {
        "Tempo (BPM)": "55–100",
        "Density": "4–12",
        "Dynamic Range": "10–90",
        "Energy": "5–8",
        "Pitch Mean": "42–58",
        "Avg Polyphony": "1–4",
        "Syncopation": "0.00–0.02",
        "Desc": "Brooding, dark timbres, sparse rhythm, low register with FX layers. Low fill activity and pitch mean."
    },
    "romantic": {
        "Tempo (BPM)": "60–125",
        "Density": "10–20",
        "Dynamic Range": "30–100",
        "Energy": "5–9",
        "Pitch Mean": "60–80",
        "Avg Polyphony": "2–5",
        "Syncopation": "0.02–0.06",
        "Desc": "Flowing, expressive melodies. Warm instruments, lush dynamics. Often rubato-like rhythmic feel."
    },
    "gritty": {
        "Tempo (BPM)": "135–180",
        "Density": "15–33",
        "Dynamic Range": "85–130",
        "Energy": "10–14",
        "Pitch Mean": "45–65",
        "Avg Polyphony": "5–10",
        "Syncopation": "0.00–0.03",
        "Desc": "Dirty, mechanical, and raw. Often feels industrial or punkish. Focused bursts of sound."
    },
    "dreamy": {
        "Tempo (BPM)": "70–110",
        "Density": "5–15",
        "Dynamic Range": "30–85",
        "Energy": "5–8",
        "Pitch Mean": "62–85",
        "Avg Polyphony": "2–6",
        "Syncopation": "0.03–0.08",
        "Desc": "Reverb-heavy, washed textures, layered pads or plucks. Mid swing with non-rigid rhythm."
    },
    "frantic": {
        "Tempo (BPM)": "160–250",
        "Density": "22–40",
        "Dynamic Range": "100–130",
        "Energy": "14–17",
        "Pitch Mean": "45–75",
        "Avg Polyphony": "7–15",
        "Syncopation": "0.04–0.10",
        "Desc": "Chaotic energy. Rapid onsets, wild rhythm, extreme fills and FX activity."
    },
    "focused": {
        "Tempo (BPM)": "83–135",
        "Density": "8–22",
        "Dynamic Range": "40–100",
        "Energy": "8–11",
        "Pitch Mean": "50–70",
        "Avg Polyphony": "4–7",
        "Syncopation": "0.00–0.03",
        "Desc": "Steady, repetitive motifs. Looped patterns with subtle intensity and mid polyphony."
    }
}

emoji_map = {
    "chill": "🧊",
    "dreamy": "💭",
    "focused": "🎯",
    "romantic": "💘",
    "uplifting": "🌅",
    "energetic": "⚡",
    "suspenseful": "🕳️",
    "ominous": "🌑",
    "gritty": "🪓",
    "frantic": "🌀"
}


print("🎛️  Mood Lookup Tool\n----------------------")
print("Type one or more moods separated by commas (e.g. chill,dreamy,focused)")
print("Type 'exit' or 'q' to quit.\n")

while True:
    user_input = input("Enter mood(s) to compare: ").strip().lower()
    if user_input in ["exit", "q"]:
        print("Exiting mood comparison. 👋")
        break

    # Split by commas or space
    moods = [m.strip() for m in user_input.replace(',', ' ').split()]
    if not moods:
        continue

    for mood in moods:
        if mood in mood_table:
            emoji = emoji_map.get(mood, "❓")
            print(f"\n{emoji} {mood.upper()}")
            for key, val in mood_table[mood].items():
                print(f"{key}: {val}")
        else:
            print(f"\n⚠️ Mood '{mood}' not found in table.")

    print("\n---\n")