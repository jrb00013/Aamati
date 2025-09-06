#pragma once

#include <JuceHeader.h>
#include <vector>
#include <map>
#include <string>
#include <memory>

/**
 * AI-Driven Real-time MIDI Generation System
 * Generates MIDI content based on mood analysis and musical context
 */
class AIMidiGenerator
{
public:
    struct GenerationContext
    {
        std::string primaryMood;
        std::string secondaryMood;
        float tempo = 120.0f;
        int key = 0; // 0 = C, 1 = C#, etc.
        std::string scale = "major"; // major, minor, dorian, etc.
        float energy = 0.5f;
        float complexity = 0.5f;
        int timeSignature = 4;
        double currentTime = 0.0;
    };
    
    struct GeneratedPattern
    {
        std::vector<juce::MidiMessage> messages;
        double duration = 1.0;
        float confidence = 0.0f;
        std::string patternType = "melody";
    };
    
    struct InstrumentPreset
    {
        int program = 0; // MIDI program number
        std::string name = "Piano";
        float volume = 0.8f;
        float pan = 0.0f;
        std::map<std::string, float> parameters;
    };
    
    AIMidiGenerator();
    ~AIMidiGenerator();
    
    // Main generation functions
    void setGenerationContext(const GenerationContext& context);
    GeneratedPattern generateMelody(double duration, int channel = 0);
    GeneratedPattern generateHarmony(double duration, int channel = 1);
    GeneratedPattern generateRhythm(double duration, int channel = 9); // Drum channel
    GeneratedPattern generateFill(double duration, int channel = 9);
    
    // Real-time generation
    void generateRealTimeContent(std::vector<juce::MidiMessage>& output, double currentTime, double lookAhead = 1.0);
    void updateContext(const GenerationContext& context);
    
    // Pattern generation based on mood
    GeneratedPattern generateMoodPattern(const std::string& mood, double duration, const std::string& patternType);
    GeneratedPattern generateTransitionPattern(const std::string& fromMood, const std::string& toMood, double duration);
    
    // Instrumentation guidance
    void setInstrumentPreset(int channel, const InstrumentPreset& preset);
    InstrumentPreset getInstrumentPreset(int channel) const;
    std::vector<InstrumentPreset> getRecommendedPresets(const std::string& mood) const;
    
    // Real-time parameters
    void setGenerationIntensity(float intensity) { generationIntensity = juce::jlimit(0.0f, 1.0f, intensity); }
    void setCreativityLevel(float creativity) { creativityLevel = juce::jlimit(0.0f, 1.0f, creativity); }
    void setComplexityLevel(float complexity) { complexityLevel = juce::jlimit(0.0f, 1.0f, complexity); }
    
    // Pattern management
    void loadPatternLibrary(const std::string& libraryPath);
    void savePatternLibrary(const std::string& libraryPath);
    void addCustomPattern(const std::string& name, const GeneratedPattern& pattern);
    
private:
    // Generation context
    GenerationContext currentContext;
    std::map<int, InstrumentPreset> instrumentPresets;
    
    // Generation parameters
    float generationIntensity = 0.5f;
    float creativityLevel = 0.5f;
    float complexityLevel = 0.5f;
    
    // Pattern libraries
    std::map<std::string, std::vector<GeneratedPattern>> patternLibraries;
    std::map<std::string, GeneratedPattern> customPatterns;
    
    // Random number generation
    juce::Random random;
    
    // Internal generation functions
    void initializePatternLibraries();
    void initializeInstrumentPresets();
    
    // Melody generation
    std::vector<int> generateMelodyNotes(int length, int key, const std::string& scale);
    std::vector<double> generateMelodyRhythm(int length, float tempo);
    std::vector<int> generateMelodyVelocities(int length, float energy);
    
    // Harmony generation
    std::vector<std::vector<int>> generateChordProgression(int length, int key, const std::string& scale);
    std::vector<int> generateChordVoicing(const std::vector<int>& chord, int key);
    
    // Rhythm generation
    std::vector<double> generateRhythmPattern(int length, float complexity, const std::string& mood);
    std::vector<int> generateDrumPattern(int length, float energy, const std::string& mood);
    
    // Fill generation
    GeneratedPattern generateDrumFill(double duration, float energy);
    GeneratedPattern generateMelodicFill(double duration, int key, const std::string& scale);
    
    // Mood-specific generation
    GeneratedPattern generateChillPattern(double duration);
    GeneratedPattern generateEnergeticPattern(double duration);
    GeneratedPattern generateSuspensefulPattern(double duration);
    GeneratedPattern generateUpliftingPattern(double duration);
    GeneratedPattern generateOminousPattern(double duration);
    GeneratedPattern generateRomanticPattern(double duration);
    GeneratedPattern generateGrittyPattern(double duration);
    GeneratedPattern generateDreamyPattern(double duration);
    GeneratedPattern generateFranticPattern(double duration);
    GeneratedPattern generateFocusedPattern(double duration);
    
    // Musical theory helpers
    std::vector<int> getScaleNotes(int key, const std::string& scale);
    std::vector<int> getChordNotes(int root, const std::string& chordType);
    bool isInScale(int note, int key, const std::string& scale);
    int getNoteInKey(int note, int key);
    
    // Pattern analysis
    float analyzePatternComplexity(const GeneratedPattern& pattern);
    float analyzePatternEnergy(const GeneratedPattern& pattern);
    std::string classifyPatternType(const GeneratedPattern& pattern);
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(AIMidiGenerator)
};
