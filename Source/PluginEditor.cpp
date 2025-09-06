#include "PluginEditor.h"

AamatiAudioProcessorEditor::CustomLookAndFeel::CustomLookAndFeel()
{
    // Aamati Theme: Black, White, Gold
    setColour(juce::Slider::thumbColourId, juce::Colour(255, 215, 0)); // Gold knob
    setColour(juce::Slider::rotarySliderFillColourId, juce::Colour(255, 215, 0)); // Gold fill
    setColour(juce::Slider::rotarySliderOutlineColourId, juce::Colour(30, 30, 30)); // Dark outline
    setColour(juce::Slider::textBoxTextColourId, juce::Colour(255, 255, 255)); // White text
    setColour(juce::Slider::textBoxBackgroundColourId, juce::Colour(20, 20, 20)); // Dark background
    setColour(juce::Slider::textBoxOutlineColourId, juce::Colour(255, 215, 0)); // Gold outline
    setColour(juce::Label::textColourId, juce::Colour(255, 255, 255)); // White text
    setColour(juce::ToggleButton::tickColourId, juce::Colour(255, 215, 0)); // Gold tick
    setColour(juce::ToggleButton::tickDisabledColourId, juce::Colour(100, 100, 100)); // Gray disabled
    setColour(juce::ToggleButton::textColourId, juce::Colour(255, 255, 255)); // White text
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

    // Outer ring (dark)
    g.setColour(juce::Colour(20, 20, 20));
    g.fillEllipse(rx - 2, ry - 2, rw + 4, rw + 4);
    
    // Main background (dark gray)
    g.setColour(juce::Colour(40, 40, 40));
    g.fillEllipse(rx, ry, rw, rw);

    // Gold arc fill
    g.setColour(findColour(juce::Slider::rotarySliderFillColourId));
    juce::Path arcPath;
    arcPath.addCentredArc(centreX, centreY, radius, radius, 0, rotaryStartAngle, angle, true);
    g.strokePath(arcPath, juce::PathStrokeType(8.0f, juce::PathStrokeType::curved, juce::PathStrokeType::rounded));

    // Inner ring (dark)
    g.setColour(juce::Colour(30, 30, 30));
    g.fillEllipse(centreX - radius * 0.8f, centreY - radius * 0.8f, radius * 1.6f, radius * 1.6f);

    // Center dot
    g.setColour(juce::Colour(60, 60, 60));
    g.fillEllipse(centreX - 3, centreY - 3, 6, 6);

    // Gold pointer
    juce::Path p;
    auto pointerLength = radius * 0.6f;
    auto pointerThickness = 4.0f;
    p.addRectangle(-pointerThickness * 0.5f, -radius + 4, pointerThickness, pointerLength);
    p.applyTransform(juce::AffineTransform::rotation(angle).translated(centreX, centreY));
    g.setColour(findColour(juce::Slider::thumbColourId));
    g.fillPath(p);

    // Glow effect on pointer
    g.setColour(juce::Colour(255, 215, 0).withAlpha(0.3f));
    g.strokePath(p, juce::PathStrokeType(6.0f));

    // Value display with enhanced styling
    g.setColour(findColour(juce::Slider::textBoxTextColourId));
    g.setFont(juce::Font(juce::FontOptions().withHeight(16.0f).withStyle("Bold")));
    auto text = juce::String(slider.getValue(), 0) + " Hz";
    auto textBounds = juce::Rectangle<int>(rx, ry + rw + 5, rw, 25);
    
    // Text background
    g.setColour(juce::Colour(20, 20, 20).withAlpha(0.8f));
    g.fillRoundedRectangle(textBounds.toFloat().expanded(4), 4.0f);
    
    // Text border
    g.setColour(findColour(juce::Slider::textBoxOutlineColourId));
    g.drawRoundedRectangle(textBounds.toFloat().expanded(4), 4.0f, 1.0f);
    
    g.drawText(text, textBounds, juce::Justification::centred);
}

