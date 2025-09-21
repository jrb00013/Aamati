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

// Enhanced audio analysis implementations
double FeatureExtractor::calculateTempo(const std::vector<float>& audioData, double sampleRate)
{
    if (audioData.size() < static_cast<size_t>(sampleRate)) return 120.0;
    
    // Use autocorrelation for tempo detection
    std::vector<float> autocorrelation = calculateAutocorrelation(audioData);
    
    // Find peaks in autocorrelation
    std::vector<int> peakIndices = findPeaks(autocorrelation);
    
    if (peakIndices.empty()) return 120.0;
    
    // Calculate tempo from peak intervals
    std::vector<double> tempos;
    for (size_t i = 0; i < peakIndices.size() - 1; ++i)
    {
        double interval = static_cast<double>(peakIndices[i+1] - peakIndices[i]) / sampleRate;
        if (interval > 0.1 && interval < 2.0) // Reasonable tempo range
        {
            tempos.push_back(60.0 / interval);
        }
    }
    
    if (tempos.empty()) return 120.0;
    
    // Return median tempo for stability
    std::sort(tempos.begin(), tempos.end());
    return tempos[tempos.size() / 2];
}

std::vector<float> FeatureExtractor::calculateAutocorrelation(const std::vector<float>& audioData)
{
    size_t maxLag = std::min(audioData.size() / 2, static_cast<size_t>(44100)); // Max 1 second
    std::vector<float> autocorrelation(maxLag, 0.0f);
    
    for (size_t lag = 0; lag < maxLag; ++lag)
    {
        float sum = 0.0f;
        size_t count = 0;
        
        for (size_t i = 0; i < audioData.size() - lag; ++i)
        {
            sum += audioData[i] * audioData[i + lag];
            count++;
        }
        
        if (count > 0)
        {
            autocorrelation[lag] = sum / count;
        }
    }
    
    return autocorrelation;
}

std::vector<int> FeatureExtractor::findPeaks(const std::vector<float>& data)
{
    std::vector<int> peaks;
    float threshold = 0.1f;
    
    for (size_t i = 1; i < data.size() - 1; ++i)
    {
        if (data[i] > data[i-1] && data[i] > data[i+1] && data[i] > threshold)
        {
            peaks.push_back(static_cast<int>(i));
        }
    }
    
    return peaks;
}

double FeatureExtractor::calculateSwing(const std::vector<float>& audioData, double sampleRate)
{
    if (audioData.size() < static_cast<size_t>(sampleRate)) return 0.0;
    
    // Detect onsets for swing analysis
    std::vector<float> onsets = detectOnsets(audioData, sampleRate);
    
    if (onsets.size() < 4) return 0.0;
    
    // Analyze timing patterns for swing
    double swingAmount = 0.0;
    int swingCount = 0;
    
    for (size_t i = 0; i < onsets.size() - 2; ++i)
    {
        double interval1 = onsets[i+1] - onsets[i];
        double interval2 = onsets[i+2] - onsets[i+1];
        
        // Look for swing patterns (long-short-long)
        if (interval1 > interval2 * 1.5) // First interval significantly longer
        {
            double expectedSwing = interval1 * 0.67; // Expected swing ratio
            double actualRatio = interval2 / interval1;
            swingAmount += std::abs(actualRatio - 0.67);
            swingCount++;
        }
    }
    
    return swingCount > 0 ? swingAmount / swingCount : 0.0;
}

std::vector<float> FeatureExtractor::detectOnsets(const std::vector<float>& audioData, double sampleRate)
{
    std::vector<float> onsets;
    
    // Simple onset detection using spectral flux
    float threshold = 0.1f;
    float prevEnergy = 0.0f;
    
    for (size_t i = 1; i < audioData.size(); ++i)
    {
        float currentEnergy = std::abs(audioData[i]);
        
        // Detect sudden increase in energy
        if (currentEnergy > prevEnergy * 1.5f && currentEnergy > threshold)
        {
            onsets.push_back(static_cast<float>(i) / static_cast<float>(sampleRate));
        }
        
        prevEnergy = currentEnergy;
    }
    
    return onsets;
}

double FeatureExtractor::calculateDensity(const std::vector<float>& audioData, double sampleRate)
{
    // Calculate density as number of significant events per second
    int significantEvents = 0;
    float threshold = 0.1f;
    
    for (float sample : audioData)
    {
        if (std::abs(sample) > threshold)
        {
            significantEvents++;
        }
    }
    
    double duration = audioData.size() / sampleRate;
    return duration > 0 ? significantEvents / duration : 0.0;
}

