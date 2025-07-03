# estimate_features.py

import os
import pretty_midi
import pandas as pd
import numpy as np
import datetime
import scipy.stats
import scipy.signal
import json
from joblib import load

def estimate_dynamic_intensity(vel, dr, vs):
    # vel = mean velocity, dr = dynamic range, vs = velocity std dev

    if vel < 30:
        if dr < 20:
            return 0  # ppp
        elif dr < 30:
            return 1  # pp
        else:
            return 2  # p
    elif vel < 50:
        if dr < 25:
            return 2  # p
        elif dr < 40:
            return 3  # mp
        else:
            return 4  # mf
    elif vel < 70:
        if dr < 30:
            return 3  # mp
        elif dr < 50:
            return 4  # mf
        else:
            return 5  # f
    elif vel < 90:
        if dr < 40:
            return 5  # f
        elif dr < 60:
            return 6  # ff
        else:
            return 7  # fff
    else:  # vel >= 90
        if dr < 50:
            return 6  # ff
        elif dr < 70:
            return 7  # fff
        else:
            return 8  # ffff
        
# def estimate_fill_activity(pitch_range, onset_entropy):
#     # Exponents based on music theory rationale
#     a = 0.8  # pitch range influence
#     b = 0.3  # onset entropy influence

#     # Scaling factor ensures fill_score peaks around 10 at upper bounds
#     scaling_factor = (90 ** a) * (3 ** b) / 10  # scale so max output ~10

#     # Compute raw fill activity score
#     fill_score = ((pitch_range ** a) * (onset_entropy ** b)) / scaling_factor

#     # Clamp to [0, 9] discrete levels
#     return min(int(round(fill_score)), 9)
        
def estimate_fx_character(features):

    distortion_proxy = features['dynamic_range'] * features['density']
    tone_brightness = features['pitch_range'] / (features['mean_note_length'] + 1e-6)  # avoid div zero
    harmonic_complexity = features['syncopation'] * features['swing']
    velocity_variability = features['velocity_std']
    onset_entropy = features['onset_entropy']

    if distortion_proxy > 150 and velocity_variability > 20:
        return 6  # 'distorted, mono, rough'
    elif harmonic_complexity > 0.05 and onset_entropy > 2.5:
        return 8  # 'glitchy, stuttered, noisy'
    elif tone_brightness > 40 and onset_entropy < 1.2:
        return 1  # 'dry, punchy, sharp'
    elif distortion_proxy > 80 and tone_brightness < 15:
        return 4  # 'saturated, low-end heavy'
    elif velocity_variability < 5 and harmonic_complexity < 0.01:
        return 9  # 'clean, subtle, precise'
    elif onset_entropy > 3.0 and velocity_variability > 15:
        return 7  # 'reverb-heavy, washed-out'
    elif harmonic_complexity > 0.03 and distortion_proxy > 50:
        return 0  # 'wet, wide, airy'
    else:
        return 5  # 'warm, lush, resonant'
    
def estimate_timing_feel(swing, syncopation, onset_entropy):
  
    # Estimate timing feel score (0=tight, 1=mid, 2=loose, 3=random)
    # Initialize scores for each
    scores = {'tight': 0, 'mid': 0, 'loose': 0, 'random': 0}

    # Evaluate 'tight' characteristics: low swing & low syncopation
    if swing < 0.05 and syncopation < 0.015:
        scores['tight'] += 2
    elif swing < 0.1 and syncopation < 0.03:
        scores['tight'] += 1

    # Evaluate 'loose' characteristics: higher swing and moderate syncopation
    if swing > 0.08 and syncopation > 0.015:
        scores['loose'] += 2
    elif swing > 0.05 and syncopation > 0.01:
        scores['loose'] += 1

    # Evaluate 'random' characteristics: high syncopation and high onset entropy
    if syncopation > 0.045 and onset_entropy > 2.0:
        scores['random'] += 3
    elif syncopation > 0.035 and onset_entropy > 1.8:
        scores['random'] += 1

    # Default to 'mid' if none strong
    # Increase 'mid' score when values are moderate
    if 0.03 <= swing <= 0.08 and 0.01 <= syncopation <= 0.04:
        scores['mid'] += 2
    else:
        scores['mid'] += 1

    # Pick the category with highest score
    best_category = max(scores, key=scores.get)

    # Map to numeric code
    mapping = {'tight': 0, 'mid': 1, 'loose': 2, 'random': 3}
    return mapping[best_category]