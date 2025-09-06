#pragma once

#include <JuceHeader.h>
#include "ModelRunner.h"

class AamatiAudioProcessor : public juce::AudioProcessor
{
public:
    AamatiAudioProcessor();
    ~AamatiAudioProcessor() override;

    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;

    bool isBusesLayoutSupported(const juce::AudioProcessor::BusesLayout& layouts) const override;

    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer& midiMesssages) override;
    void processBlock(juce::AudioBuffer<double>&, juce::MidiBuffer& midiMesssages) override;

    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    const juce::String getName() const override;

    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram(int index) override;
    const juce::String getProgramName(int index) override;
    void changeProgramName(int index, const juce::String& newName) override;

    void getStateInformation(juce::MemoryBlock& destData) override;
    void setStateInformation(const void* data, int sizeInBytes) override;
    void updateFilters();

    // Parameters
    juce::AudioProcessorValueTreeState parameters;

private:
    void applyMLProcessing(juce::AudioBuffer<float>& buffer, const GrooveFeatures& features, float sensitivity);
    void applyMoodProcessing(juce::AudioBuffer<float>& buffer, const std::string& mood, float sensitivity);

    juce::dsp::ProcessorChain<
        juce::dsp::IIR::Filter<float>,  // High-pass
        juce::dsp::IIR::Filter<float>,  // Low-pass
        juce::dsp::Gain<float>         // Optional gain control
    > processorChain;

    std::unique_ptr<ModelRunner> modelRunner;
    std::unique_ptr<FeatureExtractor> featureExtractor;
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(AamatiAudioProcessor)


};