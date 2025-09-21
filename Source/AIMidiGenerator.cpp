#include "AIMidiGenerator.h"

AIMidiGenerator::AIMidiGenerator() : random(juce::Time::currentTimeMillis())
{
    initializePatternLibraries();
    initializeInstrumentPresets();
}

AIMidiGenerator::~AIMidiGenerator()
{
}

void AIMidiGenerator::initializePatternLibraries()
{
    // Initialize pattern libraries for different moods
    std::vector<std::string> moods = {"chill", "energetic", "suspenseful", "uplifting", 
                                     "ominous", "romantic", "gritty", "dreamy", "frantic", "focused"};
    
    for (const auto& mood : moods)
    {
        patternLibraries[mood] = std::vector<GeneratedPattern>();
    }
}

void AIMidiGenerator::initializeInstrumentPresets()
{
    // Initialize instrument presets for different moods
    InstrumentPreset piano;
    piano.program = 0; // Acoustic Piano
    piano.name = "Piano";
    piano.volume = 0.8f;
    piano.pan = 0.0f;
    instrumentPresets[0] = piano;
    
    InstrumentPreset strings;
    strings.program = 48; // String Ensemble
    strings.name = "Strings";
    strings.volume = 0.7f;
    strings.pan = -0.3f;
    instrumentPresets[1] = strings;
    
    InstrumentPreset brass;
    brass.program = 56; // Trumpet
    brass.name = "Brass";
    brass.volume = 0.9f;
    brass.pan = 0.3f;
    instrumentPresets[2] = brass;
    
    InstrumentPreset synth;
    synth.program = 80; // Lead Synth
    synth.name = "Synth";
    synth.volume = 0.8f;
    synth.pan = 0.0f;
    instrumentPresets[3] = synth;
}

