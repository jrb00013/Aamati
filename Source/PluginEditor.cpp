#include "PluginEditor.h"

AamatiAudioProcessorEditor::CustomLookAndFeel::CustomLookAndFeel()
{
    setColour(juce::Slider::thumbColourId, juce::Colour(255, 128, 0)); // Orange knob
    setColour(juce::Slider::rotarySliderFillColourId, juce::Colour(100, 100, 255)); // Blue fill
    setColour(juce::Slider::rotarySliderOutlineColourId, juce::Colours::darkgrey);
    setColour(juce::Slider::textBoxTextColourId, juce::Colours::white);
    setColour(juce::Slider::textBoxBackgroundColourId, juce::Colour(40, 40, 40));
    setColour(juce::Slider::textBoxOutlineColourId, juce::Colour(60, 60, 60));
    setColour(juce::Label::textColourId, juce::Colours::white);
}

void AamatiAudioProcessorEditor::CustomLookAndFeel::drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height,
                                                                    float sliderPosProportional, float rotaryStartAngle,
                                                                    float rotaryEndAngle, juce::Slider& slider)
{
    auto radius = juce::jmin(width / 2, height / 2) - 4.0f;
    auto centreX = x + width * 0.5f;
    auto centreY = y + height * 0.5f;
    auto rx = centreX - radius;
    auto ry = centreY - radius;
    auto rw = radius * 2.0f;
    auto angle = rotaryStartAngle + sliderPosProportional * (rotaryEndAngle - rotaryStartAngle);

    // Fill
    g.setColour(findColour(juce::Slider::rotarySliderFillColourId));
    g.fillEllipse(rx, ry, rw, rw);

    // Outline
    g.setColour(findColour(juce::Slider::rotarySliderOutlineColourId));
    g.drawEllipse(rx, ry, rw, rw, 3.0f);

    // Center cutout
    g.setColour(juce::Colour(40, 40, 40));
    g.fillEllipse(centreX - radius * 0.7f, centreY - radius * 0.7f, radius * 1.4f, radius * 1.4f);

    // Pointer
    juce::Path p;
    auto pointerLength = radius * 0.5f;
    auto pointerThickness = 3.0f;
    p.addRectangle(-pointerThickness * 0.5f, -radius, pointerThickness, pointerLength);
    p.applyTransform(juce::AffineTransform::rotation(angle).translated(centreX, centreY));
    g.setColour(findColour(juce::Slider::thumbColourId));
    g.fillPath(p);

    // Value display
    g.setColour(findColour(juce::Slider::textBoxTextColourId));
    g.setFont(juce::Font(juce::FontOptions().withHeight(14.0f).withStyle("Bold")));
    auto text = juce::String(slider.getValue(), 0) + " Hz";
    g.drawText(text, rx, ry + rw + 5, rw, 20, juce::Justification::centred);
}

AamatiAudioProcessorEditor::AamatiAudioProcessorEditor(AamatiAudioProcessor& p)
    : AudioProcessorEditor(&p), audioProcessor(p),
      highPassAttachment(std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
          audioProcessor.parameters, "highPass", highPassSlider)),
      lowPassAttachment(std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
          audioProcessor.parameters, "lowPass", lowPassSlider))
{
    setLookAndFeel(&customLookAndFeel);
    setSize(500, 400);

    // Title
    titleLabel.setText("AAMATI", juce::dontSendNotification);
    titleLabel.setFont(juce::Font(juce::FontOptions().withHeight(36.0f).withStyle("Bold")));
    titleLabel.setJustificationType(juce::Justification::centred);
    titleLabel.setColour(juce::Label::textColourId, juce::Colour(255, 128, 0));
    addAndMakeVisible(titleLabel);

    // High pass slider setup
    highPassSlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    highPassSlider.setTextBoxStyle(juce::Slider::NoTextBox, true, 0, 0);
    highPassSlider.setRange(20.0f, 5000.0f, 1.0f);
    highPassSlider.setPopupDisplayEnabled(true, false, this);
    addAndMakeVisible(highPassSlider);

    highPassLabel.setText("HIGH PASS", juce::dontSendNotification);
    highPassLabel.setFont(juce::Font(juce::FontOptions().withHeight(16.0f).withStyle("Bold")));
    highPassLabel.setJustificationType(juce::Justification::centred);
    addAndMakeVisible(highPassLabel);

    // Low pass slider setup
    lowPassSlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    lowPassSlider.setTextBoxStyle(juce::Slider::NoTextBox, true, 0, 0);
    lowPassSlider.setRange(5000.0f, 22000.0f, 1.0f);
    lowPassSlider.setPopupDisplayEnabled(true, false, this);
    addAndMakeVisible(lowPassSlider);

    lowPassLabel.setText("LOW PASS", juce::dontSendNotification);
    lowPassLabel.setFont(juce::Font(juce::FontOptions().withHeight(16.0f).withStyle("Bold")));
    lowPassLabel.setJustificationType(juce::Justification::centred);
    addAndMakeVisible(lowPassLabel);
}

