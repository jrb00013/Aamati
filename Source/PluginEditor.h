"// #pragma once
#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"
#include "ModernUI.h"
#include "EmotionalOptimizer.h"
#include "GrooveShaper.h"
#include "AIMidiGenerator.h"

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
    juce::Slider mlSensitivitySlider;
    juce::ToggleButton mlEnabledButton;
    
    juce::Label highPassLabel;
    juce::Label lowPassLabel;
    juce::Label mlSensitivityLabel;
    juce::Label titleLabel;
    juce::Label moodLabel;
    juce::Label modelStatusLabel;
    juce::Label featuresLabel;

    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> highPassAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> lowPassAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> mlSensitivityAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::ButtonAttachment> mlEnabledAttachment;
    
    // Timer for updating UI
    juce::Timer updateTimer;
    void timerCallback() override;
    
    // Advanced UI Components
    juce::TextButton uploadMidiButton;
    juce::TextButton downloadReportButton;
    juce::ComboBox featureSelector;
    juce::ComboBox presetSelector;
    
    // Mood Display Components
    juce::Label primaryMoodLabel;
    juce::Label secondaryMoodLabel;
    juce::Label moodConfidenceLabel;
    juce::Label moodTagsLabel;
    
    // Feature Buttons
    juce::TextButton emotionalOptButton;
    juce::TextButton grooveShapeButton;
    juce::TextButton instrumentationButton;
    juce::TextButton melodicContourButton;
    juce::TextButton harmonicDensityButton;
    juce::TextButton fillOrnamentButton;
    juce::TextButton aiMidiGenButton;
    juce::TextButton keyTempoDetectButton;
    juce::TextButton visualAnalyzerButton;
    juce::TextButton moodRemixerButton;
    juce::TextButton masteringToolsButton;
    juce::TextButton grooveHumanizerButton;
    juce::TextButton dynamicBalancerButton;
    
    // Feature Panels
    juce::Component emotionalOptPanel;
    juce::Component grooveShapePanel;
    juce::Component instrumentationPanel;
    juce::Component melodicContourPanel;
    juce::Component harmonicDensityPanel;
    juce::Component fillOrnamentPanel;
    juce::Component aiMidiGenPanel;
    juce::Component keyTempoDetectPanel;
    juce::Component visualAnalyzerPanel;
    juce::Component moodRemixerPanel;
    juce::Component masteringToolsPanel;
    juce::Component grooveHumanizerPanel;
    juce::Component dynamicBalancerPanel;
    
    // Current active panel
    juce::Component* activePanel = nullptr;
    
    // UI State
    bool showAdvancedFeatures = false;
    std::string currentMood = "unknown";
    std::string currentSecondaryMood = "unknown";
    float currentConfidence = 0.0f;
    
    // Custom look and feel
    class AamatiLookAndFeel : public juce::LookAndFeel_V4
    {
    public:
        AamatiLookAndFeel();
        void drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height,
                            float sliderPos, float rotaryStartAngle, float rotaryEndAngle,
                            juce::Slider& slider) override;
        void drawButtonBackground(juce::Graphics& g, juce::Button& button,
                                const juce::Colour& backgroundColour,
                                bool shouldDrawButtonAsHighlighted,
                                bool shouldDrawButtonAsDown) override;
        void drawLabel(juce::Graphics& g, juce::Label& label) override;
        juce::Font getLabelFont(juce::Label& label) override;
        void drawLinearSlider(juce::Graphics& g, int x, int y, int width, int height,
                            float sliderPos, float minSliderPos, float maxSliderPos,
                            const juce::Slider::SliderStyle style, juce::Slider& slider) override;
    };
    
    AamatiLookAndFeel aamatiLookAndFeel;

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