void AIMidiGenerator::setGenerationContext(const GenerationContext& context)
{
    currentContext = context;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateMelody(double duration, int channel)
{
    GeneratedPattern pattern;
    pattern.patternType = "melody";
    pattern.duration = duration;
    
    // Generate melody based on mood and context
    int noteCount = static_cast<int>(duration * 4); // 4 notes per second
    auto notes = generateMelodyNotes(noteCount, currentContext.key, currentContext.scale);
    auto rhythm = generateMelodyRhythm(noteCount, currentContext.tempo);
    auto velocities = generateMelodyVelocities(noteCount, currentContext.energy);
    
    double currentTime = 0.0;
    for (size_t i = 0; i < notes.size() && i < rhythm.size() && i < velocities.size(); ++i)
    {
        // Note on
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(
            channel, notes[i], static_cast<juce::uint8>(velocities[i]));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        // Note off
        double noteDuration = rhythm[i] * (60.0 / currentContext.tempo);
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(
            channel, notes[i], static_cast<juce::uint8>(velocities[i]));
        noteOff.setTimeStamp(currentTime + noteDuration);
        pattern.messages.push_back(noteOff);
        
        currentTime += noteDuration * 0.8; // Slight overlap
    }
    
    pattern.confidence = 0.8f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateHarmony(double duration, int channel)
{
    GeneratedPattern pattern;
    pattern.patternType = "harmony";
    pattern.duration = duration;
    
    // Generate chord progression
    int chordCount = static_cast<int>(duration); // One chord per second
    auto progression = generateChordProgression(chordCount, currentContext.key, currentContext.scale);
    
    double currentTime = 0.0;
    for (const auto& chord : progression)
    {
        auto voicing = generateChordVoicing(chord, currentContext.key);
        
        // Play chord
        for (int note : voicing)
        {
            juce::MidiMessage noteOn = juce::MidiMessage::noteOn(
                channel, note, static_cast<juce::uint8>(60 + currentContext.energy * 40));
            noteOn.setTimeStamp(currentTime);
            pattern.messages.push_back(noteOn);
        }
        
        // Release chord after 0.8 seconds
        currentTime += 0.8;
        for (int note : voicing)
        {
            juce::MidiMessage noteOff = juce::MidiMessage::noteOff(
                channel, note, static_cast<juce::uint8>(60));
            noteOff.setTimeStamp(currentTime);
            pattern.messages.push_back(noteOff);
        }
        
        currentTime += 0.2; // Gap between chords
    }
    
    pattern.confidence = 0.7f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateRhythm(double duration, int channel)
{
    GeneratedPattern pattern;
    pattern.patternType = "rhythm";
    pattern.duration = duration;
    
    // Generate drum pattern based on mood
    int beatCount = static_cast<int>(duration * 4); // 4 beats per second
    auto drumPattern = generateDrumPattern(beatCount, currentContext.energy, currentContext.primaryMood);
    auto rhythm = generateRhythmPattern(beatCount, currentContext.complexity, currentContext.primaryMood);
    
    double currentTime = 0.0;
    for (size_t i = 0; i < drumPattern.size() && i < rhythm.size(); ++i)
    {
        if (drumPattern[i] > 0) // If there's a drum hit
        {
            int velocity = static_cast<int>(60 + currentContext.energy * 40);
            juce::MidiMessage noteOn = juce::MidiMessage::noteOn(
                channel, drumPattern[i], static_cast<juce::uint8>(velocity));
            noteOn.setTimeStamp(currentTime);
            pattern.messages.push_back(noteOn);
            
            // Short drum hit
            juce::MidiMessage noteOff = juce::MidiMessage::noteOff(
                channel, drumPattern[i], static_cast<juce::uint8>(velocity));
            noteOff.setTimeStamp(currentTime + 0.1);
            pattern.messages.push_back(noteOff);
        }
        
        currentTime += rhythm[i] * (60.0 / currentContext.tempo);
    }
    
    pattern.confidence = 0.9f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateFill(double duration, int channel)
{
    GeneratedPattern pattern;
    pattern.patternType = "fill";
    pattern.duration = duration;
    
    if (channel == 9) // Drum channel
    {
        return generateDrumFill(duration, currentContext.energy);
    }
    else
    {
        return generateMelodicFill(duration, currentContext.key, currentContext.scale);
    }
}

void AIMidiGenerator::generateRealTimeContent(std::vector<juce::MidiMessage>& output, double currentTime, double lookAhead)
{
    // Generate content based on current context and time
    if (currentContext.primaryMood == "energetic")
    {
        auto pattern = generateEnergeticPattern(lookAhead);
        for (const auto& msg : pattern.messages)
        {
            output.push_back(msg);
        }
    }
    else if (currentContext.primaryMood == "chill")
    {
        auto pattern = generateChillPattern(lookAhead);
        for (const auto& msg : pattern.messages)
        {
            output.push_back(msg);
        }
    }
    // Add more mood-specific generation...
}

void AIMidiGenerator::updateContext(const GenerationContext& context)
{
    currentContext = context;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateMoodPattern(const std::string& mood, double duration, const std::string& patternType)
{
    if (mood == "chill") return generateChillPattern(duration);
    if (mood == "energetic") return generateEnergeticPattern(duration);
    if (mood == "suspenseful") return generateSuspensefulPattern(duration);
    if (mood == "uplifting") return generateUpliftingPattern(duration);
    if (mood == "ominous") return generateOminousPattern(duration);
    if (mood == "romantic") return generateRomanticPattern(duration);
    if (mood == "gritty") return generateGrittyPattern(duration);
    if (mood == "dreamy") return generateDreamyPattern(duration);
    if (mood == "frantic") return generateFranticPattern(duration);
    if (mood == "focused") return generateFocusedPattern(duration);
    
    // Default pattern
    GeneratedPattern pattern;
    pattern.patternType = patternType;
    pattern.duration = duration;
    pattern.confidence = 0.5f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateTransitionPattern(const std::string& fromMood, const std::string& toMood, double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "transition";
    pattern.duration = duration;
    
    // Generate transition between moods
    // This would involve morphing from one mood's characteristics to another
    
    pattern.confidence = 0.6f;
    return pattern;
}

void AIMidiGenerator::setInstrumentPreset(int channel, const InstrumentPreset& preset)
{
    instrumentPresets[channel] = preset;
}

AIMidiGenerator::InstrumentPreset AIMidiGenerator::getInstrumentPreset(int channel) const
{
    auto it = instrumentPresets.find(channel);
    if (it != instrumentPresets.end())
        return it->second;
    
    // Return default preset
    InstrumentPreset defaultPreset;
    defaultPreset.program = 0;
    defaultPreset.name = "Piano";
    defaultPreset.volume = 0.8f;
    defaultPreset.pan = 0.0f;
    return defaultPreset;
}

std::vector<AIMidiGenerator::InstrumentPreset> AIMidiGenerator::getRecommendedPresets(const std::string& mood) const
{
    std::vector<InstrumentPreset> presets;
    
    if (mood == "chill" || mood == "dreamy")
    {
        presets.push_back(instrumentPresets.at(1)); // Strings
        presets.push_back(instrumentPresets.at(0)); // Piano
    }
    else if (mood == "energetic" || mood == "frantic")
    {
        presets.push_back(instrumentPresets.at(2)); // Brass
        presets.push_back(instrumentPresets.at(3)); // Synth
    }
    else if (mood == "romantic")
    {
        presets.push_back(instrumentPresets.at(1)); // Strings
        presets.push_back(instrumentPresets.at(0)); // Piano
    }
    else
    {
        presets.push_back(instrumentPresets.at(0)); // Piano
    }
    
    return presets;
}

// Implementation of mood-specific pattern generation methods
AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateChillPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "chill";
    pattern.duration = duration;
    
    // Generate relaxed, ambient pattern
    int noteCount = static_cast<int>(duration * 2); // Slower notes
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        int note = 60 + random.nextInt(12); // Random notes in one octave
        int velocity = 40 + random.nextInt(30); // Soft velocities
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + 1.0); // Long notes
        pattern.messages.push_back(noteOff);
        
        currentTime += 0.5 + random.nextFloat() * 0.5; // Variable timing
    }
    
    pattern.confidence = 0.8f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateEnergeticPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "energetic";
    pattern.duration = duration;
    
    // Generate fast, energetic pattern
    int noteCount = static_cast<int>(duration * 8); // Fast notes
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        int note = 60 + random.nextInt(24); // Wider range
        int velocity = 80 + random.nextInt(40); // Loud velocities
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + 0.1); // Short notes
        pattern.messages.push_back(noteOff);
        
        currentTime += 0.1 + random.nextFloat() * 0.1; // Fast timing
    }
    
    pattern.confidence = 0.9f;
    return pattern;
}

// Complete mood pattern implementations
AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateSuspensefulPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "suspenseful";
    pattern.duration = duration;
    
    // Generate tense, building pattern with irregular timing
    int noteCount = static_cast<int>(duration * 3); // Moderate density
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        // Use minor scale with chromatic tension
        int baseNote = 60 + (i % 12); // C minor scale base
        int tensionNote = baseNote + (random.nextInt(3) - 1); // Add chromatic tension
        int note = juce::jlimit(36, 84, tensionNote);
        
        // Varying velocities for tension
        int velocity = 50 + random.nextInt(40); // Medium to high velocity
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        // Irregular note lengths for suspense
        double noteLength = 0.3 + random.nextFloat() * 0.4; // 0.3-0.7 seconds
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + noteLength);
        pattern.messages.push_back(noteOff);
        
        // Irregular timing - sometimes pause, sometimes rush
        double nextTime = 0.2 + random.nextFloat() * 0.6; // 0.2-0.8 seconds
        currentTime += nextTime;
    }
    
    pattern.confidence = 0.85f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateUpliftingPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "uplifting";
    pattern.duration = duration;
    
    // Generate ascending, bright pattern
    int noteCount = static_cast<int>(duration * 4); // Higher density
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        // Ascending pattern with major scale
        int scaleDegree = i % 7; // Major scale degrees
        int octave = 4 + (i / 7); // Ascending octaves
        int note = 60 + scaleDegree + (octave * 12); // C major scale
        
        // Bright, energetic velocities
        int velocity = 70 + random.nextInt(30); // High velocity
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        // Shorter, punchy notes
        double noteLength = 0.2 + random.nextFloat() * 0.3; // 0.2-0.5 seconds
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + noteLength);
        pattern.messages.push_back(noteOff);
        
        // Regular, upbeat timing
        currentTime += 0.25 + random.nextFloat() * 0.1; // Slight variation
    }
    
    pattern.confidence = 0.9f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateOminousPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "ominous";
    pattern.duration = duration;
    
    // Generate dark, descending pattern
    int noteCount = static_cast<int>(duration * 2); // Lower density
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        // Descending pattern with minor scale and tritones
        int scaleDegree = (6 - (i % 7)) % 7; // Descending minor scale
        int octave = 5 - (i / 7); // Descending octaves
        int note = 60 + scaleDegree + (octave * 12);
        
        // Add tritone for dissonance
        if (random.nextFloat() < 0.3f)
        {
            note += 6; // Tritone
        }
        
        note = juce::jlimit(36, 84, note);
        
        // Dark, low velocities
        int velocity = 30 + random.nextInt(30); // Low to medium velocity
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        // Long, sustained notes
        double noteLength = 0.8 + random.nextFloat() * 0.4; // 0.8-1.2 seconds
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + noteLength);
        pattern.messages.push_back(noteOff);
        
        // Slow, ominous timing
        currentTime += 0.5 + random.nextFloat() * 0.3; // 0.5-0.8 seconds
    }
    
    pattern.confidence = 0.8f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateRomanticPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "romantic";
    pattern.duration = duration;
    
    // Generate flowing, lyrical pattern
    int noteCount = static_cast<int>(duration * 3); // Moderate density
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        // Romantic intervals (thirds, sixths)
        int interval = (i % 2 == 0) ? 4 : 7; // Major third or perfect fifth
        int baseNote = 60 + (i % 12);
        int note = baseNote + interval;
        note = juce::jlimit(48, 84, note);
        
        // Expressive velocities with crescendo/decrescendo
        int baseVelocity = 60;
        float crescendo = std::sin(currentTime * 2.0) * 0.3f; // Musical phrasing
        int velocity = juce::jlimit(40, 80, static_cast<int>(baseVelocity + crescendo * 20));
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        // Flowing note lengths
        double noteLength = 0.4 + random.nextFloat() * 0.4; // 0.4-0.8 seconds
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + noteLength);
        pattern.messages.push_back(noteOff);
        
        // Rubato timing - slight tempo variations
        double baseTime = 0.3;
        double rubato = std::sin(currentTime * 1.5) * 0.1; // Subtle tempo variation
        currentTime += baseTime + rubato;
    }
    
    pattern.confidence = 0.85f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateGrittyPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "gritty";
    pattern.duration = duration;
    
    // Generate aggressive, distorted pattern
    int noteCount = static_cast<int>(duration * 6); // High density
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        // Use blues scale with chromatic passing tones
        int bluesScale[] = {0, 3, 5, 6, 7, 10}; // Blues scale intervals
        int scaleIndex = i % 6;
        int octave = 4 + (i / 6);
        int note = 60 + bluesScale[scaleIndex] + (octave * 12);
        
        // Add chromatic grit
        if (random.nextFloat() < 0.4f)
        {
            note += random.nextInt(3) - 1; // Chromatic variation
        }
        
        note = juce::jlimit(36, 84, note);
        
        // Aggressive velocities
        int velocity = 80 + random.nextInt(40); // High velocity
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        // Short, staccato notes
        double noteLength = 0.1 + random.nextFloat() * 0.2; // 0.1-0.3 seconds
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + noteLength);
        pattern.messages.push_back(noteOff);
        
        // Aggressive, syncopated timing
        double baseTime = 0.15;
        if (i % 3 == 0) baseTime *= 0.5; // Syncopation
        currentTime += baseTime + random.nextFloat() * 0.1;
    }
    
    pattern.confidence = 0.9f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateDreamyPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "dreamy";
    pattern.duration = duration;
    
    // Generate ethereal, floating pattern
    int noteCount = static_cast<int>(duration * 2); // Low density
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        // Use whole tone scale for dreamy effect
        int wholeToneScale[] = {0, 2, 4, 6, 8, 10}; // Whole tone scale
        int scaleIndex = i % 6;
        int octave = 4 + (i / 6);
        int note = 60 + wholeToneScale[scaleIndex] + (octave * 12);
        note = juce::jlimit(48, 84, note);
        
        // Soft, floating velocities
        int velocity = 40 + random.nextInt(25); // Low to medium velocity
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        // Very long, sustained notes
        double noteLength = 1.0 + random.nextFloat() * 1.0; // 1.0-2.0 seconds
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + noteLength);
        pattern.messages.push_back(noteOff);
        
        // Slow, floating timing
        currentTime += 0.6 + random.nextFloat() * 0.4; // 0.6-1.0 seconds
    }
    
    pattern.confidence = 0.8f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateFranticPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "frantic";
    pattern.duration = duration;
    
    // Generate chaotic, high-energy pattern
    int noteCount = static_cast<int>(duration * 12); // Very high density
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        // Random chromatic notes for chaos
        int note = 60 + random.nextInt(24) - 12; // Wide range
        note = juce::jlimit(36, 84, note);
        
        // Very high velocities
        int velocity = 90 + random.nextInt(35); // Very high velocity
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        // Very short notes
        double noteLength = 0.05 + random.nextFloat() * 0.1; // 0.05-0.15 seconds
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + noteLength);
        pattern.messages.push_back(noteOff);
        
        // Chaotic timing
        currentTime += 0.05 + random.nextFloat() * 0.1; // 0.05-0.15 seconds
    }
    
    pattern.confidence = 0.95f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateFocusedPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "focused";
    pattern.duration = duration;
    
    // Generate precise, structured pattern
    int noteCount = static_cast<int>(duration * 4); // Moderate density
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        // Use pentatonic scale for clarity
        int pentatonicScale[] = {0, 2, 4, 7, 9}; // Pentatonic scale intervals
        int scaleIndex = i % 5;
        int octave = 4 + (i / 5);
        int note = 60 + pentatonicScale[scaleIndex] + (octave * 12);
        note = juce::jlimit(48, 84, note);
        
        // Consistent, focused velocities
        int velocity = 65 + random.nextInt(20); // Medium-high, consistent
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        // Precise note lengths
        double noteLength = 0.25 + random.nextFloat() * 0.1; // 0.25-0.35 seconds
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + noteLength);
        pattern.messages.push_back(noteOff);
        
        // Precise, metronomic timing
        currentTime += 0.25; // Exact quarter notes
    }
    
    pattern.confidence = 0.9f;
    return pattern;
}

