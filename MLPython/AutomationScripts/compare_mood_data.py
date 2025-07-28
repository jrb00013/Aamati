import os
import shutil
import pandas as pd
import textwrap

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

COLOR_MAP = {
    "chill": "\033[94m",      # Bright Blue 
    "dreamy": "\033[96m",     # Cyan
    "focused": "\033[92m",    # Green
    "romantic": "\033[38;5;205m" ,   # Pink
    "uplifting": "\033[38;5;208m",  # Orange
    "energetic": "\033[93m",  # Yellow
    "suspenseful": "\033[90m",# Dark gray
    "ominous": "\033[95m",    # Magenta
    "gritty": "\033[38;5;94m",     # Brown
    "frantic": "\033[91m",    # Bright red
}
RESET_COLOR = "\033[0m"

def format_column(mood: str, width: int = 35):
    data = mood_table[mood]
    emoji = emoji_map.get(mood, "❓")
    lines = [f"{emoji} {mood.upper()}".ljust(width), "-" * width]
    for key in ["Tempo (BPM)", "Density", "Dynamic Range", "Energy", "Pitch Mean", "Avg Polyphony", "Syncopation"]:
        val = data[key]
        lines.append(f"{key}: {val}".ljust(width))
    desc_lines = textwrap.wrap(f"Desc: {data['Desc']}", width)
    lines.extend(desc_lines)
    return lines

def format_mood_data(mood, data, width=40):
    lines = []
    color = COLOR_MAP.get(mood.lower(), "")
    reset = RESET_COLOR

    header = f"{mood.upper()}".center(width)
    lines.append(color + header + reset)
    lines.append(color + "-" * width + reset)

    for key, value in data.items():
        if key != "Desc":
            lines.append(color + f"{key}: {value}" + reset)
        else:
            # Wrap and indent description
            wrapped = textwrap.wrap(value, width=width - 2)
            lines.append(color + "Desc:" + reset)
            lines += [color + f"  {line}" + reset for line in wrapped]

    lines.append(color + "-" * width + reset)
    return lines

def print_side_by_side(mood_list):
    term_width = shutil.get_terminal_size().columns
    max_columns = min(3, len(mood_list))  # max 3 columns
    width_per_column = term_width // max_columns if max_columns else term_width
    gap = 4  # spaces between columns
    
    # Format blocks per mood, but keep them as list of strings
    formatted_blocks = [
        format_mood_data(mood.upper(), mood_table[mood.lower()], width_per_column - gap)
        for mood in mood_list
    ]
    
    # Pad each block with empty strings to match max length
    max_lines = max(len(block) for block in formatted_blocks)
    for block in formatted_blocks:
        while len(block) < max_lines:
            block.append('')
    
    for i in range(max_lines):
        line_pieces = []
        for block in formatted_blocks:
            line_pieces.append(block[i].ljust(width_per_column - gap))
        # Join columns with gap spaces between them
        print((" " * gap).join(line_pieces))
    
    print("-" * term_width)



print("🎛️  Mood Lookup Tool\n----------------------")
print("Type one or more moods separated by commas (e.g. chill,dreamy,focused)")
print("Type 'exit' or 'q' to quit.\n")

while True:
    user_input = input("Enter mood(s) to compare: ").strip().lower()
    if user_input in ["exit", "q"]:
        print("Exiting mood comparison. 👋")
        break

    # Clean input
    moods = [m.strip() for m in user_input.replace(',', ' ').split()]
    valid_moods = [m for m in moods if m in mood_table]
    invalid = [m for m in moods if m not in mood_table]

    if not valid_moods:
        print("⚠️ No valid moods entered.\n")
        continue

    if invalid:
        for mood in invalid:
            print(f"⚠️ Mood '{mood}' not found in table.")

    print()
    print_side_by_side(valid_moods)  #    limit to first 3 moods for now
