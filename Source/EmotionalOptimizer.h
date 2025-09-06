#pragma once

#include <JuceHeader.h>
#include <vector>
#include <map>
#include <string>

/**
 * Emotional Optimization System
 * Adjusts MIDI to make the listener "feel" the intended emotion
 */
class EmotionalOptimizer
{
public:
    struct EmotionalProfile
    {
        float energy = 0.5f;
        float tension = 0.5f;
        float complexity = 0.5f;
        float danceability = 0.5f;
        float warmth = 0.5f;
        float brightness = 0.5f;
    };
    
    struct MIDINote
    {
        int noteNumber = 60;
        float velocity = 64.0f;
        float startTime = 0.0f;
        float duration = 1.0f;
        int channel = 0;
    };
    
    EmotionalOptimizer();
    ~EmotionalOptimizer();
    
    // Main processing functions
    void setMoodProfile(const std::string& primaryMood, const std::string& secondaryMood);
    void processMIDINotes(std::vector<MIDINote>& notes, float tempo);
    void applyEmotionalOptimization(std::vector<MIDINote>& notes, const EmotionalProfile& profile);
    
    // Specific emotional adjustments
    void adjustVelocityForEmotion(std::vector<MIDINote>& notes, float energy, float tension);
    void adjustDensityForEmotion(std::vector<MIDINote>& notes, float complexity, float energy);
    void adjustHarmonicTension(std::vector<MIDINote>& notes, float tension, float brightness);
    void adjustGrooveForEmotion(std::vector<MIDINote>& notes, float danceability, float tempo);
    
    // Preset management
    void loadEmotionalPreset(const std::string& presetName);
    void saveEmotionalPreset(const std::string& presetName, const EmotionalProfile& profile);
    
    // Real-time parameters
    void setEmotionalSensitivity(float sensitivity) { emotionalSensitivity = juce::jlimit(0.0f, 1.0f, sensitivity); }
    void setPresetBlend(float blend) { presetBlend = juce::jlimit(0.0f, 1.0f, blend); }
    
private:
    // Mood profiles
    std::map<std::string, EmotionalProfile> moodProfiles;
    EmotionalProfile currentProfile;
    EmotionalProfile targetProfile;
    
    // Processing parameters
    float emotionalSensitivity = 0.5f;
    float presetBlend = 0.0f;
    
    // Internal processing
    void initializeMoodProfiles();
    EmotionalProfile blendProfiles(const EmotionalProfile& primary, const EmotionalProfile& secondary, float blend);
    float calculateVelocityMultiplier(float energy, float tension, float baseVelocity);
    float calculateDensityMultiplier(float complexity, float energy);
    float calculateHarmonicTension(float tension, float brightness);
    float calculateGrooveOffset(float danceability, float tempo);
    
    // Harmonic analysis
    bool isMinorChord(int rootNote, const std::vector<int>& chordNotes);
    bool isDissonantInterval(int note1, int note2);
    float calculateChordTension(const std::vector<int>& chordNotes);
    
    // Rhythm analysis
    float calculateSwingAmount(const std::vector<MIDINote>& notes, float tempo);
    float calculateSyncopation(const std::vector<MIDINote>& notes, float tempo);
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(EmotionalOptimizer)
};
