#include "EmotionalOptimizer.h"

EmotionalOptimizer::EmotionalOptimizer()
{
    initializeMoodProfiles();
}

EmotionalOptimizer::~EmotionalOptimizer()
{
}

void EmotionalOptimizer::initializeMoodProfiles()
{
    // Define emotional profiles for each mood
    moodProfiles["chill"] = {0.2f, 0.1f, 0.3f, 0.4f, 0.8f, 0.6f};
    moodProfiles["energetic"] = {0.9f, 0.6f, 0.7f, 0.9f, 0.4f, 0.9f};
    moodProfiles["suspenseful"] = {0.6f, 0.9f, 0.8f, 0.3f, 0.2f, 0.4f};
    moodProfiles["uplifting"] = {0.8f, 0.2f, 0.5f, 0.8f, 0.7f, 0.9f};
    moodProfiles["ominous"] = {0.4f, 0.8f, 0.6f, 0.2f, 0.1f, 0.2f};
    moodProfiles["romantic"] = {0.3f, 0.3f, 0.7f, 0.5f, 0.9f, 0.7f};
    moodProfiles["gritty"] = {0.7f, 0.7f, 0.6f, 0.6f, 0.3f, 0.5f};
    moodProfiles["dreamy"] = {0.2f, 0.1f, 0.8f, 0.3f, 0.8f, 0.8f};
    moodProfiles["frantic"] = {0.95f, 0.9f, 0.9f, 0.7f, 0.2f, 0.8f};
    moodProfiles["focused"] = {0.6f, 0.4f, 0.4f, 0.6f, 0.5f, 0.6f};
}

void EmotionalOptimizer::setMoodProfile(const std::string& primaryMood, const std::string& secondaryMood)
{
    auto primaryIt = moodProfiles.find(primaryMood);
    auto secondaryIt = moodProfiles.find(secondaryMood);
    
    if (primaryIt != moodProfiles.end() && secondaryIt != moodProfiles.end())
    {
        currentProfile = blendProfiles(primaryIt->second, secondaryIt->second, 0.7f);
        targetProfile = currentProfile;
    }
    else
    {
        // Default to neutral profile
        currentProfile = {0.5f, 0.5f, 0.5f, 0.5f, 0.5f, 0.5f};
        targetProfile = currentProfile;
    }
}

void EmotionalOptimizer::processMIDINotes(std::vector<MIDINote>& notes, float tempo)
{
    if (notes.empty()) return;
    
    // Apply emotional optimization
    applyEmotionalOptimization(notes, currentProfile);
    
    // Apply specific emotional adjustments
    adjustVelocityForEmotion(notes, currentProfile.energy, currentProfile.tension);
    adjustDensityForEmotion(notes, currentProfile.complexity, currentProfile.energy);
    adjustHarmonicTension(notes, currentProfile.tension, currentProfile.brightness);
    adjustGrooveForEmotion(notes, currentProfile.danceability, tempo);
}

void EmotionalOptimizer::applyEmotionalOptimization(std::vector<MIDINote>& notes, const EmotionalProfile& profile)
{
    // Apply overall emotional characteristics
    for (auto& note : notes)
    {
        // Energy affects velocity
        float velocityMultiplier = calculateVelocityMultiplier(profile.energy, profile.tension, note.velocity);
        note.velocity = juce::jlimit(1.0f, 127.0f, note.velocity * velocityMultiplier);
        
        // Warmth affects note selection (simplified)
        if (profile.warmth < 0.3f)
        {
            // Cooler tones - shift to higher registers
            note.noteNumber = juce::jlimit(0, 127, note.noteNumber + 2);
        }
        else if (profile.warmth > 0.7f)
        {
            // Warmer tones - shift to lower registers
            note.noteNumber = juce::jlimit(0, 127, note.noteNumber - 2);
        }
    }
}

