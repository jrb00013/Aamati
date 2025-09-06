#include "FeatureExtractor.h"
#include "MidiFile.h"
#include "Options.h"
#include <cmath>
#include <vector>
#include <numeric>
#include <algorithm>
#include <JuceHeader.h>

using namespace std;
using namespace smf;

FeatureExtractor::FeatureExtractor() 
    : lastAnalysisTime(0.0)
{
    audioHistory.reserve(MAX_HISTORY_SIZE);
    velocityHistory.reserve(MAX_HISTORY_SIZE);
    pitchHistory.reserve(MAX_HISTORY_SIZE);
}

FeatureExtractor::~FeatureExtractor() {}

void FeatureExtractor::reset()
{
    audioHistory.clear();
    velocityHistory.clear();
    pitchHistory.clear();
    lastAnalysisTime = 0.0;
}

std::optional<GrooveFeatures> FeatureExtractor::extractFeaturesFromAudio(const juce::AudioBuffer<float>& buffer, double sampleRate)
{
    // Add current buffer to history
    for (int channel = 0; channel < buffer.getNumChannels(); ++channel)
    {
        for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
        {
            float sampleValue = buffer.getSample(channel, sample);
            audioHistory.push_back(sampleValue);
            
            // Calculate velocity (amplitude) for this sample
            float velocity = std::abs(sampleValue);
            velocityHistory.push_back(velocity);
            
            // For pitch, we'll use a simple approximation based on sample value
            // In a real implementation, you'd use pitch detection algorithms
            float pitch = (sampleValue + 1.0f) * 64.0f; // Map to 0-128 range
            pitchHistory.push_back(pitch);
        }
    }
    
    // Keep history size manageable
    if (audioHistory.size() > MAX_HISTORY_SIZE)
    {
        size_t excess = audioHistory.size() - MAX_HISTORY_SIZE;
        audioHistory.erase(audioHistory.begin(), audioHistory.begin() + excess);
        velocityHistory.erase(velocityHistory.begin(), velocityHistory.begin() + excess);
        pitchHistory.erase(pitchHistory.begin(), pitchHistory.begin() + excess);
    }
    
    // Only analyze if we have enough data (at least 1 second)
    if (audioHistory.size() < static_cast<size_t>(sampleRate))
    {
        return std::nullopt;
    }
    
    // Calculate features
    GrooveFeatures features;
    features.tempo = calculateTempo(audioHistory, sampleRate);
    features.swing = calculateSwing(audioHistory, sampleRate);
    features.density = calculateDensity(audioHistory, sampleRate);
    features.dynamicRange = calculateDynamicRange(audioHistory);
    features.energy = calculateEnergy(audioHistory);
    features.velocityMean = calculateVelocityMean(velocityHistory);
    features.velocityStd = calculateVelocityStd(velocityHistory);
    features.pitchMean = calculatePitchMean(pitchHistory);
    features.pitchRange = calculatePitchRange(pitchHistory);
    features.avgPolyphony = calculateAvgPolyphony(audioHistory, sampleRate);
    features.syncopation = calculateSyncopation(audioHistory, sampleRate);
    features.onsetEntropy = calculateOnsetEntropy(audioHistory, sampleRate);
    
    return features;
}

GrooveFeatures FeatureExtractor::extractFeaturesFromMidi(const string& midiPath) {
    MidiFile midi;
    if (!midi.read(midiPath)) return {120.0f, 0.0f, 0.0f, 0.0f, 0.0f}; // fallback

    midi.doTimeAnalysis();
    midi.linkNotePairs();

    vector<float> noteTimes;
    vector<int> velocities;
    float endTime = 0.0f;

    for (int t = 0; t < midi.getTrackCount(); ++t) {
        for (int e = 0; e < midi[t].size(); ++e) {
            MidiEvent& mev = midi[t][e];
            if (!mev.isNoteOn()) continue;
            if (!mev.isDrumNote()) continue;

            float time = mev.seconds;
            noteTimes.push_back(time);
            velocities.push_back(mev.getVelocity());

            if (time > endTime) endTime = time;
        }
    }

    if (noteTimes.size() < 2 || endTime <= 0.0f)
        return {120.0f, 0.0f, 0.0f, 0.0f, 0.0f};

    float density = noteTimes.size() / endTime;

    // Swing: Deviation from strict 8th note grid (assume 120 BPM 8th notes = 0.25s apart)
    float swingSum = 0.0f;
    for (auto& time : noteTimes) {
        float quant = round(time * 4.0f) / 4.0f; // nearest 0.25
        swingSum += fabs(time - quant);
    }
    float swing = swingSum / noteTimes.size();

    int maxVel = *max_element(velocities.begin(), velocities.end());
    int minVel = *min_element(velocities.begin(), velocities.end());
    float dynamicRange = static_cast<float>(maxVel - minVel);
    float meanVel = accumulate(velocities.begin(), velocities.end(), 0.0f) / velocities.size();

    float energy = (density * 0.5f) + (meanVel / 127.0f * 0.5f);

    float tempo = 120.0f;
    if (midi.getTicksPerQuarterNote() > 0) {
        tempo = 60.0f / midi.getTimeInSeconds(midi.getTicksPerQuarterNote());
    }

    return {tempo, swing, density, dynamicRange, energy};
}
