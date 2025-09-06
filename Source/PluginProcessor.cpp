#include "PluginProcessor.h"
#include "PluginEditor.h"
#include "ModelRunner.h"
#include "FeatureExtractor.h"

#include <onnxruntime/core/providers/shared_library/provider_api.h>
#include <vector>
#include <string>
#include <iostream>

// Mood enum
enum class Mood {
    Calm,
    Tense,
    Explosive,
    Chill,
    Energetic,
    Suspenseful,
    Uplifting,
    Ominous,
    Romantic,
    Gritty,
    Dreamy,
    Frantic,
    Focused
};

Mood currentMood = Mood::Calm;

AamatiAudioProcessor::AamatiAudioProcessor()
    : AudioProcessor(BusesProperties()
        .withInput("Input", juce::AudioChannelSet::stereo(), true)
        .withOutput("Output", juce::AudioChannelSet::stereo(), true)),
    parameters(*this, nullptr, "Parameters", {
        std::make_unique<juce::AudioParameterFloat>(
            "highPass", "High Pass Frequency",
            juce::NormalisableRange<float>(20.0f, 5000.0f, 0.1f, 0.3f), 200.0f),
        std::make_unique<juce::AudioParameterFloat>(
            "lowPass", "Low Pass Frequency",
            juce::NormalisableRange<float>(5000.0f, 22000.0f, 0.1f, 0.3f), 12000.0f),
        std::make_unique<juce::AudioParameterBool>(
            "mlEnabled", "ML Processing Enabled", true),
        std::make_unique<juce::AudioParameterFloat>(
            "mlSensitivity", "ML Sensitivity",
            juce::NormalisableRange<float>(0.1f, 2.0f, 0.1f), 1.0f)
    })
{
}

AamatiAudioProcessor::~AamatiAudioProcessor() {}

const juce::String AamatiAudioProcessor::getName() const {
    return JucePlugin_Name;
}

bool AamatiAudioProcessor::acceptsMidi() const { return false; }
bool AamatiAudioProcessor::producesMidi() const { return false; }
bool AamatiAudioProcessor::isMidiEffect() const { return false; }
double AamatiAudioProcessor::getTailLengthSeconds() const { return 0.0; }

int AamatiAudioProcessor::getNumPrograms() { return 1; }
int AamatiAudioProcessor::getCurrentProgram() { return 0; }
void AamatiAudioProcessor::setCurrentProgram(int) {}
const juce::String AamatiAudioProcessor::getProgramName(int) { return {}; }
void AamatiAudioProcessor::changeProgramName(int, const juce::String&) {}

void AamatiAudioProcessor::prepareToPlay(double sampleRate, int samplesPerBlock)
{
    juce::ignoreUnused(sampleRate, samplesPerBlock);

    // Find executable directory
    auto exeDir = juce::File::getSpecialLocation(juce::File::currentExecutableFile).getParentDirectory();

    // Construct full path to your model inside Resources folder
    auto modelFile = exeDir.getChildFile("Resources/groove_mood_model.onnx");

    // Create ModelRunner instance
    if (modelFile.exists())
    {
        modelRunner = std::make_unique<ModelRunner>(modelFile.getFullPathName().toStdString());
        DBG("ML Model loaded successfully");
    }
    else
    {
        DBG("ML Model file not found: " << modelFile.getFullPathName());
    }

    // Initialize feature extractor
    featureExtractor = std::make_unique<FeatureExtractor>();

    juce::dsp::ProcessSpec spec;
    spec.sampleRate = sampleRate;
    spec.maximumBlockSize = static_cast<juce::uint32>(samplesPerBlock);
    spec.numChannels = static_cast<juce::uint32>(getTotalNumOutputChannels());

    processorChain.prepare(spec);
    
    updateFilters();
}

void AamatiAudioProcessor::updateFilters()
{
    auto highPassFreq = parameters.getRawParameterValue("highPass")->load();
    auto lowPassFreq = parameters.getRawParameterValue("lowPass")->load();
    
    // Update high-pass filter
    *processorChain.get<0>().coefficients = *juce::dsp::IIR::Coefficients<float>::makeHighPass(
        getSampleRate(), highPassFreq);
    
    // Update low-pass filter
    *processorChain.get<1>().coefficients = *juce::dsp::IIR::Coefficients<float>::makeLowPass(
        getSampleRate(), lowPassFreq);
}

void AamatiAudioProcessor::releaseResources() {}

bool AamatiAudioProcessor::isBusesLayoutSupported(const juce::AudioProcessor::BusesLayout& layouts) const {
    return layouts.getMainInputChannelSet() == juce::AudioChannelSet::stereo()
        && layouts.getMainOutputChannelSet() == juce::AudioChannelSet::stereo();
}