void EmotionalOptimizer::adjustVelocityForEmotion(std::vector<MIDINote>& notes, float energy, float tension)
{
    for (auto& note : notes)
    {
        float baseVelocity = note.velocity;
        
        // Energy affects overall velocity
        float energyMultiplier = 0.5f + (energy * 1.0f);
        
        // Tension affects velocity variation
        float tensionVariation = (tension - 0.5f) * 0.3f;
        
        // Apply adjustments
        float newVelocity = baseVelocity * energyMultiplier + (tensionVariation * 64.0f);
        note.velocity = juce::jlimit(1.0f, 127.0f, newVelocity);
    }
}

void EmotionalOptimizer::adjustDensityForEmotion(std::vector<MIDINote>& notes, float complexity, float energy)
{
    if (notes.empty()) return;
    
    // Calculate target density based on complexity and energy
    float targetDensity = complexity * energy * 2.0f;
    float currentDensity = static_cast<float>(notes.size()) / 10.0f; // Normalize
    
    if (targetDensity > currentDensity)
    {
        // Add more notes (simplified - in real implementation, generate new notes)
        // For now, just adjust existing note durations
        for (auto& note : notes)
        {
            note.duration *= (1.0f + (targetDensity - currentDensity) * 0.1f);
        }
    }
    else if (targetDensity < currentDensity)
    {
        // Reduce density by shortening notes
        for (auto& note : notes)
        {
            note.duration *= (1.0f - (currentDensity - targetDensity) * 0.1f);
        }
    }
}

void EmotionalOptimizer::adjustHarmonicTension(std::vector<MIDINote>& notes, float tension, float brightness)
{
    // Group notes by time to analyze harmony
    std::map<float, std::vector<MIDINote*>> timeGroups;
    
    for (auto& note : notes)
    {
        float timeSlot = std::floor(note.startTime * 4.0f) / 4.0f; // Quarter note slots
        timeGroups[timeSlot].push_back(&note);
    }
    
    // Adjust harmonic tension for each time group
    for (auto& group : timeGroups)
    {
        if (group.second.size() < 2) continue;
        
        std::vector<int> chordNotes;
        for (auto* note : group.second)
        {
            chordNotes.push_back(note->noteNumber);
        }
        
        float currentTension = calculateChordTension(chordNotes);
        float targetTension = tension;
        
        if (std::abs(currentTension - targetTension) > 0.1f)
        {
            // Adjust notes to match target tension
            for (auto* note : group.second)
            {
                if (targetTension > currentTension)
                {
                    // Increase tension - add dissonance
                    if (juce::Random::getSystemRandom().nextFloat() < 0.3f)
                    {
                        note->noteNumber = juce::jlimit(0, 127, note->noteNumber + 1);
                    }
                }
                else
                {
                    // Decrease tension - make more consonant
                    if (juce::Random::getSystemRandom().nextFloat() < 0.3f)
                    {
                        note->noteNumber = juce::jlimit(0, 127, note->noteNumber - 1);
                    }
                }
            }
        }
    }
}

void EmotionalOptimizer::adjustGrooveForEmotion(std::vector<MIDINote>& notes, float danceability, float tempo)
{
    float swingAmount = calculateSwingAmount(notes, tempo);
    float targetSwing = danceability * 0.5f; // Map danceability to swing
    
    if (std::abs(swingAmount - targetSwing) > 0.1f)
    {
        // Apply swing adjustment
        for (auto& note : notes)
        {
            // Simple swing implementation - offset off-beat notes
            float beatPosition = std::fmod(note.startTime * tempo / 60.0f, 1.0f);
            if (beatPosition > 0.5f) // Off-beat
            {
                float swingOffset = (targetSwing - swingAmount) * 0.1f;
                note.startTime += swingOffset;
            }
        }
    }
}