// Helper method implementations
std::vector<int> AIMidiGenerator::generateMelodyNotes(int length, int key, const std::string& scale)
{
    std::vector<int> notes;
    auto scaleNotes = getScaleNotes(key, scale);
    
    for (int i = 0; i < length; ++i)
    {
        int noteIndex = random.nextInt(static_cast<int>(scaleNotes.size()));
        int octave = 3 + random.nextInt(3); // Octaves 3-5
        notes.push_back(scaleNotes[noteIndex] + (octave * 12));
    }
    
    return notes;
}

std::vector<double> AIMidiGenerator::generateMelodyRhythm(int length, float tempo)
{
    std::vector<double> rhythm;
    
    for (int i = 0; i < length; ++i)
    {
        // Generate rhythm based on tempo
        double baseDuration = 60.0 / tempo; // Quarter note duration
        double variation = 0.5 + random.nextFloat(); // 0.5 to 1.5 times base duration
        rhythm.push_back(baseDuration * variation);
    }
    
    return rhythm;
}

std::vector<int> AIMidiGenerator::generateMelodyVelocities(int length, float energy)
{
    std::vector<int> velocities;
    
    for (int i = 0; i < length; ++i)
    {
        int baseVelocity = static_cast<int>(40 + energy * 60); // 40-100 based on energy
        int variation = random.nextInt(20) - 10; // ±10 variation
        velocities.push_back(juce::jlimit(1, 127, baseVelocity + variation));
    }
    
    return velocities;
}