void AamatiAudioProcessor::processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    juce::ScopedNoDenormals noDenormals;
    
    // Update filters if necessary
    updateFilters();
    
    // Create a dsp block for processing
    juce::dsp::AudioBlock<float> block(buffer);
    juce::dsp::ProcessContextReplacing<float> context(block);
    
    // Process the DSP chain
    processorChain.process(context);
    
    // ML Processing
    bool mlEnabled = parameters.getRawParameterValue("mlEnabled")->load() > 0.5f;
    if (mlEnabled && modelRunner && featureExtractor)
    {
        // Extract features from current audio buffer
        auto features = featureExtractor->extractFeaturesFromAudio(buffer, getSampleRate());
        
        if (features.has_value())
        {
            // Get ML sensitivity parameter
            float sensitivity = parameters.getRawParameterValue("mlSensitivity")->load();
            
            // Apply ML-based processing
            applyMLProcessing(buffer, features.value(), sensitivity);
        }
    }
    
    // Mid/Side processing
    for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
    {
        // Get left and right channel samples
        float left = buffer.getSample(0, sample);
        float right = buffer.getSample(1, sample);
        
        // Compute mid and side components
        float mid = (left + right) * 0.5f;
        float side = (left - right) * 0.5f;
        
        // Reduce mid component to alter the stereo image
        mid *= 0.5f;
        
        // Reassign mid and side back to the left and right channels
        buffer.setSample(0, sample, mid + side); // Left channel
        buffer.setSample(1, sample, mid - side); // Right channel
    }

    // Midi messages are ignored for now
    (void)midiMessages;
}

void AamatiAudioProcessor::processBlock(juce::AudioBuffer<double>& buffer, juce::MidiBuffer& midiMessages)
{
    // You can ignore processing if your plugin does not support double-precision processing
    juce::ignoreUnused(buffer, midiMessages);
}

bool AamatiAudioProcessor::hasEditor() const { return true; }

juce::AudioProcessorEditor* AamatiAudioProcessor::createEditor() {
    return new AamatiAudioProcessorEditor(*this);
}

void AamatiAudioProcessor::getStateInformation(juce::MemoryBlock& destData) {
    auto state = parameters.copyState();
    std::unique_ptr<juce::XmlElement> xml(state.createXml());
    copyXmlToBinary(*xml, destData);
}

void AamatiAudioProcessor::setStateInformation(const void* data, int sizeInBytes) {
    std::unique_ptr<juce::XmlElement> xmlState(getXmlFromBinary(data, sizeInBytes));
    if (xmlState.get() != nullptr) {
        parameters.replaceState(juce::ValueTree::fromXml(*xmlState));
        updateFilters(); // Apply the loaded parameters
    }
}

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new AamatiAudioProcessor();
}

void AamatiAudioProcessor::applyMLProcessing(juce::AudioBuffer<float>& buffer, const GrooveFeatures& features, float sensitivity)
{
    // Convert features to array format expected by model
    std::array<float, 5> featureArray = {
        static_cast<float>(features.tempo),
        static_cast<float>(features.swing),
        static_cast<float>(features.density),
        static_cast<float>(features.dynamicRange),
        static_cast<float>(features.energy)
    };

    // Get mood prediction
    std::string predictedMood = modelRunner->predict(featureArray);
    
    // Apply mood-based processing
    applyMoodProcessing(buffer, predictedMood, sensitivity);
    
    // Debug output
    DBG("Predicted Mood: " << predictedMood);
}

void AamatiAudioProcessor::applyMoodProcessing(juce::AudioBuffer<float>& buffer, const std::string& mood, float sensitivity)
{
    // Apply different processing based on predicted mood
    if (mood == "energetic" || mood == "frantic")
    {
        // Add brightness and punch
        for (int channel = 0; channel < buffer.getNumChannels(); ++channel)
        {
            for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
            {
                float sampleValue = buffer.getSample(channel, sample);
                // Apply slight saturation and high-frequency emphasis
                sampleValue = juce::jlimit(-1.0f, 1.0f, sampleValue * (1.0f + sensitivity * 0.1f));
                buffer.setSample(channel, sample, sampleValue);
            }
        }
    }
    else if (mood == "chill" || mood == "dreamy")
    {
        // Apply gentle filtering and reverb-like processing
        for (int channel = 0; channel < buffer.getNumChannels(); ++channel)
        {
            for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
            {
                float sampleValue = buffer.getSample(channel, sample);
                // Apply gentle low-pass filtering effect
                sampleValue *= (1.0f - sensitivity * 0.05f);
                buffer.setSample(channel, sample, sampleValue);
            }
        }
    }
    else if (mood == "ominous" || mood == "suspenseful")
    {
        // Add dark character with low-end emphasis
        for (int channel = 0; channel < buffer.getNumChannels(); ++channel)
        {
            for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
            {
                float sampleValue = buffer.getSample(channel, sample);
                // Apply slight low-frequency emphasis
                sampleValue *= (1.0f + sensitivity * 0.05f);
                buffer.setSample(channel, sample, sampleValue);
            }
        }
    }
}
