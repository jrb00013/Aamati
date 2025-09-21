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

def parse_range(range_str):
    """Parse range string like '60–115' or '2-5' and return min, max values"""
    # Handle different dash types and formats
    range_str = range_str.replace('–', '-').replace('—', '-').strip()
    
    if '-' in range_str:
        parts = range_str.split('-')
        if len(parts) == 2:
            try:
                min_val = float(parts[0].strip())
                max_val = float(parts[1].strip())
                return min_val, max_val
            except ValueError:
                return None, None
    else:
        try:
            val = float(range_str)
            return val, val
        except ValueError:
            return None, None
    
    return None, None

def combine_ranges(range1, range2):
    """Combine two ranges and return a new range string"""
    min1, max1 = parse_range(range1)
    min2, max2 = parse_range(range2)
    
    if min1 is None or min2 is None:
        return f"{range1} + {range2}"
    
    # Average the ranges
    new_min = (min1 + min2) / 2
    new_max = (max1 + max2) / 2
    
    # Format based on whether it's a whole number or decimal
    if new_min == int(new_min) and new_max == int(new_max):
        return f"{int(new_min)}–{int(new_max)}"
    else:
        return f"{new_min:.1f}–{new_max:.1f}"

def create_hybrid_mood(mood1, mood2):
    """Create a hybrid mood by combining attributes of two moods"""
    data1 = mood_table[mood1.lower()]
    data2 = mood_table[mood2.lower()]
    
    hybrid_name = f"{mood1.lower()}-{mood2.lower()}"
    
    # Combine each attribute
    hybrid_data = {}
    hybrid_calculation = {}  # Store calculation details
    
    for key in data1.keys():
        if key == "Desc":
            # Combine descriptions with order sensitivity
            desc1 = data1[key]
            desc2 = data2[key]
            
            # Create order-specific hybrid descriptions with meaningful transitions
            combo = f"{mood1.lower()}-{mood2.lower()}"
            
            hybrid_descriptions = {
                # Chill combinations
                "chill-dreamy": f"A chill-dreamy hybrid: Smooth minimalism meets ethereal textures. {desc1[:len(desc1)//2]}... enhanced by {desc2[:len(desc2)//2]}...",
                "dreamy-chill": f"A dreamy-chill hybrid: Ethereal atmospheres grounded in smooth minimalism. {desc2[:len(desc2)//2]}... anchored by {desc1[:len(desc1)//2]}...",
                
                "chill-energetic": f"A chill-energetic hybrid: Relaxed vibes energized with driving rhythms. {desc1[:len(desc1)//2]}... propelled by {desc2[:len(desc2)//2]}...",
                "energetic-chill": f"An energetic-chill hybrid: High-energy beats cooled into smooth grooves. {desc1[:len(desc1)//2]}... mellowed by {desc2[:len(desc2)//2]}...",
                
                "chill-suspenseful": f"A chill-suspenseful hybrid: Mellow tones infused with subtle tension. {desc1[:len(desc1)//2]}... darkened by {desc2[:len(desc2)//2]}...",
                "suspenseful-chill": f"A suspenseful-chill hybrid: Tense atmospheres softened into calm. {desc1[:len(desc1)//2]}... eased by {desc2[:len(desc2)//2]}...",
                
                "chill-uplifting": f"A chill-uplifting hybrid: Relaxed vibes brightened with optimism. {desc1[:len(desc1)//2]}... elevated by {desc2[:len(desc2)//2]}...",
                "uplifting-chill": f"An uplifting-chill hybrid: Bright energy cooled into gentle warmth. {desc1[:len(desc1)//2]}... grounded by {desc2[:len(desc2)//2]}...",
                
                "chill-ominous": f"A chill-ominous hybrid: Smooth textures darkened with foreboding. {desc1[:len(desc1)//2]}... shadowed by {desc2[:len(desc2)//2]}...",
                "ominous-chill": f"An ominous-chill hybrid: Dark atmospheres softened into calm. {desc1[:len(desc1)//2]}... lightened by {desc2[:len(desc2)//2]}...",
                
                "chill-romantic": f"A chill-romantic hybrid: Relaxed vibes warmed with emotional depth. {desc1[:len(desc1)//2]}... enriched by {desc2[:len(desc2)//2]}...",
                "romantic-chill": f"A romantic-chill hybrid: Passionate melodies cooled into gentle intimacy. {desc1[:len(desc1)//2]}... soothed by {desc2[:len(desc2)//2]}...",
                
                "chill-gritty": f"A chill-gritty hybrid: Smooth tones roughened with raw edge. {desc1[:len(desc1)//2]}... sharpened by {desc2[:len(desc2)//2]}...",
                "gritty-chill": f"A gritty-chill hybrid: Raw energy smoothed into controlled power. {desc1[:len(desc1)//2]}... refined by {desc2[:len(desc2)//2]}...",
                
                "chill-frantic": f"A chill-frantic hybrid: Calm vibes electrified with chaotic energy. {desc1[:len(desc1)//2]}... disrupted by {desc2[:len(desc2)//2]}...",
                "frantic-chill": f"A frantic-chill hybrid: Chaotic energy cooled into controlled chaos. {desc1[:len(desc1)//2]}... stabilized by {desc2[:len(desc2)//2]}...",
                
                "chill-focused": f"A chill-focused hybrid: Relaxed vibes concentrated into precision. {desc1[:len(desc1)//2]}... sharpened by {desc2[:len(desc2)//2]}...",
                "focused-chill": f"A focused-chill hybrid: Concentrated energy relaxed into flow. {desc1[:len(desc1)//2]}... eased by {desc2[:len(desc2)//2]}..."
            }
            
            hybrid_data[key] = hybrid_descriptions.get(combo, f"A {mood1}-{mood2} hybrid: {desc1[:len(desc1)//2]}... blended with {desc2[:len(desc2)//2]}...")
        else:
            # Combine ranges with detailed calculation
            range1 = data1[key]
            range2 = data2[key]
            
            # Parse ranges
            min1, max1 = parse_range(range1)
            min2, max2 = parse_range(range2)
            
            if min1 is not None and min2 is not None:
                # Research-based mood-specific emotional weighting
                # Based on Music Emotion Classification literature (Dhanapala & Samarasinghe, 2024)
                
                # Define emotional intensity and dominance patterns
                emotional_patterns = {
                    # High arousal moods (energetic, frantic, uplifting)
                    'energetic': {'dominance': 0.8, 'arousal': 'high', 'valence': 'positive'},
                    'frantic': {'dominance': 0.85, 'arousal': 'very_high', 'valence': 'mixed'},
                    'uplifting': {'dominance': 0.75, 'arousal': 'high', 'valence': 'positive'},
                    'gritty': {'dominance': 0.8, 'arousal': 'high', 'valence': 'negative'},
                    
                    # Medium arousal moods (focused, suspenseful, romantic)
                    'focused': {'dominance': 0.7, 'arousal': 'medium', 'valence': 'neutral'},
                    'suspenseful': {'dominance': 0.75, 'arousal': 'medium', 'valence': 'negative'},
                    'romantic': {'dominance': 0.65, 'arousal': 'medium', 'valence': 'positive'},
                    'ominous': {'dominance': 0.7, 'arousal': 'medium', 'valence': 'negative'},
                    
                    # Low arousal moods (chill, dreamy)
                    'chill': {'dominance': 0.6, 'arousal': 'low', 'valence': 'neutral'},
                    'dreamy': {'dominance': 0.55, 'arousal': 'low', 'valence': 'positive'}
                }
                
                # Get emotional patterns for both moods
                pattern1 = emotional_patterns.get(mood1.lower(), {'dominance': 0.6, 'arousal': 'medium', 'valence': 'neutral'})
                pattern2 = emotional_patterns.get(mood2.lower(), {'dominance': 0.6, 'arousal': 'medium', 'valence': 'neutral'})
                
                # Calculate dynamic weights based on emotional dominance and arousal
                # ORDER MATTERS! First mood gets significant priority
                base_weight1 = pattern1['dominance'] + 0.2  # First mood gets +20% boost
                base_weight2 = pattern2['dominance']
                
                # Adjust weights based on arousal levels (high arousal moods dominate)
                arousal_boost = {
                    'very_high': 0.15,
                    'high': 0.1,
                    'medium': 0.05,
                    'low': 0.0
                }
                
                weight1 = base_weight1 + arousal_boost.get(pattern1['arousal'], 0.05)
                weight2 = base_weight2 + arousal_boost.get(pattern2['arousal'], 0.05)
                
                # Normalize weights to sum to 1.0
                total_weight = weight1 + weight2
                weight1 = weight1 / total_weight
                weight2 = weight2 / total_weight
                
                # Calculate weighted hybrid values
                hybrid_min = (min1 * weight1) + (min2 * weight2)
                hybrid_max = (max1 * weight1) + (max2 * weight2)
                
                # Format result
                if hybrid_min == int(hybrid_min) and hybrid_max == int(hybrid_max):
                    result_str = f"{int(hybrid_min)}–{int(hybrid_max)}"
                else:
                    result_str = f"{hybrid_min:.1f}–{hybrid_max:.1f}"
                
                hybrid_data[key] = result_str
                
                # Store calculation details
                hybrid_calculation[key] = {
                    'mood1': f"{mood1}: {range1}",
                    'mood2': f"{mood2}: {range2}",
                    'calculation': f"({min1:.1f}×{weight1:.2f}+{min2:.1f}×{weight2:.2f}) to ({max1:.1f}×{weight1:.2f}+{max2:.1f}×{weight2:.2f})",
                    'result': result_str
                }
            else:
                # Fallback if parsing fails
                hybrid_data[key] = f"{range1} + {range2}"
                hybrid_calculation[key] = {
                    'mood1': f"{mood1}: {range1}",
                    'mood2': f"{mood2}: {range2}",
                    'calculation': "Unable to parse ranges",
                    'result': f"{range1} + {range2}"
                }
    
    return hybrid_name, hybrid_data, hybrid_calculation