std::vector<std::vector<int>> AIMidiGenerator::generateChordProgression(int length, int key, const std::string& scale)
{
    std::vector<std::vector<int>> progression;
    
    // Simple chord progression based on key
    std::vector<int> chordRoots = {0, 2, 4, 5}; // I, iii, IV, V progression
    
    for (int i = 0; i < length; ++i)
    {
        int rootIndex = i % chordRoots.size();
        int root = key + chordRoots[rootIndex];
        std::vector<int> chord = {root, root + 4, root + 7}; // Major triad
        progression.push_back(chord);
    }
    
    return progression;
}

std::vector<int> AIMidiGenerator::generateChordVoicing(const std::vector<int>& chord, int key)
{
    std::vector<int> voicing;
    
    for (int note : chord)
    {
        int octave = 3 + random.nextInt(2); // Octaves 3-4
        voicing.push_back(note + (octave * 12));
    }
    
    return voicing;
}

std::vector<double> AIMidiGenerator::generateRhythmPattern(int length, float complexity, const std::string& mood)
{
    std::vector<double> rhythm;
    
    for (int i = 0; i < length; ++i)
    {
        double baseDuration = 0.25; // Quarter note
        double variation = 0.5 + random.nextFloat() * complexity; // More complex = more variation
        rhythm.push_back(baseDuration * variation);
    }
    
    return rhythm;
}

