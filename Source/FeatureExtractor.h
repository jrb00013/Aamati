#pragma once
#include <vector>
#include <optional>
#include <JuceHeader.h>

struct GrooveFeatures {
    double tempo;
    double swing;
    double density;
    double dynamicRange;
    double energy;
    double velocityMean;
    double velocityStd;
    double pitchMean;
    double pitchRange;
    double avgPolyphony;
    double syncopation;
    double onsetEntropy;
};

class FeatureExtractor {
public:
    FeatureExtractor();
    ~FeatureExtractor();
    
    // Real-time audio feature extraction
    std::optional<GrooveFeatures> extractFeaturesFromAudio(const juce::AudioBuffer<float>& buffer, double sampleRate);
    
    // MIDI file feature extraction (for training)
    GrooveFeatures extractFeaturesFromMidi(const std::string& midiFilePath);
    
    // Reset internal state for new analysis
    void reset();

private:
    // Internal state for real-time analysis
    std::vector<float> audioHistory;
    std::vector<float> velocityHistory;
    std::vector<float> pitchHistory;
    double lastAnalysisTime;
    static constexpr size_t MAX_HISTORY_SIZE = 44100 * 10; // 10 seconds at 44.1kHz
    
    // Helper methods
    double calculateTempo(const std::vector<float>& audioData, double sampleRate);
    double calculateSwing(const std::vector<float>& audioData, double sampleRate);
    double calculateDensity(const std::vector<float>& audioData, double sampleRate);
    double calculateDynamicRange(const std::vector<float>& audioData);
    double calculateEnergy(const std::vector<float>& audioData);
    double calculateVelocityMean(const std::vector<float>& audioData);
    double calculateVelocityStd(const std::vector<float>& audioData);
    double calculatePitchMean(const std::vector<float>& audioData);
    double calculatePitchRange(const std::vector<float>& audioData);
    double calculateAvgPolyphony(const std::vector<float>& audioData, double sampleRate);
    double calculateSyncopation(const std::vector<float>& audioData, double sampleRate);
    double calculateOnsetEntropy(const std::vector<float>& audioData, double sampleRate);
};