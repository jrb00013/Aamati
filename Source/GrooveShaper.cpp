#include "GrooveShaper.h"

GrooveShaper::GrooveShaper() : random(juce::Time::currentTimeMillis())
{
    initializeGrooveProfiles();
}

GrooveShaper::~GrooveShaper()
{
}

void GrooveShaper::initializeGrooveProfiles()
{
    // Define groove profiles for different moods
    grooveProfiles["chill"] = {0.8f, 0.3f, 0.2f, 0.7f, 0.3f, 0.1f};
    grooveProfiles["energetic"] = {0.6f, 0.1f, 0.9f, 0.3f, 0.8f, 0.2f};
    grooveProfiles["suspenseful"] = {0.4f, 0.0f, 0.7f, 0.2f, 0.6f, 0.0f};
    grooveProfiles["uplifting"] = {0.7f, 0.2f, 0.8f, 0.5f, 0.6f, 0.1f};
    grooveProfiles["ominous"] = {0.3f, 0.0f, 0.5f, 0.1f, 0.4f, 0.0f};
    grooveProfiles["romantic"] = {0.9f, 0.4f, 0.3f, 0.8f, 0.4f, 0.2f};
    grooveProfiles["gritty"] = {0.5f, 0.1f, 0.8f, 0.4f, 0.7f, 0.3f};
    grooveProfiles["dreamy"] = {0.8f, 0.5f, 0.2f, 0.9f, 0.3f, 0.3f};
    grooveProfiles["frantic"] = {0.3f, 0.0f, 0.9f, 0.1f, 0.9f, 0.1f};
    grooveProfiles["focused"] = {0.4f, 0.0f, 0.6f, 0.2f, 0.5f, 0.0f};
}

void GrooveShaper::setGrooveProfile(const std::string& mood, float intensity)
{
    auto it = grooveProfiles.find(mood);
    if (it != grooveProfiles.end())
    {
        currentProfile = it->second;
        
        // Apply intensity scaling
        currentProfile.humanization *= intensity;
        currentProfile.swingAmount *= intensity;
        currentProfile.accentPattern *= intensity;
        currentProfile.microTiming *= intensity;
        currentProfile.velocityVariation *= intensity;
        currentProfile.ghostNotes *= intensity;
        
        // Clamp values
        currentProfile.humanization = juce::jlimit(0.0f, 1.0f, currentProfile.humanization);
        currentProfile.swingAmount = juce::jlimit(0.0f, 1.0f, currentProfile.swingAmount);
        currentProfile.accentPattern = juce::jlimit(0.0f, 1.0f, currentProfile.accentPattern);
        currentProfile.microTiming = juce::jlimit(0.0f, 1.0f, currentProfile.microTiming);
        currentProfile.velocityVariation = juce::jlimit(0.0f, 1.0f, currentProfile.velocityVariation);
        currentProfile.ghostNotes = juce::jlimit(0.0f, 1.0f, currentProfile.ghostNotes);
    }
}

void GrooveShaper::processGroove(std::vector<juce::MidiMessage>& midiMessages, float tempo, float timeSignature)
{
    if (midiMessages.empty()) return;
    
    // Apply all groove shaping techniques
    applySwing(midiMessages, currentProfile.swingAmount, tempo);
    applyMicroTiming(midiMessages, currentProfile.microTiming, tempo);
    applyAccentPattern(midiMessages, currentProfile.accentPattern, timeSignature);
    applyVelocityVariation(midiMessages, currentProfile.velocityVariation);
    addGhostNotes(midiMessages, currentProfile.ghostNotes, tempo);
}