AamatiAudioProcessorEditor::AamatiAudioProcessorEditor(AamatiAudioProcessor& p)
    : AudioProcessorEditor(&p), audioProcessor(p),
      highPassAttachment(std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
          audioProcessor.parameters, "highPass", highPassSlider)),
      lowPassAttachment(std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
          audioProcessor.parameters, "lowPass", lowPassSlider)),
      mlSensitivityAttachment(std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
          audioProcessor.parameters, "mlSensitivity", mlSensitivitySlider)),
      mlEnabledAttachment(std::make_unique<juce::AudioProcessorValueTreeState::ButtonAttachment>(
          audioProcessor.parameters, "mlEnabled", mlEnabledButton))
{
    setLookAndFeel(&customLookAndFeel);
    
    // Initialize advanced processing components
    emotionalOptimizer = std::make_unique<EmotionalOptimizer>();
    grooveShaper = std::make_unique<GrooveShaper>();
    aiMidiGenerator = std::make_unique<AIMidiGenerator>();
    
    // Initialize modern UI
    modernUI = std::make_unique<ModernUI>();
    addAndMakeVisible(modernUI.get());
    
    // Set up modern UI callbacks
    setupModernUICallbacks();
    
    // Set size based on UI mode
    if (useModernUI)
    {
        setSize(1200, 800);
    }
    else
    {
        setSize(600, 500);
    }

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

    // ML Sensitivity slider setup
    mlSensitivitySlider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    mlSensitivitySlider.setTextBoxStyle(juce::Slider::NoTextBox, true, 0, 0);
    mlSensitivitySlider.setRange(0.1f, 2.0f, 0.1f);
    mlSensitivitySlider.setPopupDisplayEnabled(true, false, this);
    addAndMakeVisible(mlSensitivitySlider);

    mlSensitivityLabel.setText("ML SENSITIVITY", juce::dontSendNotification);
    mlSensitivityLabel.setFont(juce::Font(juce::FontOptions().withHeight(16.0f).withStyle("Bold")));
    mlSensitivityLabel.setJustificationType(juce::Justification::centred);
    addAndMakeVisible(mlSensitivityLabel);

    // ML Enabled button setup
    mlEnabledButton.setButtonText("ML ENABLED");
    mlEnabledButton.setColour(juce::ToggleButton::textColourId, juce::Colours::white);
    mlEnabledButton.setColour(juce::ToggleButton::tickColourId, juce::Colour(255, 128, 0));
    addAndMakeVisible(mlEnabledButton);

    // Mood display label
    moodLabel.setText("MOOD: --", juce::dontSendNotification);
    moodLabel.setFont(juce::Font(juce::FontOptions().withHeight(20.0f).withStyle("Bold")));
    moodLabel.setJustificationType(juce::Justification::centred);
    moodLabel.setColour(juce::Label::textColourId, juce::Colour(100, 255, 100));
    addAndMakeVisible(moodLabel);

    // Model status label
    modelStatusLabel.setText("MODEL: LOADING...", juce::dontSendNotification);
    modelStatusLabel.setFont(juce::Font(juce::FontOptions().withHeight(14.0f)));
    modelStatusLabel.setJustificationType(juce::Justification::centred);
    modelStatusLabel.setColour(juce::Label::textColourId, juce::Colour(255, 200, 100));
    addAndMakeVisible(modelStatusLabel);

    // Features display label
    featuresLabel.setText("FEATURES: --", juce::dontSendNotification);
    featuresLabel.setFont(juce::Font(juce::FontOptions().withHeight(12.0f)));
    featuresLabel.setJustificationType(juce::Justification::centred);
    featuresLabel.setColour(juce::Label::textColourId, juce::Colour(200, 200, 200));
    addAndMakeVisible(featuresLabel);

    // Start update timer
    updateTimer.startTimer(100); // Update every 100ms
}

void AamatiAudioProcessorEditor::setupModernUICallbacks()
{
    if (!modernUI) return;
    
    // Set up feature callbacks
    modernUI->onEmotionalOptimization = [this]() {
        if (emotionalOptimizer) {
            emotionalOptimizer->setMoodProfile(currentMood, currentSecondaryMood);
        }
    };
    
    modernUI->onGrooveShaping = [this]() {
        if (grooveShaper) {
            grooveShaper->setGrooveProfile(currentMood, 0.8f);
        }
    };
    
    modernUI->onAIMidiGeneration = [this]() {
        if (aiMidiGenerator) {
            AIMidiGenerator::GenerationContext context;
            context.primaryMood = currentMood;
            context.secondaryMood = currentSecondaryMood;
            context.tempo = 120.0f; // Get from processor
            aiMidiGenerator->setGenerationContext(context);
        }
    };
    
    // Add more callbacks for other features...
}

AamatiAudioProcessorEditor::~AamatiAudioProcessorEditor()
{
    updateTimer.stopTimer();
    setLookAndFeel(nullptr);
}

void AamatiAudioProcessorEditor::timerCallback()
{
    // Update model status
    if (audioProcessor.modelRunner && audioProcessor.modelRunner->isModelLoaded())
    {
        modelStatusLabel.setText("MODEL: LOADED", juce::dontSendNotification);
        modelStatusLabel.setColour(juce::Label::textColourId, juce::Colour(100, 255, 100));
    }
    else
    {
        modelStatusLabel.setText("MODEL: NOT LOADED", juce::dontSendNotification);
        modelStatusLabel.setColour(juce::Label::textColourId, juce::Colour(255, 100, 100));
    }
    
    // Update mood display
    if (audioProcessor.currentMood != currentMood)
    {
        currentMood = audioProcessor.currentMood;
        moodLabel.setText("MOOD: " + currentMood, juce::dontSendNotification);
        
        // Update modern UI if available
        if (modernUI)
        {
            ModernUI::MoodDisplay moodDisplay;
            moodDisplay.primaryMood = currentMood;
            moodDisplay.secondaryMood = currentSecondaryMood;
            moodDisplay.confidence = currentConfidence;
            moodDisplay.tags = {"analyzing", "processing"};
            moodDisplay.analysis = "Real-time analysis active";
            
            modernUI->updateMoodDisplay(moodDisplay);
        }
    }
    else
    {
        moodLabel.setText("MOOD: ANALYZING...", juce::dontSendNotification);
    }
    
    // Update features display
    if (audioProcessor.featureExtractor)
    {
        auto features = audioProcessor.featureExtractor->getLastFeatures();
        if (features)
        {
            juce::String featuresText = "TEMPO: " + juce::String(features->tempo, 1) + 
                                      " | SWING: " + juce::String(features->swing, 2) +
                                      " | DENSITY: " + juce::String(features->density, 1);
            featuresLabel.setText(featuresText, juce::dontSendNotification);
        }
    }
    else
    {
        featuresLabel.setText("FEATURES: EXTRACTING...", juce::dontSendNotification);
    }
}

