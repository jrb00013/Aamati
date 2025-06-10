// #pragma once
#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"

class AamatiAudioProcessorEditor : public juce::AudioProcessorEditor
{
public:
    explicit AamatiAudioProcessorEditor(AamatiAudioProcessor& p);
    ~AamatiAudioProcessorEditor() override;

    void paint(juce::Graphics&) override;
    void resized() override;

private:
    AamatiAudioProcessor& audioProcessor;

    // Custom look and feel for knobs
    struct CustomLookAndFeel : public juce::LookAndFeel_V4
    {
        CustomLookAndFeel();
        void drawRotarySlider(juce::Graphics&, int x, int y, int width, int height,
                            float sliderPosProportional, float rotaryStartAngle,
                            float rotaryEndAngle, juce::Slider&) override;
    };

    CustomLookAndFeel customLookAndFeel;

    juce::Slider highPassSlider;
    juce::Slider lowPassSlider;
    juce::Label highPassLabel;
    juce::Label lowPassLabel;
    juce::Label titleLabel;

    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> highPassAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> lowPassAttachment;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(AamatiAudioProcessorEditor)
};


// old ui header file
// #include <JuceHeader.h>
// #include "PluginProcessor.h"

// class AamatiAudioProcessorEditor : public juce::AudioProcessorEditor
// {
// public:
//     explicit AamatiAudioProcessorEditor(AamatiAudioProcessor& p);
//     ~AamatiAudioProcessorEditor() override;

//     void paint(juce::Graphics&) override;
//     void resized() override;

// private:
//     AamatiAudioProcessor& audioProcessor;

//     juce::Slider highPassSlider;
//     juce::Slider lowPassSlider;

//     std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> highPassAttachment;
//     std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> lowPassAttachment;

//     JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(AamatiAudioProcessorEditor)
// };