std::vector<int> AIMidiGenerator::generateDrumPattern(int length, float energy, const std::string& mood)
{
    std::vector<int> pattern;
    
    // Basic drum pattern: kick on 1 and 3, snare on 2 and 4, hi-hat on all beats
    for (int i = 0; i < length; ++i)
    {
        int beat = i % 4;
        int drum = 0; // No drum
        
        if (beat == 0 || beat == 2) // Kick drum
        {
            drum = 36; // C1
        }
        else if (beat == 1 || beat == 3) // Snare drum
        {
            drum = 38; // D1
        }
        
        // Add hi-hat based on energy
        if (random.nextFloat() < energy)
        {
            drum = 42; // F#1
        }
        
        pattern.push_back(drum);
    }
    
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateDrumFill(double duration, float energy)
{
    GeneratedPattern pattern;
    pattern.patternType = "drum_fill";
    pattern.duration = duration;
    
    // Generate drum fill
    int noteCount = static_cast<int>(duration * 16); // Fast fills
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i)
    {
        int drum = 36 + random.nextInt(12); // Various drums
        int velocity = static_cast<int>(60 + energy * 40);
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(9, drum, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(9, drum, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + 0.05); // Very short
        pattern.messages.push_back(noteOff);
        
        currentTime += 0.05 + random.nextFloat() * 0.05;
    }
    
    pattern.confidence = 0.8f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateMelodicFill(double duration, int key, const std::string& scale)
{
    GeneratedPattern pattern;
    pattern.patternType = "melodic_fill";
    pattern.duration = duration;
    
    // Generate melodic fill
    auto notes = generateMelodyNotes(static_cast<int>(duration * 8), key, scale);
    double currentTime = 0.0;
    
    for (int note : notes)
    {
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(80));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(80));
        noteOff.setTimeStamp(currentTime + 0.1);
        pattern.messages.push_back(noteOff);
        
        currentTime += 0.1;
    }
    
    pattern.confidence = 0.7f;
    return pattern;
}

