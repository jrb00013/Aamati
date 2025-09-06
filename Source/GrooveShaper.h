#pragma once

#include <JuceHeader.h>
#include <vector>
#include <map>
#include <string>

/**
 * Dynamic Groove Shaping System
 * Makes rhythm "feel" more human or natural based on mood
 */
class GrooveShaper
{
public:
    struct GrooveProfile
    {
        float humanization = 0.5f;      // 0.0 = robotic, 1.0 = very human
        float swingAmount = 0.0f;        // 0.0 = straight, 1.0 = maximum swing
        float accentPattern = 0.5f;      // 0.0 = weak, 1.0 = strong accents
        float microTiming = 0.5f;        // 0.0 = quantized, 1.0 = loose timing
        float velocityVariation = 0.5f;  // 0.0 = uniform, 1.0 = varied
        float ghostNotes = 0.0f;         // 0.0 = no ghosts, 1.0 = many ghosts
    };
    
    struct TimingVariation
    {
        float early = 0.0f;    // Notes that come early (negative offset)
        float late = 0.0f;     // Notes that come late (positive offset)
        float onTime = 1.0f;   // Notes that are on time
    };
    
    GrooveShaper();
    ~GrooveShaper();
    
    // Main processing functions
    void setGrooveProfile(const std::string& mood, float intensity = 1.0f);
    void processGroove(std::vector<juce::MidiMessage>& midiMessages, float tempo, float timeSignature = 4.0f);
    void applyHumanization(std::vector<juce::MidiMessage>& midiMessages, const GrooveProfile& profile);
    
    // Specific groove shaping functions
    void applySwing(std::vector<juce::MidiMessage>& midiMessages, float swingAmount, float tempo);
    void applyMicroTiming(std::vector<juce::MidiMessage>& midiMessages, float microTiming, float tempo);
    void applyAccentPattern(std::vector<juce::MidiMessage>& midiMessages, float accentPattern, float timeSignature);
    void applyVelocityVariation(std::vector<juce::MidiMessage>& midiMessages, float variation);
    void addGhostNotes(std::vector<juce::MidiMessage>& midiMessages, float ghostAmount, float tempo);
    
    // Real-time parameters
    void setGrooveIntensity(float intensity) { grooveIntensity = juce::jlimit(0.0f, 1.0f, intensity); }
    void setHumanizationAmount(float amount) { humanizationAmount = juce::jlimit(0.0f, 1.0f, amount); }
    void setSwingAmount(float amount) { swingAmount = juce::jlimit(0.0f, 1.0f, amount); }
    
    // Preset management
    void loadGroovePreset(const std::string& presetName);
    void saveGroovePreset(const std::string& presetName, const GrooveProfile& profile);
    
private:
    // Groove profiles for different moods
    std::map<std::string, GrooveProfile> grooveProfiles;
    GrooveProfile currentProfile;
    
    // Processing parameters
    float grooveIntensity = 0.5f;
    float humanizationAmount = 0.5f;
    float swingAmount = 0.0f;
    
    // Internal state
    juce::Random random;
    std::map<int, float> lastNoteTimes; // Track last note time per channel
    std::map<int, int> noteCounts;      // Track note counts per channel
    
    // Internal processing functions
    void initializeGrooveProfiles();
    float calculateSwingOffset(float beatPosition, float swingAmount);
    float calculateMicroTimingOffset(float baseOffset, float microTiming);
    float calculateAccentMultiplier(float beatPosition, float accentPattern, float timeSignature);
    float calculateVelocityVariation(float baseVelocity, float variation);
    
    // Rhythm analysis
    float getBeatPosition(double timeInSeconds, float tempo, float timeSignature);
    bool isOnBeat(float beatPosition, float tolerance = 0.1f);
    bool isOffBeat(float beatPosition, float tolerance = 0.1f);
    bool isStrongBeat(float beatPosition, float timeSignature);
    
    // Humanization algorithms
    float generateHumanTimingOffset(float baseOffset, float humanization);
    float generateVelocityVariation(float baseVelocity, float variation);
    bool shouldAddGhostNote(float beatPosition, float ghostAmount);
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(GrooveShaper)
};
