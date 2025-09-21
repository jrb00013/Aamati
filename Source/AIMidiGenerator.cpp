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
    
    // Initialize hybrid mood combinations
    initializeHybridMoods();
}

void AIMidiGenerator::initializeHybridMoods()
{
    // Define 30+ hybrid mood combinations with their characteristics
    
    // Single mood intensifications (same mood repeated)
    hybridMoods["romantic-romantic"] = {"romantic", "romantic", {0.5f, 0.5f}, "deep-romance"};
    hybridMoods["dreamy-dreamy"] = {"dreamy", "dreamy", {0.5f, 0.5f}, "ethereal-bliss"};
    hybridMoods["chill-chill"] = {"chill", "chill", {0.5f, 0.5f}, "zen-calm"};
    hybridMoods["energetic-energetic"] = {"energetic", "energetic", {0.5f, 0.5f}, "pure-energy"};
    hybridMoods["suspenseful-suspenseful"] = {"suspenseful", "suspenseful", {0.5f, 0.5f}, "deep-tension"};
    hybridMoods["uplifting-uplifting"] = {"uplifting", "uplifting", {0.5f, 0.5f}, "pure-joy"};
    hybridMoods["ominous-ominous"] = {"ominous", "ominous", {0.5f, 0.5f}, "dark-abyss"};
    hybridMoods["gritty-gritty"] = {"gritty", "gritty", {0.5f, 0.5f}, "raw-power"};
    hybridMoods["frantic-frantic"] = {"frantic", "frantic", {0.5f, 0.5f}, "pure-chaos"};
    hybridMoods["focused-focused"] = {"focused", "focused", {0.5f, 0.5f}, "laser-precision"};
    
    // Triple same mood intensifications
    hybridMoods["romantic-romantic-romantic"] = {"romantic", "romantic", "romantic", {0.33f, 0.33f, 0.34f}, "passionate-storm"};
    hybridMoods["dreamy-dreamy-dreamy"] = {"dreamy", "dreamy", "dreamy", {0.33f, 0.33f, 0.34f}, "cosmic-drift"};
    hybridMoods["chill-chill-chill"] = {"chill", "chill", "chill", {0.33f, 0.33f, 0.34f}, "meditative-trance"};
    hybridMoods["energetic-energetic-energetic"] = {"energetic", "energetic", "energetic", {0.33f, 0.33f, 0.34f}, "explosive-force"};
    hybridMoods["suspenseful-suspenseful-suspenseful"] = {"suspenseful", "suspenseful", "suspenseful", {0.33f, 0.33f, 0.34f}, "paralyzing-dread"};
    
    // Dual combinations
    hybridMoods["chill-energetic"] = {"chill", "energetic", {0.7f, 0.3f}, "relaxed-energy"};
    hybridMoods["energetic-chill"] = {"energetic", "chill", {0.6f, 0.4f}, "controlled-energy"};
    hybridMoods["suspenseful-uplifting"] = {"suspenseful", "uplifting", {0.6f, 0.4f}, "building-tension"};
    hybridMoods["uplifting-suspenseful"] = {"uplifting", "suspenseful", {0.7f, 0.3f}, "hopeful-tension"};
    hybridMoods["ominous-romantic"] = {"ominous", "romantic", {0.5f, 0.5f}, "dark-romance"};
    hybridMoods["romantic-ominous"] = {"romantic", "ominous", {0.6f, 0.4f}, "melancholic"};
    hybridMoods["gritty-dreamy"] = {"gritty", "dreamy", {0.4f, 0.6f}, "ethereal-grit"};
    hybridMoods["dreamy-gritty"] = {"dreamy", "gritty", {0.7f, 0.3f}, "soft-edge"};
    hybridMoods["frantic-focused"] = {"frantic", "focused", {0.3f, 0.7f}, "controlled-chaos"};
    hybridMoods["focused-frantic"] = {"focused", "frantic", {0.6f, 0.4f}, "intense-precision"};
    
    // Triple combinations
    hybridMoods["chill-energetic-romantic"] = {"chill", "energetic", "romantic", {0.4f, 0.3f, 0.3f}, "passionate-calm"};
    hybridMoods["suspenseful-uplifting-gritty"] = {"suspenseful", "uplifting", "gritty", {0.4f, 0.3f, 0.3f}, "raw-hope"};
    hybridMoods["dreamy-ominous-focused"] = {"dreamy", "ominous", "focused", {0.4f, 0.3f, 0.3f}, "dark-clarity"};
    hybridMoods["frantic-chill-uplifting"] = {"frantic", "chill", "uplifting", {0.3f, 0.4f, 0.3f}, "chaotic-peace"};
    hybridMoods["romantic-gritty-suspenseful"] = {"romantic", "gritty", "suspenseful", {0.4f, 0.3f, 0.3f}, "passionate-tension"};
    
    // Complex combinations
    hybridMoods["energetic-uplifting-focused"] = {"energetic", "uplifting", "focused", {0.4f, 0.3f, 0.3f}, "driven-optimism"};
    hybridMoods["chill-dreamy-romantic"] = {"chill", "dreamy", "romantic", {0.4f, 0.3f, 0.3f}, "ethereal-love"};
    hybridMoods["ominous-suspenseful-gritty"] = {"ominous", "suspenseful", "gritty", {0.4f, 0.3f, 0.3f}, "dark-intensity"};
    hybridMoods["frantic-energetic-gritty"] = {"frantic", "energetic", "gritty", {0.4f, 0.3f, 0.3f}, "raw-power"};
    hybridMoods["uplifting-focused-romantic"] = {"uplifting", "focused", "romantic", {0.4f, 0.3f, 0.3f}, "inspired-love"};
    
    // Quadruple combinations
    hybridMoods["chill-energetic-romantic-dreamy"] = {"chill", "energetic", "romantic", "dreamy", {0.3f, 0.25f, 0.25f, 0.2f}, "passionate-dream"};
    hybridMoods["suspenseful-uplifting-gritty-focused"] = {"suspenseful", "uplifting", "gritty", "focused", {0.3f, 0.25f, 0.25f, 0.2f}, "intense-determination"};
    hybridMoods["ominous-romantic-dreamy-chill"] = {"ominous", "romantic", "dreamy", "chill", {0.3f, 0.25f, 0.25f, 0.2f}, "dark-serenity"};
    hybridMoods["frantic-energetic-gritty-uplifting"] = {"frantic", "energetic", "gritty", "uplifting", {0.3f, 0.25f, 0.25f, 0.2f}, "explosive-joy"};
    hybridMoods["focused-suspenseful-romantic-chill"] = {"focused", "suspenseful", "romantic", "chill", {0.3f, 0.25f, 0.25f, 0.2f}, "controlled-passion"};
    
    // Extreme combinations
    hybridMoods["frantic-ominous-gritty-suspenseful"] = {"frantic", "ominous", "gritty", "suspenseful", {0.3f, 0.25f, 0.25f, 0.2f}, "apocalyptic-chaos"};
    hybridMoods["dreamy-romantic-chill-uplifting"] = {"dreamy", "romantic", "chill", "uplifting", {0.3f, 0.25f, 0.25f, 0.2f}, "heavenly-bliss"};
    hybridMoods["energetic-focused-uplifting-gritty"] = {"energetic", "focused", "uplifting", "gritty", {0.3f, 0.25f, 0.25f, 0.2f}, "unstoppable-force"};
    hybridMoods["chill-dreamy-romantic-focused"] = {"chill", "dreamy", "romantic", "focused", {0.3f, 0.25f, 0.25f, 0.2f}, "meditative-love"};
    hybridMoods["suspenseful-ominous-frantic-gritty"] = {"suspenseful", "ominous", "frantic", "gritty", {0.3f, 0.25f, 0.25f, 0.2f}, "nightmare-fuel"};
    
    // Balanced combinations
    hybridMoods["all-balanced"] = {"chill", "energetic", "suspenseful", "uplifting", "ominous", "romantic", "gritty", "dreamy", "frantic", "focused", 
                                 {0.1f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f, 0.1f}, "universal-harmony"};
    hybridMoods["positive-spectrum"] = {"chill", "energetic", "uplifting", "romantic", "dreamy", "focused", 
                                       {0.2f, 0.2f, 0.2f, 0.15f, 0.15f, 0.1f}, "pure-positivity"};
    hybridMoods["dark-spectrum"] = {"suspenseful", "ominous", "gritty", "frantic", 
                                   {0.3f, 0.3f, 0.2f, 0.2f}, "pure-darkness"};
    hybridMoods["dynamic-spectrum"] = {"energetic", "frantic", "gritty", "uplifting", "focused", 
                                      {0.25f, 0.2f, 0.2f, 0.2f, 0.15f}, "pure-energy"};
    hybridMoods["serene-spectrum"] = {"chill", "dreamy", "romantic", "focused", 
                                     {0.3f, 0.3f, 0.25f, 0.15f}, "pure-serenity"};
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

// Enhanced hybrid mood system
AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateHybridPattern(const std::vector<std::string>& moods, const std::vector<float>& weights, double duration)
{
    if (moods.empty() || moods.size() != weights.size()) {
        return generateDefaultPattern(duration);
    }
    
    GeneratedPattern pattern;
    pattern.patternType = "hybrid";
    pattern.duration = duration;
    
    // Check if this is a same-mood repetition (intensification)
    bool isSameMoodIntensification = true;
    for (size_t i = 1; i < moods.size(); ++i) {
        if (moods[i] != moods[0]) {
            isSameMoodIntensification = false;
            break;
        }
    }
    
    if (isSameMoodIntensification) {
        // Generate intensified version of the mood
        pattern = generateIntensifiedMoodPattern(moods[0], moods.size(), duration);
    } else {
        // Normalize weights
        float totalWeight = 0.0f;
        for (float weight : weights) {
            totalWeight += weight;
        }
        
        if (totalWeight <= 0.0f) {
            return generateDefaultPattern(duration);
        }
        
        // Generate base patterns for each mood
        std::vector<GeneratedPattern> basePatterns;
        for (const auto& mood : moods) {
            basePatterns.push_back(generateMoodPattern(mood, duration));
        }
        
        // Blend patterns based on weights
        pattern = blendPatterns(basePatterns, weights);
    }
    
    pattern.confidence = calculateHybridConfidence(moods, weights);
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateIntensifiedMoodPattern(const std::string& mood, int intensity, double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "intensified-" + mood;
    pattern.duration = duration;
    
    // Get base mood characteristics
    auto scale = getMoodScale(mood);
    double baseRhythm = getMoodRhythm(mood);
    int baseVelocity = getMoodVelocity(mood);
    
    // Calculate intensification factors
    float intensityMultiplier = 1.0f + (intensity - 1) * 0.3f; // 30% increase per repetition
    float densityMultiplier = 1.0f + (intensity - 1) * 0.2f;  // 20% density increase per repetition
    float complexityMultiplier = 1.0f + (intensity - 1) * 0.25f; // 25% complexity increase per repetition
    
    // Generate intensified pattern
    int noteCount = static_cast<int>(duration * 4 * densityMultiplier);
    double currentTime = 0.0;
    
    for (int i = 0; i < noteCount; ++i) {
        // Use scale with intensification
        int scaleIndex = i % scale.size();
        int octave = 4 + (i / scale.size());
        int note = scale[scaleIndex] + (octave * 12);
        note = juce::jlimit(36, 84, note);
        
        // Intensified velocity
        int intensifiedVelocity = static_cast<int>(baseVelocity * intensityMultiplier);
        intensifiedVelocity = juce::jlimit(1, 127, intensifiedVelocity);
        
        // Add complexity variations
        if (intensity > 1) {
            // Add chromatic passing tones for complexity
            if (random.nextFloat() < complexityMultiplier * 0.3f) {
                note += random.nextInt(3) - 1; // Chromatic variation
                note = juce::jlimit(36, 84, note);
            }
            
            // Add velocity variations for expressiveness
            int velocityVariation = random.nextInt(static_cast<int>(20 * complexityMultiplier)) - static_cast<int>(10 * complexityMultiplier);
            intensifiedVelocity = juce::jlimit(1, 127, intensifiedVelocity + velocityVariation);
        }
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(intensifiedVelocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        // Intensified rhythm (faster for higher intensity)
        double noteLength = baseRhythm / intensityMultiplier;
        if (intensity > 2) {
            noteLength *= (0.7f + random.nextFloat() * 0.6f); // More variation for high intensity
        }
        
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(intensifiedVelocity));
        noteOff.setTimeStamp(currentTime + noteLength);
        pattern.messages.push_back(noteOff);
        
        // Intensified timing
        double timeStep = baseRhythm / intensityMultiplier;
        if (intensity > 1) {
            timeStep *= (0.8f + random.nextFloat() * 0.4f); // More variation
        }
        currentTime += timeStep;
    }
    
    // Calculate confidence based on intensity
    float baseConfidence = 0.8f;
    float intensityBonus = (intensity - 1) * 0.05f; // 5% bonus per intensity level
    pattern.confidence = juce::jlimit(0.0f, 1.0f, baseConfidence + intensityBonus);
    
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateTransitionPattern(const std::string& fromMood, const std::string& toMood, double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "transition";
    pattern.duration = duration;
    
    // Generate smooth transition between moods
    int transitionSteps = static_cast<int>(duration * 4); // 4 steps per second
    double currentTime = 0.0;
    
    for (int step = 0; step < transitionSteps; ++step) {
        float progress = static_cast<float>(step) / transitionSteps;
        
        // Generate notes with morphing characteristics
        auto transitionNotes = generateTransitionNotes(fromMood, toMood, progress, 4); // 4 notes per step
        auto transitionRhythm = generateTransitionRhythm(fromMood, toMood, progress, 4);
        auto transitionVelocities = generateTransitionVelocities(fromMood, toMood, progress, 4);
        
        // Add notes to pattern
        for (size_t i = 0; i < transitionNotes.size() && i < transitionRhythm.size() && i < transitionVelocities.size(); ++i) {
            juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, transitionNotes[i], static_cast<juce::uint8>(transitionVelocities[i]));
            noteOn.setTimeStamp(currentTime);
            pattern.messages.push_back(noteOn);
            
            double noteDuration = transitionRhythm[i] * (60.0 / 120.0); // Assume 120 BPM
            juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, transitionNotes[i], static_cast<juce::uint8>(transitionVelocities[i]));
            noteOff.setTimeStamp(currentTime + noteDuration);
            pattern.messages.push_back(noteOff);
            
            currentTime += noteDuration * 0.8; // Slight overlap
        }
    }
    
    pattern.confidence = 0.8f;
    return pattern;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::blendPatterns(const std::vector<GeneratedPattern>& patterns, const std::vector<float>& weights)
{
    GeneratedPattern blendedPattern;
    blendedPattern.patternType = "blended";
    blendedPattern.duration = patterns.empty() ? 0.0 : patterns[0].duration;
    
    if (patterns.empty()) return blendedPattern;
    
    // Normalize weights
    float totalWeight = 0.0f;
    for (float weight : weights) {
        totalWeight += weight;
    }
    
    if (totalWeight <= 0.0f) return patterns[0];
    
    // Create time-sorted message list
    std::vector<juce::MidiMessage> allMessages;
    
    for (size_t i = 0; i < patterns.size(); ++i) {
        float normalizedWeight = weights[i] / totalWeight;
        
        for (const auto& message : patterns[i].messages) {
            juce::MidiMessage weightedMessage = message;
            
            // Apply weight to velocity
            if (message.isNoteOn()) {
                int newVelocity = static_cast<int>(message.getVelocity() * normalizedWeight);
                weightedMessage = juce::MidiMessage::noteOn(message.getChannel(), message.getNoteNumber(), static_cast<juce::uint8>(newVelocity));
            }
            
            allMessages.push_back(weightedMessage);
        }
    }
    
    // Sort messages by timestamp
    std::sort(allMessages.begin(), allMessages.end(), 
        [](const juce::MidiMessage& a, const juce::MidiMessage& b) {
            return a.getTimeStamp() < b.getTimeStamp();
        });
    
    // Merge overlapping notes and apply blending
    blendedPattern.messages = mergeOverlappingNotes(allMessages);
    
    return blendedPattern;
}

std::vector<juce::MidiMessage> AIMidiGenerator::mergeOverlappingNotes(const std::vector<juce::MidiMessage>& messages)
{
    std::vector<juce::MidiMessage> mergedMessages;
    std::map<int, std::vector<juce::MidiMessage>> activeNotes; // note -> messages
    
    for (const auto& message : messages) {
        if (message.isNoteOn()) {
            activeNotes[message.getNoteNumber()].push_back(message);
        } else if (message.isNoteOff()) {
            auto it = activeNotes.find(message.getNoteNumber());
            if (it != activeNotes.end() && !it->second.empty()) {
                // Find the most recent note on for this note
                auto& noteOnMessages = it->second;
                auto latestNoteOn = std::max_element(noteOnMessages.begin(), noteOnMessages.end(),
                    [](const juce::MidiMessage& a, const juce::MidiMessage& b) {
                        return a.getTimeStamp() < b.getTimeStamp();
                    });
                
                // Add the note on and off
                mergedMessages.push_back(*latestNoteOn);
                mergedMessages.push_back(message);
                
                // Remove this note from active notes
                activeNotes.erase(it);
            }
        }
    }
    
    return mergedMessages;
}

std::vector<int> AIMidiGenerator::generateTransitionNotes(const std::string& fromMood, const std::string& toMood, float progress, int count)
{
    std::vector<int> notes;
    
    // Get scale characteristics for both moods
    auto fromScale = getMoodScale(fromMood);
    auto toScale = getMoodScale(toMood);
    
    for (int i = 0; i < count; ++i) {
        // Interpolate between scales
        float fromWeight = 1.0f - progress;
        float toWeight = progress;
        
        int fromNote = fromScale[i % fromScale.size()] + 60; // C4 base
        int toNote = toScale[i % toScale.size()] + 60;
        
        // Linear interpolation
        int blendedNote = static_cast<int>(fromNote * fromWeight + toNote * toWeight);
        notes.push_back(juce::jlimit(36, 84, blendedNote));
    }
    
    return notes;
}

std::vector<double> AIMidiGenerator::generateTransitionRhythm(const std::string& fromMood, const std::string& toMood, float progress, int count)
{
    std::vector<double> rhythm;
    
    // Get rhythm characteristics for both moods
    double fromRhythm = getMoodRhythm(fromMood);
    double toRhythm = getMoodRhythm(toMood);
    
    for (int i = 0; i < count; ++i) {
        // Interpolate rhythm
        double blendedRhythm = fromRhythm * (1.0 - progress) + toRhythm * progress;
        
        // Add variation
        double variation = 0.5 + random.nextFloat();
        rhythm.push_back(blendedRhythm * variation);
    }
    
    return rhythm;
}

std::vector<int> AIMidiGenerator::generateTransitionVelocities(const std::string& fromMood, const std::string& toMood, float progress, int count)
{
    std::vector<int> velocities;
    
    // Get velocity characteristics for both moods
    int fromVelocity = getMoodVelocity(fromMood);
    int toVelocity = getMoodVelocity(toMood);
    
    for (int i = 0; i < count; ++i) {
        // Interpolate velocity
        int blendedVelocity = static_cast<int>(fromVelocity * (1.0f - progress) + toVelocity * progress);
        
        // Add variation
        int variation = random.nextInt(20) - 10;
        velocities.push_back(juce::jlimit(1, 127, blendedVelocity + variation));
    }
    
    return velocities;
}

std::vector<int> AIMidiGenerator::getMoodScale(const std::string& mood)
{
    if (mood == "chill" || mood == "dreamy") {
        return {0, 2, 4, 5, 7, 9, 11}; // Major scale
    } else if (mood == "energetic" || mood == "frantic") {
        return {0, 2, 4, 6, 7, 9, 11}; // Mixolydian
    } else if (mood == "suspenseful" || mood == "ominous") {
        return {0, 2, 3, 5, 7, 8, 10}; // Natural minor
    } else if (mood == "uplifting") {
        return {0, 2, 4, 5, 7, 9, 11}; // Major scale
    } else if (mood == "romantic") {
        return {0, 2, 4, 5, 7, 9, 11}; // Major scale
    } else if (mood == "gritty") {
        return {0, 3, 5, 6, 7, 10}; // Blues scale
    } else if (mood == "focused") {
        return {0, 2, 4, 7, 9}; // Pentatonic
    } else {
        return {0, 2, 4, 5, 7, 9, 11}; // Default major
    }
}

double AIMidiGenerator::getMoodRhythm(const std::string& mood)
{
    if (mood == "chill" || mood == "dreamy") {
        return 0.8; // Slow, sustained
    } else if (mood == "energetic" || mood == "frantic") {
        return 0.2; // Fast, staccato
    } else if (mood == "suspenseful" || mood == "ominous") {
        return 0.6; // Medium, irregular
    } else if (mood == "uplifting") {
        return 0.3; // Fast, punchy
    } else if (mood == "romantic") {
        return 0.5; // Medium, flowing
    } else if (mood == "gritty") {
        return 0.25; // Fast, aggressive
    } else if (mood == "focused") {
        return 0.4; // Medium, precise
    } else {
        return 0.5; // Default medium
    }
}

int AIMidiGenerator::getMoodVelocity(const std::string& mood)
{
    if (mood == "chill" || mood == "dreamy") {
        return 50; // Soft
    } else if (mood == "energetic" || mood == "frantic") {
        return 90; // Loud
    } else if (mood == "suspenseful" || mood == "ominous") {
        return 60; // Medium-low
    } else if (mood == "uplifting") {
        return 80; // Loud
    } else if (mood == "romantic") {
        return 65; // Medium
    } else if (mood == "gritty") {
        return 85; // Very loud
    } else if (mood == "focused") {
        return 70; // Medium-high
    } else {
        return 70; // Default medium-high
    }
}

float AIMidiGenerator::calculateHybridConfidence(const std::vector<std::string>& moods, const std::vector<float>& weights)
{
    if (moods.empty()) return 0.0f;
    
    // Base confidence from individual moods
    float totalConfidence = 0.0f;
    float totalWeight = 0.0f;
    
    for (size_t i = 0; i < moods.size(); ++i) {
        auto pattern = generateMoodPattern(moods[i], 1.0);
        totalConfidence += pattern.confidence * weights[i];
        totalWeight += weights[i];
    }
    
    if (totalWeight <= 0.0f) return 0.0f;
    
    float baseConfidence = totalConfidence / totalWeight;
    
    // Reduce confidence for complex combinations
    float complexityPenalty = 1.0f - (moods.size() - 1) * 0.1f;
    complexityPenalty = juce::jlimit(0.5f, 1.0f, complexityPenalty);
    
    return baseConfidence * complexityPenalty;
}

AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateDefaultPattern(double duration)
{
    GeneratedPattern pattern;
    pattern.patternType = "default";
    pattern.duration = duration;
    
    // Simple C major scale pattern
    int noteCount = static_cast<int>(duration * 4);
    double currentTime = 0.0;
    
    int scale[] = {60, 62, 64, 65, 67, 69, 71}; // C major scale
    
    for (int i = 0; i < noteCount; ++i) {
        int note = scale[i % 7];
        int velocity = 70;
        
        juce::MidiMessage noteOn = juce::MidiMessage::noteOn(0, note, static_cast<juce::uint8>(velocity));
        noteOn.setTimeStamp(currentTime);
        pattern.messages.push_back(noteOn);
        
        juce::MidiMessage noteOff = juce::MidiMessage::noteOff(0, note, static_cast<juce::uint8>(velocity));
        noteOff.setTimeStamp(currentTime + 0.5);
        pattern.messages.push_back(noteOff);
        
        currentTime += 0.5;
    }
    
    pattern.confidence = 0.7f;
    return pattern;
}

// Hybrid mood management methods
AIMidiGenerator::GeneratedPattern AIMidiGenerator::generatePredefinedHybrid(const std::string& hybridName, double duration)
{
    auto it = hybridMoods.find(hybridName);
    if (it == hybridMoods.end()) {
        return generateDefaultPattern(duration);
    }
    
    const HybridMood& hybrid = it->second;
    return generateHybridPattern(hybrid.moods, hybrid.weights, duration);
}

std::vector<std::string> AIMidiGenerator::getAvailableHybridMoods() const
{
    std::vector<std::string> availableMoods;
    for (const auto& pair : hybridMoods) {
        availableMoods.push_back(pair.first);
    }
    return availableMoods;
}

AIMidiGenerator::HybridMood AIMidiGenerator::getHybridMoodInfo(const std::string& hybridName) const
{
    auto it = hybridMoods.find(hybridName);
    if (it != hybridMoods.end()) {
        return it->second;
    }
    
    // Return default hybrid mood
    HybridMood defaultMood;
    defaultMood.moods = {"chill"};
    defaultMood.weights = {1.0f};
    defaultMood.description = "default";
    return defaultMood;
}

void AIMidiGenerator::addCustomHybridMood(const std::string& name, const HybridMood& hybridMood)
{
    hybridMoods[name] = hybridMood;
}

// Utility method for creating same-mood intensifications
AIMidiGenerator::GeneratedPattern AIMidiGenerator::generateSameMoodPattern(const std::string& mood, int repetitions, double duration)
{
    std::vector<std::string> moods(repetitions, mood);
    std::vector<float> weights(repetitions, 1.0f / repetitions); // Equal weights
    
    return generateHybridPattern(moods, weights, duration);
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