AamatiAudioProcessorEditor::~AamatiAudioProcessorEditor()
{
    setLookAndFeel(nullptr);
}

void AamatiAudioProcessorEditor::paint(juce::Graphics& g)
{
    // Gradient background
    juce::ColourGradient gradient(
        juce::Colour(30, 30, 40), 0.0f, 0.0f,
        juce::Colour(10, 10, 20), 0.0f, (float)getHeight(), false);
    g.setGradientFill(gradient);
    g.fillAll();

    // Border
    g.setColour(juce::Colour(60, 60, 70));
    g.drawRect(getLocalBounds(), 2);
}

void AamatiAudioProcessorEditor::resized()
{
    auto bounds = getLocalBounds().reduced(20);
    auto topSection = bounds.removeFromTop(60);
    titleLabel.setBounds(topSection);

    auto controlArea = bounds.withSizeKeepingCentre(400, 300);
    auto highPassArea = controlArea.removeFromLeft(controlArea.getWidth() / 2).reduced(10);
    auto lowPassArea = controlArea.reduced(10);

    highPassLabel.setBounds(highPassArea.removeFromTop(30));
    highPassSlider.setBounds(highPassArea);

    lowPassLabel.setBounds(lowPassArea.removeFromTop(30));
    lowPassSlider.setBounds(lowPassArea);
}



// workin UI
// #include "PluginEditor.h"

// AamatiAudioProcessorEditor::AamatiAudioProcessorEditor(AamatiAudioProcessor& p)
//     : AudioProcessorEditor(&p), audioProcessor(p),
//       highPassAttachment(std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
//           audioProcessor.parameters, "highPass", highPassSlider)),
//       lowPassAttachment(std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
//           audioProcessor.parameters, "lowPass", lowPassSlider))
// {
//     setSize(400, 300);

//     // High pass slider setup
//     highPassSlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
//     highPassSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
//     addAndMakeVisible(highPassSlider);

//     // Low pass slider setup
//     lowPassSlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
//     lowPassSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
//     addAndMakeVisible(lowPassSlider);
// }

// AamatiAudioProcessorEditor::~AamatiAudioProcessorEditor() {}

// void AamatiAudioProcessorEditor::paint(juce::Graphics& g)
// {
//     g.fillAll(juce::Colours::black);
//     g.setColour(juce::Colours::white);
//     g.setFont(20.0f);
//     g.drawFittedText("Aamati Plugin", getLocalBounds().removeFromTop(30), juce::Justification::centred, 1);
    
//     g.setFont(15.0f);
//     g.drawText("High Pass", 40, 30, 100, 20, juce::Justification::left);
//     g.drawText("Low Pass", 40, 80, 100, 20, juce::Justification::left);
// }

// void AamatiAudioProcessorEditor::resized()
// {
//     highPassSlider.setBounds(40, 50, getWidth() - 80, 20);
//     lowPassSlider.setBounds(40, 100, getWidth() - 80, 20);
// }