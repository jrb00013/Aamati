"""
Mood mappings and feature definitions for the Aamati ML system.
"""

# Define mood-to-feature mapping
MOOD_FEATURE_MAP = {
    "chill": {
        "timing_feel": "loose", 
        "rhythmic_density": "low", 
        "dynamic_intensity": "soft", 
        "fill_activity": "sparse", 
        "fx_character": "wet, wide, airy"
    },
    "energetic": {
        "timing_feel": "tight", 
        "rhythmic_density": "high", 
        "dynamic_intensity": "hard", 
        "fill_activity": "frequent", 
        "fx_character": "dry, punchy, sharp"
    },
    "suspenseful": {
        "timing_feel": "mid", 
        "rhythmic_density": "medium", 
        "dynamic_intensity": "varied", 
        "fill_activity": "moderate", 
        "fx_character": "dark, modulated, narrow"
    },
    "uplifting": {
        "timing_feel": "mid", 
        "rhythmic_density": "high", 
        "dynamic_intensity": "bright", 
        "fill_activity": "medium", 
        "fx_character": "shimmery, wide, echoing"
    },
    "ominous": {
        "timing_feel": "tight", 
        "rhythmic_density": "medium", 
        "dynamic_intensity": "deep", 
        "fill_activity": "sparse", 
        "fx_character": "saturated, low-end heavy"
    },
    "romantic": {
        "timing_feel": "loose", 
        "rhythmic_density": "medium", 
        "dynamic_intensity": "gentle", 
        "fill_activity": "occasional", 
        "fx_character": "warm, lush, resonant"
    },
    "gritty": {
        "timing_feel": "tight", 
        "rhythmic_density": "high", 
        "dynamic_intensity": "harsh", 
        "fill_activity": "irregular", 
        "fx_character": "distorted, mono, rough"
    },
    "dreamy": {
        "timing_feel": "loose", 
        "rhythmic_density": "low", 
        "dynamic_intensity": "light", 
        "fill_activity": "sparse", 
        "fx_character": "reverb-heavy, washed-out"
    },
    "frantic": {
        "timing_feel": "random", 
        "rhythmic_density": "very_high", 
        "dynamic_intensity": "wild", 
        "fill_activity": "bursty", 
        "fx_character": "glitchy, stuttered, noisy"
    },
    "focused": {
        "timing_feel": "tight", 
        "rhythmic_density": "medium", 
        "dynamic_intensity": "consistent", 
        "fill_activity": "minimal", 
        "fx_character": "clean, subtle, precise"
    }
}

# Define numeric mappings
TIMING_FEEL_MAP = {'tight': 0, 'mid': 1, 'loose': 2, 'random': 3}
RHYTHMIC_DENSITY_MAP = {'low': 0, 'medium': 1, 'high': 2, 'very_high': 3}
DYNAMIC_INTENSITY_MAP = {
    'soft': 0, 'gentle': 1, 'light': 2, 'bright': 3, 'deep': 4, 
    'varied': 5, 'consistent': 6, 'hard': 7, 'harsh': 8, 'wild': 9
}
FILL_ACTIVITY_MAP = {
    'sparse': 0, 'minimal': 1, 'occasional': 2, 'moderate': 3, 
    'medium': 4, 'frequent': 5, 'bursty': 6, 'irregular': 7
}
FX_CHARACTER_MAP = {
    'wet, wide, airy': 0, 'dry, punchy, sharp': 1, 'dark, modulated, narrow': 2,
    'shimmery, wide, echoing': 3, 'saturated, low-end heavy': 4, 'warm, lush, resonant': 5,
    'distorted, mono, rough': 6, 'reverb-heavy, washed-out': 7, 'glitchy, stuttered, noisy': 8,
    'clean, subtle, precise': 9
}

# Emoji mappings for UI
EMOJI_MAP = {
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

# Color mappings for terminal output
COLOR_MAP = {
    "chill": "\033[94m",      # Bright Blue 
    "dreamy": "\033[96m",     # Cyan
    "focused": "\033[92m",    # Green
    "romantic": "\033[38;5;205m",   # Pink
    "uplifting": "\033[38;5;208m",  # Orange
    "energetic": "\033[93m",  # Yellow
    "suspenseful": "\033[90m",# Dark gray
    "ominous": "\033[95m",    # Magenta
    "gritty": "\033[38;5;94m",     # Brown
    "frantic": "\033[91m",    # Bright red
}

RESET_COLOR = "\033[0m"

# Mood data dictionary for comparison tool
MOOD_DATA_TABLE = {
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