void GrooveShaper::applySwing(std::vector<juce::MidiMessage>& midiMessages, float swingAmount, float tempo)
{
    if (swingAmount <= 0.0f) return;
    
    for (auto& message : midiMessages)
    {
        if (message.isNoteOn() || message.isNoteOff())
        {
            double timeInSeconds = message.getTimeStamp();
            float beatPosition = getBeatPosition(timeInSeconds, tempo, 4.0f);
            
            // Apply swing to off-beat notes
            if (isOffBeat(beatPosition))
            {
                float swingOffset = calculateSwingOffset(beatPosition, swingAmount);
                double newTime = timeInSeconds + (swingOffset / tempo) * 60.0f;
                message.setTimeStamp(newTime);
            }
        }
    }
}

void GrooveShaper::applyMicroTiming(std::vector<juce::MidiMessage>& midiMessages, float microTiming, float tempo)
{
    if (microTiming <= 0.0f) return;
    
    for (auto& message : midiMessages)
    {
        if (message.isNoteOn() || message.isNoteOff())
        {
            double timeInSeconds = message.getTimeStamp();
            float baseOffset = 0.0f;
            
            // Generate human-like timing variation
            float timingOffset = calculateMicroTimingOffset(baseOffset, microTiming);
            double newTime = timeInSeconds + (timingOffset / tempo) * 60.0f;
            message.setTimeStamp(newTime);
        }
    }
}

void GrooveShaper::applyAccentPattern(std::vector<juce::MidiMessage>& midiMessages, float accentPattern, float timeSignature)
{
    if (accentPattern <= 0.0f) return;
    
    for (auto& message : midiMessages)
    {
        if (message.isNoteOn())
        {
            double timeInSeconds = message.getTimeStamp();
            float beatPosition = getBeatPosition(timeInSeconds, 120.0f, timeSignature); // Use 120 BPM for beat calculation
            
            float accentMultiplier = calculateAccentMultiplier(beatPosition, accentPattern, timeSignature);
            int newVelocity = juce::jlimit(1, 127, static_cast<int>(message.getVelocity() * accentMultiplier));
            message = juce::MidiMessage::noteOn(message.getChannel(), message.getNoteNumber(), static_cast<juce::uint8>(newVelocity));
        }
    }
}

void GrooveShaper::applyVelocityVariation(std::vector<juce::MidiMessage>& midiMessages, float variation)
{
    if (variation <= 0.0f) return;
    
    for (auto& message : midiMessages)
    {
        if (message.isNoteOn())
        {
            int baseVelocity = message.getVelocity();
            float velocityVariation = calculateVelocityVariation(static_cast<float>(baseVelocity), variation);
            int newVelocity = juce::jlimit(1, 127, static_cast<int>(velocityVariation));
            message = juce::MidiMessage::noteOn(message.getChannel(), message.getNoteNumber(), static_cast<juce::uint8>(newVelocity));
        }
    }
}

void GrooveShaper::addGhostNotes(std::vector<juce::MidiMessage>& midiMessages, float ghostAmount, float tempo)
{
    if (ghostAmount <= 0.0f) return;
    
    std::vector<juce::MidiMessage> newMessages;
    
    for (const auto& message : midiMessages)
    {
        newMessages.push_back(message);
        
        if (message.isNoteOn())
        {
            double timeInSeconds = message.getTimeStamp();
            float beatPosition = getBeatPosition(timeInSeconds, tempo, 4.0f);
            
            // Add ghost notes on off-beats
            if (shouldAddGhostNote(beatPosition, ghostAmount))
            {
                // Create a ghost note (softer velocity)
                int ghostVelocity = juce::jlimit(1, 127, static_cast<int>(message.getVelocity() * 0.3f));
                double ghostTime = timeInSeconds + (0.5f / tempo) * 60.0f; // Half beat later
                
                juce::MidiMessage ghostNoteOn = juce::MidiMessage::noteOn(
                    message.getChannel(), message.getNoteNumber(), static_cast<juce::uint8>(ghostVelocity));
                ghostNoteOn.setTimeStamp(ghostTime);
                newMessages.push_back(ghostNoteOn);
                
                // Add corresponding note off
                juce::MidiMessage ghostNoteOff = juce::MidiMessage::noteOff(
                    message.getChannel(), message.getNoteNumber(), static_cast<juce::uint8>(ghostVelocity));
                ghostNoteOff.setTimeStamp(ghostTime + 0.1); // Short duration
                newMessages.push_back(ghostNoteOff);
            }
        }
    }
    
    midiMessages = newMessages;
}