def get_hybrid_color(mood1, mood2):
    """Get a unique color for hybrid combinations"""
    hybrid_colors = {
        "chill-dreamy": "\033[96m",      # Cyan
        "chill-energetic": "\033[93m",   # Yellow
        "chill-suspenseful": "\033[90m", # Dark gray
        "chill-uplifting": "\033[94m",   # Blue
        "chill-ominous": "\033[95m",     # Magenta
        "chill-romantic": "\033[38;5;205m", # Pink
        "chill-gritty": "\033[38;5;94m", # Brown
        "chill-frantic": "\033[91m",     # Red
        "chill-focused": "\033[92m",     # Green
        "dreamy-energetic": "\033[38;5;208m", # Orange
        "dreamy-suspenseful": "\033[38;5;141m", # Purple
        "dreamy-uplifting": "\033[38;5;214m", # Gold
        "dreamy-ominous": "\033[38;5;88m", # Dark red
        "dreamy-romantic": "\033[38;5;211m", # Light pink
        "dreamy-gritty": "\033[38;5;130m", # Dark orange
        "dreamy-frantic": "\033[38;5;196m", # Bright red
        "dreamy-focused": "\033[38;5;154m", # Light green
        "energetic-suspenseful": "\033[38;5;166m", # Dark orange
        "energetic-uplifting": "\033[38;5;220m", # Bright yellow
        "energetic-ominous": "\033[38;5;124m", # Dark red
        "energetic-romantic": "\033[38;5;203m", # Pink
        "energetic-gritty": "\033[38;5;94m", # Brown
        "energetic-frantic": "\033[38;5;196m", # Bright red
        "energetic-focused": "\033[38;5;154m", # Light green
        "suspenseful-uplifting": "\033[38;5;172m", # Orange
        "suspenseful-ominous": "\033[38;5;88m", # Dark red
        "suspenseful-romantic": "\033[38;5;181m", # Light purple
        "suspenseful-gritty": "\033[38;5;130m", # Dark orange
        "suspenseful-frantic": "\033[38;5;196m", # Bright red
        "suspenseful-focused": "\033[38;5;154m", # Light green
        "uplifting-ominous": "\033[38;5;166m", # Dark orange
        "uplifting-romantic": "\033[38;5;211m", # Light pink
        "uplifting-gritty": "\033[38;5;130m", # Dark orange
        "uplifting-frantic": "\033[38;5;196m", # Bright red
        "uplifting-focused": "\033[38;5;154m", # Light green
        "ominous-romantic": "\033[38;5;181m", # Light purple
        "ominous-gritty": "\033[38;5;88m", # Dark red
        "ominous-frantic": "\033[38;5;196m", # Bright red
        "ominous-focused": "\033[38;5;154m", # Light green
        "romantic-gritty": "\033[38;5;130m", # Dark orange
        "romantic-frantic": "\033[38;5;196m", # Bright red
        "romantic-focused": "\033[38;5;154m", # Light green
        "gritty-frantic": "\033[38;5;196m", # Bright red
        "gritty-focused": "\033[38;5;154m", # Light green
        "frantic-focused": "\033[38;5;196m", # Bright red
    }
    
    # Try both combinations
    combo1 = f"{mood1.lower()}-{mood2.lower()}"
    combo2 = f"{mood2.lower()}-{mood1.lower()}"
    
    return hybrid_colors.get(combo1, hybrid_colors.get(combo2, "\033[97m"))  # Default to white