void AamatiAudioProcessorEditor::paint(juce::Graphics& g)
{
    // Stunning Aamati gradient background
    juce::ColourGradient gradient(
        juce::Colour(15, 15, 25), 0.0f, 0.0f,
        juce::Colour(5, 5, 10), 0.0f, (float)getHeight(), false);
    g.setGradientFill(gradient);
    g.fillAll();

    // Gold accent border
    g.setColour(juce::Colour(255, 215, 0));
    g.drawRect(getLocalBounds(), 3);
    
    // Inner dark border
    g.setColour(juce::Colour(30, 30, 30));
    g.drawRect(getLocalBounds().reduced(3), 1);
    
    // Decorative corner accents
    auto bounds = getLocalBounds();
    auto cornerSize = 20;
    
    // Top-left corner
    g.setColour(juce::Colour(255, 215, 0).withAlpha(0.3f));
    g.fillEllipse(0, 0, cornerSize * 2, cornerSize * 2);
    
    // Top-right corner
    g.fillEllipse(bounds.getWidth() - cornerSize * 2, 0, cornerSize * 2, cornerSize * 2);
    
    // Bottom-left corner
    g.fillEllipse(0, bounds.getHeight() - cornerSize * 2, cornerSize * 2, cornerSize * 2);
    
    // Bottom-right corner
    g.fillEllipse(bounds.getWidth() - cornerSize * 2, bounds.getHeight() - cornerSize * 2, cornerSize * 2, cornerSize * 2);
    
    // Subtle grid pattern
    g.setColour(juce::Colour(255, 215, 0).withAlpha(0.05f));
    for (int x = 0; x < bounds.getWidth(); x += 40)
    {
        g.drawVerticalLine(x, 0, bounds.getHeight());
    }
    for (int y = 0; y < bounds.getHeight(); y += 40)
    {
        g.drawHorizontalLine(y, 0, bounds.getWidth());
    }
}

void AamatiAudioProcessorEditor::resized()
{
    if (useModernUI && modernUI)
    {
        // Use modern UI layout
        modernUI->setBounds(getLocalBounds());
    }
    else
    {
        // Use classic UI layout
        auto bounds = getLocalBounds().reduced(20);
        
        // Title section
        auto titleSection = bounds.removeFromTop(60);
        titleLabel.setBounds(titleSection);
        
        // Status section
        auto statusSection = bounds.removeFromTop(80);
        auto moodArea = statusSection.removeFromTop(30);
        moodLabel.setBounds(moodArea);
        
        auto modelArea = statusSection.removeFromTop(25);
        modelStatusLabel.setBounds(modelArea);
        
        auto featuresArea = statusSection.removeFromTop(25);
        featuresLabel.setBounds(featuresArea);
        
        // Control section
        auto controlArea = bounds.withSizeKeepingCentre(500, 300);
        
        // Top row: High Pass and Low Pass
        auto topRow = controlArea.removeFromTop(150);
        auto highPassArea = topRow.removeFromLeft(topRow.getWidth() / 2).reduced(10);
        auto lowPassArea = topRow.reduced(10);
        
        highPassLabel.setBounds(highPassArea.removeFromTop(30));
        highPassSlider.setBounds(highPassArea);
        
        lowPassLabel.setBounds(lowPassArea.removeFromTop(30));
        lowPassSlider.setBounds(lowPassArea);
        
        // Bottom row: ML Sensitivity and ML Enabled
        auto bottomRow = controlArea.removeFromTop(150);
        auto mlSensitivityArea = bottomRow.removeFromLeft(bottomRow.getWidth() / 2).reduced(10);
        auto mlEnabledArea = bottomRow.reduced(10);
        
        mlSensitivityLabel.setBounds(mlSensitivityArea.removeFromTop(30));
        mlSensitivitySlider.setBounds(mlSensitivityArea);
        
        mlEnabledButton.setBounds(mlEnabledArea.removeFromTop(50).reduced(20));
    }
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