std::vector<int> AIMidiGenerator::getScaleNotes(int key, const std::string& scale)
{
    std::vector<int> notes;
    
    if (scale == "major")
    {
        notes = {0, 2, 4, 5, 7, 9, 11}; // Major scale
    }
    else if (scale == "minor")
    {
        notes = {0, 2, 3, 5, 7, 8, 10}; // Natural minor scale
    }
    else if (scale == "dorian")
    {
        notes = {0, 2, 3, 5, 7, 9, 10}; // Dorian mode
    }
    else
    {
        notes = {0, 2, 4, 5, 7, 9, 11}; // Default to major
    }
    
    // Transpose to key
    for (int& note : notes)
    {
        note += key;
    }
    
    return notes;
}

std::vector<int> AIMidiGenerator::getChordNotes(int root, const std::string& chordType)
{
    std::vector<int> notes;
    
    if (chordType == "major")
    {
        notes = {root, root + 4, root + 7};
    }
    else if (chordType == "minor")
    {
        notes = {root, root + 3, root + 7};
    }
    else if (chordType == "diminished")
    {
        notes = {root, root + 3, root + 6};
    }
    else
    {
        notes = {root, root + 4, root + 7}; // Default to major
    }
    
    return notes;
}

bool AIMidiGenerator::isInScale(int note, int key, const std::string& scale)
{
    auto scaleNotes = getScaleNotes(key, scale);
    int noteInScale = note % 12;
    
    for (int scaleNote : scaleNotes)
    {
        if (scaleNote % 12 == noteInScale)
            return true;
    }
    
    return false;
}