def print_hybrid_mood(mood1, mood2):
    """Print a hybrid mood combination with detailed calculations"""
    hybrid_name, hybrid_data, hybrid_calculation = create_hybrid_mood(mood1, mood2)
    
    # Get hybrid-specific color
    color = get_hybrid_color(mood1, mood2)
    reset = RESET_COLOR
    
    print(f"\n🔀 HYBRID MOOD: {color}{hybrid_name.upper()}{reset}")
    print("=" * 60)
    
    # Show calculation breakdown first
    print(f"{color}🧮 CALCULATION BREAKDOWN:{reset}")
    print("-" * 40)
    
    for key, calc_info in hybrid_calculation.items():
        if key != "Desc":
            print(f"{color}{key}:{reset}")
            print(f"  {calc_info['mood1']}")
            print(f"  {calc_info['mood2']}")
            print(f"  🧮 {calc_info['calculation']}")
            print(f"  ✅ Result: {calc_info['result']}")
            print()
    
    # Show final calculated attributes below calculations
    print(f"{color}📊 FINAL HYBRID ATTRIBUTES:{reset}")
    print("-" * 40)
    
    for key, value in hybrid_data.items():
        if key != "Desc":
            print(f"{color}{key}:{reset} {value}")
    
    print()
    print(f"{color}📝 DESCRIPTION:{reset}")
    print("-" * 20)
    desc = hybrid_data.get('Desc', '')
    wrapped = textwrap.wrap(desc, width=60)
    for line in wrapped:
        print(f"{color}  {line}{reset}")
    
    print("=" * 60)