float GrooveShaper::calculateSwingOffset(float beatPosition, float swingAmount)
{
    // Swing affects off-beat notes (positions 0.5-1.0)
    if (beatPosition >= 0.5f && beatPosition < 1.0f)
    {
        float swingPosition = (beatPosition - 0.5f) / 0.5f; // Normalize to 0-1
        return swingPosition * swingAmount * 0.1f; // Maximum 0.1 beat offset
    }
    return 0.0f;
}

float GrooveShaper::calculateMicroTimingOffset(float baseOffset, float microTiming)
{
    // Generate human-like timing variation
    float variation = (random.nextFloat() - 0.5f) * 2.0f; // -1 to 1
    return variation * microTiming * 0.05f; // Maximum 0.05 beat variation
}

float GrooveShaper::calculateAccentMultiplier(float beatPosition, float accentPattern, float timeSignature)
{
    float accent = 1.0f;
    
    // Strong beats get more accent
    if (isStrongBeat(beatPosition, timeSignature))
    {
        accent = 1.0f + accentPattern * 0.5f;
    }
    // Off-beats get less accent
    else if (isOffBeat(beatPosition))
    {
        accent = 1.0f - accentPattern * 0.3f;
    }
    
    return juce::jlimit(0.1f, 2.0f, accent);
}

float GrooveShaper::calculateVelocityVariation(float baseVelocity, float variation)
{
    float variationAmount = (random.nextFloat() - 0.5f) * 2.0f * variation;
    return baseVelocity * (1.0f + variationAmount * 0.3f); // Maximum 30% variation
}

float GrooveShaper::getBeatPosition(double timeInSeconds, float tempo, float timeSignature)
{
    double beatsPerSecond = tempo / 60.0;
    double totalBeats = timeInSeconds * beatsPerSecond;
    return static_cast<float>(std::fmod(totalBeats, timeSignature));
}

bool GrooveShaper::isOnBeat(float beatPosition, float tolerance)
{
    return std::abs(beatPosition - std::round(beatPosition)) < tolerance;
}

bool GrooveShaper::isOffBeat(float beatPosition, float tolerance)
{
    return !isOnBeat(beatPosition, tolerance) && beatPosition > 0.0f;
}

bool GrooveShaper::isStrongBeat(float beatPosition, float timeSignature)
{
    float beatInMeasure = std::fmod(beatPosition, timeSignature);
    return beatInMeasure < 0.1f || std::abs(beatInMeasure - 2.0f) < 0.1f; // Beat 1 and 3
}

float GrooveShaper::generateHumanTimingOffset(float baseOffset, float humanization)
{
    // Use a more sophisticated humanization algorithm
    float randomVariation = (random.nextFloat() - 0.5f) * 2.0f;
    float humanFactor = std::sin(baseOffset * juce::MathConstants<float>::pi) * 0.1f;
    return (randomVariation + humanFactor) * humanization * 0.05f;
}

float GrooveShaper::generateVelocityVariation(float baseVelocity, float variation)
{
    // More musical velocity variation
    float randomVariation = (random.nextFloat() - 0.5f) * 2.0f;
    float musicalFactor = std::sin(baseVelocity / 127.0f * juce::MathConstants<float>::pi) * 0.2f;
    return baseVelocity * (1.0f + (randomVariation + musicalFactor) * variation * 0.2f);
}

bool GrooveShaper::shouldAddGhostNote(float beatPosition, float ghostAmount)
{
    // Ghost notes are more likely on off-beats
    if (isOffBeat(beatPosition))
    {
        return random.nextFloat() < ghostAmount * 0.3f;
    }
    return random.nextFloat() < ghostAmount * 0.1f;
}