int AIMidiGenerator::getNoteInKey(int note, int key)
{
    // Ensure note is in the correct key
    int noteInScale = note % 12;
    int octave = note / 12;
    
    // Find closest note in key
    auto scaleNotes = getScaleNotes(key, "major");
    int closestNote = scaleNotes[0];
    int minDistance = 12;
    
    for (int scaleNote : scaleNotes)
    {
        int distance = std::abs(scaleNote - noteInScale);
        if (distance < minDistance)
        {
            minDistance = distance;
            closestNote = scaleNote;
        }
    }
    
    return closestNote + (octave * 12);
}

float AIMidiGenerator::analyzePatternComplexity(const GeneratedPattern& pattern)
{
    // Analyze the complexity of a generated pattern
    if (pattern.messages.empty()) return 0.0f;
    
    int noteCount = 0;
    double totalDuration = 0.0;
    
    for (const auto& msg : pattern.messages)
    {
        if (msg.isNoteOn())
        {
            noteCount++;
        }
    }
    
    if (noteCount == 0) return 0.0f;
    
    // Complexity based on note density and variation
    float density = static_cast<float>(noteCount) / pattern.duration;
    return juce::jlimit(0.0f, 1.0f, density / 10.0f); // Normalize to 0-1
}

float AIMidiGenerator::analyzePatternEnergy(const GeneratedPattern& pattern)
{
    // Analyze the energy of a generated pattern
    if (pattern.messages.empty()) return 0.0f;
    
    float totalVelocity = 0.0f;
    int velocityCount = 0;
    
    for (const auto& msg : pattern.messages)
    {
        if (msg.isNoteOn())
        {
            totalVelocity += msg.getVelocity();
            velocityCount++;
        }
    }
    
    if (velocityCount == 0) return 0.0f;
    
    float averageVelocity = totalVelocity / velocityCount;
    return juce::jlimit(0.0f, 1.0f, averageVelocity / 127.0f);
}

std::string AIMidiGenerator::classifyPatternType(const GeneratedPattern& pattern)
{
    // Classify the type of pattern based on its characteristics
    float complexity = analyzePatternComplexity(pattern);
    float energy = analyzePatternEnergy(pattern);
    
    if (complexity > 0.7f && energy > 0.7f)
        return "frantic";
    else if (complexity < 0.3f && energy < 0.3f)
        return "chill";
    else if (energy > 0.6f)
        return "energetic";
    else if (complexity > 0.6f)
        return "complex";
    else
        return "moderate";
}