print("🎛️  Mood Lookup Tool\n----------------------")
print("Choose your mode:")
print("1️⃣  Compare moods side-by-side (e.g. chill dreamy)")
print("2️⃣  Create hybrid mood combination (e.g. chill-dreamy)")
print("Type 'exit' or 'q' to quit.\n")

# Initial mode selection
while True:
    mode_choice = input("Choose mode (1 or 2): ").strip()
    if mode_choice in ["exit", "q"]:
        print("Exiting mood comparison. 👋")
        exit()
    elif mode_choice == "change":
        print("⚠️ Please choose a mode first (1 or 2).")
        continue
    elif mode_choice in ["1", "2"]:
        break
    else:
        print("⚠️ Please choose 1 or 2.")

current_mode = mode_choice
if current_mode == "1":
    print("\n📊 COMPARISON MODE ACTIVE")
    print("Type moods separated by spaces (e.g. chill dreamy focused)")
    print("Type 'change' to switch modes, 'exit' to quit")
elif current_mode == "2":
    print("\n🔀 HYBRID MODE ACTIVE")
    print("Type one mood for single display, or two moods for hybrid (e.g. chill dreamy)")
    print("Type 'change' to switch modes, 'exit' to quit")

while True:
    if current_mode == "1":
        user_input = input("\nEnter mood(s) to compare: ").strip().lower()
        
        if user_input in ["exit", "q"]:
            print("Exiting mood comparison. 👋")
            break
        elif user_input == "change":
            print("\nChoose your mode:")
            print("1️⃣  Compare moods side-by-side (e.g. chill dreamy)")
            print("2️⃣  Create hybrid mood combination (e.g. chill-dreamy)")
            mode_choice = input("Choose mode (1 or 2): ").strip()
            if mode_choice in ["exit", "q"]:
                print("Exiting mood comparison. 👋")
                break
            elif mode_choice == "1":
                current_mode = "1"
                print("\n📊 COMPARISON MODE ACTIVE")
                print("Type moods separated by spaces (e.g. chill dreamy focused)")
                print("Type 'change' to switch modes, 'exit' to quit")
                continue
            elif mode_choice == "2":
                current_mode = "2"
                print("\n🔀 HYBRID MODE ACTIVE")
                print("Type one mood for single display, or two moods for hybrid (e.g. chill dreamy)")
                print("Type 'change' to switch modes, 'exit' to quit")
                continue
            else:
                print("⚠️ Please choose 1 or 2.")
                continue
        
        # Clean input
        moods = [m.strip() for m in user_input.split()]
        valid_moods = [m for m in moods if m in mood_table]
        invalid = [m for m in moods if m not in mood_table]

        if not valid_moods:
            print("⚠️ No valid moods entered.")
            continue

        if invalid:
            for mood in invalid:
                print(f"⚠️ Mood '{mood}' not found in table.")

        print()
        print_side_by_side(valid_moods)
        
    elif current_mode == "2":
        user_input = input("\nEnter two moods to combine: ").strip().lower()
        
        if user_input in ["exit", "q"]:
            print("Exiting mood comparison. 👋")
            break
        elif user_input == "change":
            print("\nChoose your mode:")
            print("1️⃣  Compare moods side-by-side (e.g. chill dreamy)")
            print("2️⃣  Create hybrid mood combination (e.g. chill-dreamy)")
            mode_choice = input("Choose mode (1 or 2): ").strip()
            if mode_choice in ["exit", "q"]:
                print("Exiting mood comparison. 👋")
                break
            elif mode_choice == "1":
                current_mode = "1"
                print("\n📊 COMPARISON MODE ACTIVE")
                print("Type moods separated by spaces (e.g. chill dreamy focused)")
                print("Type 'change' to switch modes, 'exit' to quit")
                continue
            elif mode_choice == "2":
                current_mode = "2"
                print("\n🔀 HYBRID MODE ACTIVE")
                print("Type one mood for single display, or two moods for hybrid (e.g. chill dreamy)")
                print("Type 'change' to switch modes, 'exit' to quit")
                continue
            else:
                print("⚠️ Please choose 1 or 2.")
                continue
        
        # Clean input
        moods = [m.strip() for m in user_input.split()]
        
        if len(moods) == 0:
            print("⚠️ Please enter at least one mood.")
            continue
        elif len(moods) == 1:
            # Single mood - show like comparison mode
            mood = moods[0]
            if mood not in mood_table:
                print(f"⚠️ Mood '{mood}' not found in table.")
                continue
            
            print(f"\n📊 SINGLE MOOD: {mood.upper()}")
            print("=" * 50)
            print_side_by_side([mood])
            continue
        elif len(moods) == 2:
            # Two moods - create hybrid
            valid_moods = [m for m in moods if m in mood_table]
            invalid = [m for m in moods if m not in mood_table]

            if len(valid_moods) != 2:
                print("⚠️ Both moods must be valid.")
                if invalid:
                    for mood in invalid:
                        print(f"⚠️ Mood '{mood}' not found in table.")
                continue

            print_hybrid_mood(valid_moods[0], valid_moods[1])
        else:
            print("⚠️ Please enter one or two moods for hybrid mode.")
            continue
