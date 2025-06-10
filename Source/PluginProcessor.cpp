#include "PluginProcessor.h"
#include "PluginEditor.h"
#include "ModelRunner.h"

#include <onnxruntime/core/providers/shared_library/provider_api.h>
#include <vector>
#include <string>
#include <iostream>



// mood enum

enum class Mood {
    Calm,
    Tense,
    Explosive
};

Mood currentMood = Mood::Calm; // example current mood 


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
            juce::NormalisableRange<float>(5000.0f, 22000.0f, 0.1f, 0.3f), 12000.0f)
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
    modelRunner = std::make_unique<ModelRunner>(modelFile.getFullPathName().toStdString());

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
     // Processing usage of modelRunner
    if (modelRunner)
    {
        std::array<float, 5> features = { /* fill with your input features for the model */ };

        std::string predictedMood = modelRunner->predict(features);

        // Use predictedMood for whatever logic you want
        // print debugging 
        DBG("Predicted Mood: " << predictedMood);
    }

    juce::ScopedNoDenormals noDenormals;
    
    // Update filters if necessary
    updateFilters();
    
    // Create a dsp block for processing
    juce::dsp::AudioBlock<float> block(buffer);
    juce::dsp::ProcessContextReplacing<float> context(block);
    
    // Process the DSP chain
    processorChain.process(context);
    
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

void updateMoodFromModel(juce::AudioBuffer<float>& buffer) {
    // This is a placeholder function, you need to pass the features extracted from the audio
    // to the model and get the predicted mood (like Calm, Tense, Explosive)

    // Extract features (for example, features from your audio buffer)
    std::vector<float> features = extractGrooveFeatures(buffer);

    // Map features to input data for model prediction (you may need to preprocess the features)
    // Call the model prediction function here and set the mood accordingly
    currentMood = predictMood(features);
}





onnx::Model* MoodPredictor::model = nullptr;

onnx::Model* MoodPredictor::loadModel(const std::string& modelPath) {
    try {
        model = new onnx::Model(modelPath);
    } catch (const std::exception& e) {
        std::cerr << "Error loading model: " << e.what() << std::endl;
    }
    return model;
}

Mood MoodPredictor::predictMood(const std::vector<float>& features) {
    // Assuming you already have a way to create an ONNX session
    std::vector<onnx::Value> input = {onnx::Value::FromVector(features)};
    auto result = model->Run(input);

    // Assuming output is a classification result (0 = Calm, 1 = Tense, 2 = Explosive)
    int moodIndex = result[0].get<int>();

    // Map the result to a Mood enum
    switch (moodIndex) {
        case 0: return Mood::Calm;
        case 1: return Mood::Tense;
        case 2: return Mood::Explosive;
        default: return Mood::Calm;
    }
}