double FeatureExtractor::calculateDynamicRange(const std::vector<float>& audioData)
{
    if (audioData.empty()) return 0.0;
    
    auto minmax = std::minmax_element(audioData.begin(), audioData.end());
    return *minmax.second - *minmax.first;
}

double FeatureExtractor::calculateEnergy(const std::vector<float>& audioData)
{
    if (audioData.empty()) return 0.0;
    
    double sum = 0.0;
    for (float sample : audioData)
    {
        sum += sample * sample;
    }
    
    return std::sqrt(sum / audioData.size());
}

double FeatureExtractor::calculateVelocityMean(const std::vector<float>& velocityData)
{
    if (velocityData.empty()) return 0.0;
    
    double sum = 0.0;
    for (float velocity : velocityData)
    {
        sum += velocity;
    }
    
    return sum / velocityData.size();
}

double FeatureExtractor::calculateVelocityStd(const std::vector<float>& velocityData)
{
    if (velocityData.size() < 2) return 0.0;
    
    double mean = calculateVelocityMean(velocityData);
    double sumSquaredDiffs = 0.0;
    
    for (float velocity : velocityData)
    {
        double diff = velocity - mean;
        sumSquaredDiffs += diff * diff;
    }
    
    return std::sqrt(sumSquaredDiffs / (velocityData.size() - 1));
}

double FeatureExtractor::calculatePitchMean(const std::vector<float>& pitchData)
{
    if (pitchData.empty()) return 0.0;
    
    double sum = 0.0;
    for (float pitch : pitchData)
    {
        sum += pitch;
    }
    
    return sum / pitchData.size();
}

double FeatureExtractor::calculatePitchRange(const std::vector<float>& pitchData)
{
    if (pitchData.empty()) return 0.0;
    
    auto minmax = std::minmax_element(pitchData.begin(), pitchData.end());
    return *minmax.second - *minmax.first;
}

double FeatureExtractor::calculateAvgPolyphony(const std::vector<float>& audioData, double sampleRate)
{
    // Simplified polyphony calculation
    // In practice, this would involve more sophisticated analysis
    int activeVoices = 0;
    float threshold = 0.1f;
    
    for (float sample : audioData)
    {
        if (std::abs(sample) > threshold)
        {
            activeVoices++;
        }
    }
    
    return static_cast<double>(activeVoices) / audioData.size();
}

double FeatureExtractor::calculateSyncopation(const std::vector<float>& audioData, double sampleRate)
{
    // Simplified syncopation calculation
    // This is a placeholder - real implementation would be much more complex
    double syncopation = 0.0;
    int count = 0;
    
    for (size_t i = 1; i < audioData.size() - 1; ++i)
    {
        if (std::abs(audioData[i]) > 0.1f)
        {
            // Check for off-beat emphasis
            double time = i / sampleRate;
            double beatPosition = std::fmod(time * 2.0, 1.0); // Assuming 120 BPM
            if (beatPosition > 0.25 && beatPosition < 0.75) // Off-beat
            {
                syncopation += std::abs(audioData[i]);
                count++;
            }
        }
    }
    
    return count > 0 ? syncopation / count : 0.0;
}

double FeatureExtractor::calculateOnsetEntropy(const std::vector<float>& audioData, double sampleRate)
{
    // Simplified onset entropy calculation
    // This is a placeholder - real implementation would use proper onset detection
    std::vector<float> onsets;
    float threshold = 0.1f;
    
    for (size_t i = 1; i < audioData.size() - 1; ++i)
    {
        if (audioData[i] > audioData[i-1] && audioData[i] > audioData[i+1] && audioData[i] > threshold)
        {
            onsets.push_back(static_cast<float>(i) / static_cast<float>(sampleRate));
        }
    }
    
    if (onsets.size() < 2) return 0.0;
    
    // Calculate intervals between onsets
    std::vector<float> intervals;
    for (size_t i = 1; i < onsets.size(); ++i)
    {
        intervals.push_back(onsets[i] - onsets[i-1]);
    }
    
    // Calculate entropy of intervals
    // This is a simplified version
    double entropy = 0.0;
    for (float interval : intervals)
    {
        if (interval > 0.0)
        {
            double probability = interval / (onsets.back() - onsets.front());
            if (probability > 0.0)
            {
                entropy -= probability * std::log2(probability);
            }
        }
    }
    
    return entropy;
}