EmotionalOptimizer::EmotionalProfile EmotionalOptimizer::blendProfiles(
    const EmotionalProfile& primary, const EmotionalProfile& secondary, float blend)
{
    EmotionalProfile result;
    result.energy = primary.energy * blend + secondary.energy * (1.0f - blend);
    result.tension = primary.tension * blend + secondary.tension * (1.0f - blend);
    result.complexity = primary.complexity * blend + secondary.complexity * (1.0f - blend);
    result.danceability = primary.danceability * blend + secondary.danceability * (1.0f - blend);
    result.warmth = primary.warmth * blend + secondary.warmth * (1.0f - blend);
    result.brightness = primary.brightness * blend + secondary.brightness * (1.0f - blend);
    return result;
}

float EmotionalOptimizer::calculateVelocityMultiplier(float energy, float tension, float baseVelocity)
{
    float energyMultiplier = 0.5f + (energy * 1.0f);
    float tensionMultiplier = 1.0f + ((tension - 0.5f) * 0.4f);
    return energyMultiplier * tensionMultiplier;
}

float EmotionalOptimizer::calculateDensityMultiplier(float complexity, float energy)
{
    return 0.5f + (complexity * energy * 1.0f);
}

float EmotionalOptimizer::calculateHarmonicTension(float tension, float brightness)
{
    return tension * (1.0f - brightness * 0.5f);
}

float EmotionalOptimizer::calculateGrooveOffset(float danceability, float tempo)
{
    return danceability * 0.1f * (120.0f / tempo); // Normalize to 120 BPM
}

bool EmotionalOptimizer::isMinorChord(int rootNote, const std::vector<int>& chordNotes)
{
    // Simplified minor chord detection
    if (chordNotes.size() < 2) return false;
    
    int root = rootNote % 12;
    for (int note : chordNotes)
    {
        int interval = (note % 12 - root + 12) % 12;
        if (interval == 3) return true; // Minor third
    }
    return false;
}

bool EmotionalOptimizer::isDissonantInterval(int note1, int note2)
{
    int interval = std::abs(note1 - note2) % 12;
    return interval == 1 || interval == 6 || interval == 11; // Semitone, tritone, major seventh
}

float EmotionalOptimizer::calculateChordTension(const std::vector<int>& chordNotes)
{
    if (chordNotes.size() < 2) return 0.0f;
    
    float totalTension = 0.0f;
    int pairCount = 0;
    
    for (size_t i = 0; i < chordNotes.size(); ++i)
    {
        for (size_t j = i + 1; j < chordNotes.size(); ++j)
        {
            if (isDissonantInterval(chordNotes[i], chordNotes[j]))
            {
                totalTension += 1.0f;
            }
            pairCount++;
        }
    }
    
    return pairCount > 0 ? totalTension / pairCount : 0.0f;
}

float EmotionalOptimizer::calculateSwingAmount(const std::vector<MIDINote>& notes, float tempo)
{
    if (notes.size() < 4) return 0.0f;
    
    float totalSwing = 0.0f;
    int swingCount = 0;
    
    for (size_t i = 0; i < notes.size() - 1; ++i)
    {
        float beatPosition1 = std::fmod(notes[i].startTime * tempo / 60.0f, 1.0f);
        float beatPosition2 = std::fmod(notes[i + 1].startTime * tempo / 60.0f, 1.0f);
        
        if (beatPosition1 < 0.5f && beatPosition2 > 0.5f) // On-beat to off-beat
        {
            float expectedOffBeat = 0.75f; // Quarter note + eighth note
            float actualOffBeat = beatPosition2;
            totalSwing += std::abs(actualOffBeat - expectedOffBeat);
            swingCount++;
        }
    }
    
    return swingCount > 0 ? totalSwing / swingCount : 0.0f;
}

float EmotionalOptimizer::calculateSyncopation(const std::vector<MIDINote>& notes, float tempo)
{
    if (notes.empty()) return 0.0f;
    
    int syncopatedNotes = 0;
    
    for (const auto& note : notes)
    {
        float beatPosition = std::fmod(note.startTime * tempo / 60.0f, 1.0f);
        if (beatPosition > 0.5f && beatPosition < 0.75f) // Off-beat
        {
            syncopatedNotes++;
        }
    }
    
    return static_cast<float>(syncopatedNotes) / notes.size();
}
