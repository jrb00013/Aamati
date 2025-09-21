#include "ModernUI.h"

ModernUI::ModernUI()
{
    setupUI();
}

ModernUI::~ModernUI()
{
}

void ModernUI::setupUI()
{
    // Set up main layout
    setSize(1200, 800);
    
    // Create header panel
    headerPanel.setBounds(0, 0, getWidth(), 80);
    addAndMakeVisible(headerPanel);
    
    // Create mood panel
    moodPanel.setBounds(0, 80, getWidth(), 120);
    addAndMakeVisible(moodPanel);
    
    // Create feature panel
    featurePanel.setBounds(0, 200, getWidth(), 400);
    addAndMakeVisible(featurePanel);
    
    // Create control panel
    controlPanel.setBounds(0, 600, getWidth(), 100);
    addAndMakeVisible(controlPanel);
    
    // Create status panel
    statusPanel.setBounds(0, 700, getWidth(), 100);
    addAndMakeVisible(statusPanel);
    
    // Setup header components
    titleLabel.setText("AAMATI", juce::dontSendNotification);
    titleLabel.setFont(style.titleFont);
    titleLabel.setJustificationType(juce::Justification::centred);
    titleLabel.setColour(juce::Label::textColourId, style.primary);
    headerPanel.addAndMakeVisible(titleLabel);
    
    uploadButton.setButtonText("Upload MIDI");
    uploadButton.setColour(juce::TextButton::buttonColourId, style.surface);
    uploadButton.setColour(juce::TextButton::textColourOnId, style.primary);
    uploadButton.setColour(juce::TextButton::textColourOffId, style.secondary);
    uploadButton.onClick = [this] { onUploadMIDI(); };
    headerPanel.addAndMakeVisible(uploadButton);
    
    downloadButton.setButtonText("Download Report");
    downloadButton.setColour(juce::TextButton::buttonColourId, style.surface);
    downloadButton.setColour(juce::TextButton::textColourOnId, style.primary);
    downloadButton.setColour(juce::TextButton::textColourOffId, style.secondary);
    downloadButton.onClick = [this] { onDownloadReport(); };
    headerPanel.addAndMakeVisible(downloadButton);
    
    settingsButton.setButtonText("Settings");
    settingsButton.setColour(juce::TextButton::buttonColourId, style.surface);
    settingsButton.setColour(juce::TextButton::textColourOnId, style.primary);
    settingsButton.setColour(juce::TextButton::textColourOffId, style.secondary);
    headerPanel.addAndMakeVisible(settingsButton);
    
    // Setup mood display components
    moodTitleLabel.setText("Mood Analysis", juce::dontSendNotification);
    moodTitleLabel.setFont(style.bodyFont.boldened());
    moodTitleLabel.setJustificationType(juce::Justification::centred);
    moodTitleLabel.setColour(juce::Label::textColourId, style.secondary);
    moodPanel.addAndMakeVisible(moodTitleLabel);
    
    primaryMoodLabel.setText("Primary: Unknown", juce::dontSendNotification);
    primaryMoodLabel.setFont(style.bodyFont);
    primaryMoodLabel.setJustificationType(juce::Justification::centred);
    primaryMoodLabel.setColour(juce::Label::textColourId, style.primary);
    moodPanel.addAndMakeVisible(primaryMoodLabel);
    
    secondaryMoodLabel.setText("Secondary: Unknown", juce::dontSendNotification);
    secondaryMoodLabel.setFont(style.bodyFont);
    secondaryMoodLabel.setJustificationType(juce::Justification::centred);
    secondaryMoodLabel.setColour(juce::Label::textColourId, style.secondary);
    moodPanel.addAndMakeVisible(secondaryMoodLabel);
    
    confidenceLabel.setText("Confidence: 0%", juce::dontSendNotification);
    confidenceLabel.setFont(style.smallFont);
    confidenceLabel.setJustificationType(juce::Justification::centred);
    confidenceLabel.setColour(juce::Label::textColourId, style.secondary);
    moodPanel.addAndMakeVisible(confidenceLabel);
    
    tagsLabel.setText("Tags: Analyzing...", juce::dontSendNotification);
    tagsLabel.setFont(style.smallFont);
    tagsLabel.setJustificationType(juce::Justification::centred);
    tagsLabel.setColour(juce::Label::textColourId, style.secondary);
    moodPanel.addAndMakeVisible(tagsLabel);
    
    analysisLabel.setText("Analysis: Ready", juce::dontSendNotification);
    analysisLabel.setFont(style.smallFont);
    analysisLabel.setJustificationType(juce::Justification::centred);
    analysisLabel.setColour(juce::Label::textColourId, style.secondary);
    moodPanel.addAndMakeVisible(analysisLabel);
    
    moodProgressBar.setPercentage(0.0);
    moodPanel.addAndMakeVisible(moodProgressBar);
    
    // Create feature buttons and panels
    createFeatureButtons();
    createFeaturePanels();
}

void ModernUI::createFeatureButtons()
{
    // Define feature buttons
    std::vector<std::pair<std::string, std::string>> features = {
        {"Emotional Optimization", "Adjust MIDI for emotional impact"},
        {"Groove Shaping", "Make rhythm feel more human"},
        {"Instrumentation", "Guide instrument selection"},
        {"Melodic Contour", "Adapt melodies to mood"},
        {"Harmonic Density", "Control chord richness"},
        {"Fill & Ornament", "Auto-generate articulations"},
        {"AI MIDI Generation", "Generate new MIDI content"},
        {"Key/Tempo Detection", "Real-time analysis"},
        {"Visual Analyzer", "AI-driven visualization"},
        {"Mood Remixer", "Transform based on mood"},
        {"Mastering Tools", "AI-driven mastering"},
        {"Groove Humanizer", "Add human feel"},
        {"Dynamic Balancer", "Balance energy levels"}
    };
    
    featureButtons.clear();
    
    for (size_t i = 0; i < features.size(); ++i)
    {
        FeatureButton fb;
        fb.name = features[i].first;
        fb.description = features[i].second;
        fb.button.setButtonText(fb.name);
        fb.button.setColour(juce::TextButton::buttonColourId, style.surface);
        fb.button.setColour(juce::TextButton::textColourOnId, style.primary);
        fb.button.setColour(juce::TextButton::textColourOffId, style.secondary);
        
        // Assign colors based on feature type
        if (i < 6) fb.color = style.primary; // Core features
        else if (i < 9) fb.color = style.accent; // AI features
        else fb.color = style.success; // Advanced features
        
        fb.button.onClick = [this, name = fb.name] { showFeaturePanel(name); };
        featurePanel.addAndMakeVisible(fb.button);
        featureButtons.push_back(fb);
    }
}

void ModernUI::createFeaturePanels()
{
    // Create all feature panels
    createEmotionalOptimizationPanel();
    createGrooveShapingPanel();
    createInstrumentationPanel();
    createMelodicContourPanel();
    createHarmonicDensityPanel();
    createFillOrnamentPanel();
    createAIMidiGenerationPanel();
    createKeyTempoDetectionPanel();
    createVisualAnalysisPanel();
    createMoodRemixingPanel();
    createMasteringToolsPanel();
    createGrooveHumanizationPanel();
    createDynamicBalancingPanel();
}

void ModernUI::createEmotionalOptimizationPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Emotional Optimization");
    
    // Energy control
    auto* energySlider = new juce::Slider();
    energySlider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    energySlider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    energySlider->setRange(0.0, 1.0, 0.01);
    energySlider->setValue(0.5);
    energySlider->setColour(juce::Slider::rotarySliderFillColourId, style.primary);
    energySlider->setColour(juce::Slider::rotarySliderOutlineColourId, style.surface);
    energySlider->setColour(juce::Slider::thumbColourId, style.accent);
    panel->addAndMakeVisible(energySlider);
    
    auto* energyLabel = new juce::Label();
    energyLabel->setText("Energy", juce::dontSendNotification);
    energyLabel->setFont(style.bodyFont);
    energyLabel->setColour(juce::Label::textColourId, style.secondary);
    energyLabel->attachToComponent(energySlider, false);
    panel->addAndMakeVisible(energyLabel);
    
    // Tension control
    auto* tensionSlider = new juce::Slider();
    tensionSlider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    tensionSlider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    tensionSlider->setRange(0.0, 1.0, 0.01);
    tensionSlider->setValue(0.5);
    tensionSlider->setColour(juce::Slider::rotarySliderFillColourId, style.primary);
    tensionSlider->setColour(juce::Slider::rotarySliderOutlineColourId, style.surface);
    tensionSlider->setColour(juce::Slider::thumbColourId, style.accent);
    panel->addAndMakeVisible(tensionSlider);
    
    auto* tensionLabel = new juce::Label();
    tensionLabel->setText("Tension", juce::dontSendNotification);
    tensionLabel->setFont(style.bodyFont);
    tensionLabel->setColour(juce::Label::textColourId, style.secondary);
    tensionLabel->attachToComponent(tensionSlider, false);
    panel->addAndMakeVisible(tensionLabel);
    
    // Warmth control
    auto* warmthSlider = new juce::Slider();
    warmthSlider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    warmthSlider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    warmthSlider->setRange(0.0, 1.0, 0.01);
    warmthSlider->setValue(0.5);
    warmthSlider->setColour(juce::Slider::rotarySliderFillColourId, style.primary);
    warmthSlider->setColour(juce::Slider::rotarySliderOutlineColourId, style.surface);
    warmthSlider->setColour(juce::Slider::thumbColourId, style.accent);
    panel->addAndMakeVisible(warmthSlider);
    
    auto* warmthLabel = new juce::Label();
    warmthLabel->setText("Warmth", juce::dontSendNotification);
    warmthLabel->setFont(style.bodyFont);
    warmthLabel->setColour(juce::Label::textColourId, style.secondary);
    warmthLabel->attachToComponent(warmthSlider, false);
    panel->addAndMakeVisible(warmthLabel);
    
    // Apply button
    auto* applyButton = new juce::TextButton();
    applyButton->setButtonText("Apply Emotional Optimization");
    applyButton->setColour(juce::TextButton::buttonColourId, style.accent);
    applyButton->setColour(juce::TextButton::textColourOnId, juce::Colours::white);
    applyButton->setColour(juce::TextButton::textColourOffId, style.secondary);
    panel->addAndMakeVisible(applyButton);
    
    // Layout controls
    auto bounds = panel->getLocalBounds().reduced(20);
    auto sliderSize = 120;
    auto spacing = 20;
    
    energySlider->setBounds(bounds.removeFromLeft(sliderSize));
    bounds.removeFromLeft(spacing);
    tensionSlider->setBounds(bounds.removeFromLeft(sliderSize));
    bounds.removeFromLeft(spacing);
    warmthSlider->setBounds(bounds.removeFromLeft(sliderSize));
    
    applyButton->setBounds(bounds.removeFromTop(40).reduced(10));
    
    featurePanels["Emotional Optimization"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createGrooveShapingPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Groove Shaping");
    
    // Humanization control
    auto* humanizationSlider = new juce::Slider();
    humanizationSlider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    humanizationSlider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    humanizationSlider->setRange(0.0, 1.0, 0.01);
    humanizationSlider->setValue(0.5);
    humanizationSlider->setColour(juce::Slider::rotarySliderFillColourId, style.primary);
    humanizationSlider->setColour(juce::Slider::rotarySliderOutlineColourId, style.surface);
    humanizationSlider->setColour(juce::Slider::thumbColourId, style.accent);
    panel->addAndMakeVisible(humanizationSlider);
    
    auto* humanizationLabel = new juce::Label();
    humanizationLabel->setText("Humanization", juce::dontSendNotification);
    humanizationLabel->setFont(style.bodyFont);
    humanizationLabel->setColour(juce::Label::textColourId, style.secondary);
    humanizationLabel->attachToComponent(humanizationSlider, false);
    panel->addAndMakeVisible(humanizationLabel);
    
    // Swing amount control
    auto* swingSlider = new juce::Slider();
    swingSlider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    swingSlider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    swingSlider->setRange(0.0, 1.0, 0.01);
    swingSlider->setValue(0.3);
    swingSlider->setColour(juce::Slider::rotarySliderFillColourId, style.primary);
    swingSlider->setColour(juce::Slider::rotarySliderOutlineColourId, style.surface);
    swingSlider->setColour(juce::Slider::thumbColourId, style.accent);
    panel->addAndMakeVisible(swingSlider);
    
    auto* swingLabel = new juce::Label();
    swingLabel->setText("Swing Amount", juce::dontSendNotification);
    swingLabel->setFont(style.bodyFont);
    swingLabel->setColour(juce::Label::textColourId, style.secondary);
    swingLabel->attachToComponent(swingSlider, false);
    panel->addAndMakeVisible(swingLabel);
    
    // Velocity variation control
    auto* velocitySlider = new juce::Slider();
    velocitySlider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    velocitySlider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    velocitySlider->setRange(0.0, 1.0, 0.01);
    velocitySlider->setValue(0.4);
    velocitySlider->setColour(juce::Slider::rotarySliderFillColourId, style.primary);
    velocitySlider->setColour(juce::Slider::rotarySliderOutlineColourId, style.surface);
    velocitySlider->setColour(juce::Slider::thumbColourId, style.accent);
    panel->addAndMakeVisible(velocitySlider);
    
    auto* velocityLabel = new juce::Label();
    velocityLabel->setText("Velocity Variation", juce::dontSendNotification);
    velocityLabel->setFont(style.bodyFont);
    velocityLabel->setColour(juce::Label::textColourId, style.secondary);
    velocityLabel->attachToComponent(velocitySlider, false);
    panel->addAndMakeVisible(velocityLabel);
    
    // Apply groove button
    auto* applyGrooveButton = new juce::TextButton();
    applyGrooveButton->setButtonText("Apply Groove Shaping");
    applyGrooveButton->setColour(juce::TextButton::buttonColourId, style.accent);
    applyGrooveButton->setColour(juce::TextButton::textColourOnId, juce::Colours::white);
    applyGrooveButton->setColour(juce::TextButton::textColourOffId, style.secondary);
    panel->addAndMakeVisible(applyGrooveButton);
    
    // Layout controls
    auto bounds = panel->getLocalBounds().reduced(20);
    auto sliderSize = 120;
    auto spacing = 20;
    
    humanizationSlider->setBounds(bounds.removeFromLeft(sliderSize));
    bounds.removeFromLeft(spacing);
    swingSlider->setBounds(bounds.removeFromLeft(sliderSize));
    bounds.removeFromLeft(spacing);
    velocitySlider->setBounds(bounds.removeFromLeft(sliderSize));
    
    applyGrooveButton->setBounds(bounds.removeFromTop(40).reduced(10));
    
    featurePanels["Groove Shaping"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createInstrumentationPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Instrumentation");
    
    // Add instrument selection controls
    auto* instrumentCombo = new juce::ComboBox();
    instrumentCombo->addItem("Piano", 1);
    instrumentCombo->addItem("Strings", 2);
    instrumentCombo->addItem("Brass", 3);
    instrumentCombo->addItem("Synth", 4);
    instrumentCombo->setSelectedId(1);
    panel->addAndMakeVisible(instrumentCombo);
    
    auto* instrumentLabel = new juce::Label();
    instrumentLabel->setText("Instrument", juce::dontSendNotification);
    instrumentLabel->attachToComponent(instrumentCombo, false);
    panel->addAndMakeVisible(instrumentLabel);
    
    featurePanels["Instrumentation"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createMelodicContourPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Melodic Contour");
    
    // Add melodic contour controls
    auto* contourSlider = new juce::Slider();
    contourSlider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    contourSlider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    contourSlider->setRange(0.0, 1.0, 0.01);
    contourSlider->setValue(0.5);
    panel->addAndMakeVisible(contourSlider);
    
    auto* contourLabel = new juce::Label();
    contourLabel->setText("Contour", juce::dontSendNotification);
    contourLabel->attachToComponent(contourSlider, false);
    panel->addAndMakeVisible(contourLabel);
    
    featurePanels["Melodic Contour"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createHarmonicDensityPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Harmonic Density");
    
    // Add harmonic density controls
    auto* densitySlider = new juce::Slider();
    densitySlider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    densitySlider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    densitySlider->setRange(0.0, 1.0, 0.01);
    densitySlider->setValue(0.5);
    panel->addAndMakeVisible(densitySlider);
    
    auto* densityLabel = new juce::Label();
    densityLabel->setText("Density", juce::dontSendNotification);
    densityLabel->attachToComponent(densitySlider, false);
    panel->addAndMakeVisible(densityLabel);
    
    featurePanels["Harmonic Density"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createFillOrnamentPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Fill & Ornament");
    
    // Add fill and ornament controls
    auto* fillSlider = new juce::Slider();
    fillSlider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    fillSlider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    fillSlider->setRange(0.0, 1.0, 0.01);
    fillSlider->setValue(0.5);
    panel->addAndMakeVisible(fillSlider);
    
    auto* fillLabel = new juce::Label();
    fillLabel->setText("Fill Amount", juce::dontSendNotification);
    fillLabel->attachToComponent(fillSlider, false);
    panel->addAndMakeVisible(fillLabel);
    
    featurePanels["Fill & Ornament"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createAIMidiGenerationPanel()
{
    auto* panel = new juce::Component();
    panel->setName("AI MIDI Generation");
    
    // Add AI MIDI generation controls
    auto* generateButton = new juce::TextButton();
    generateButton->setButtonText("Generate MIDI");
    generateButton->setColour(juce::TextButton::buttonColourId, style.accent);
    generateButton->setColour(juce::TextButton::textColourOnId, juce::Colours::white);
    panel->addAndMakeVisible(generateButton);
    
    auto* lengthSlider = new juce::Slider();
    lengthSlider->setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    lengthSlider->setTextBoxStyle(juce::Slider::TextBoxBelow, false, 80, 20);
    lengthSlider->setRange(1.0, 16.0, 1.0);
    lengthSlider->setValue(4.0);
    panel->addAndMakeVisible(lengthSlider);
    
    auto* lengthLabel = new juce::Label();
    lengthLabel->setText("Length (bars)", juce::dontSendNotification);
    lengthLabel->attachToComponent(lengthSlider, false);
    panel->addAndMakeVisible(lengthLabel);
    
    featurePanels["AI MIDI Generation"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createKeyTempoDetectionPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Key/Tempo Detection");
    
    // Add key/tempo detection controls
    auto* keyLabel = new juce::Label();
    keyLabel->setText("Key: C Major", juce::dontSendNotification);
    keyLabel->setFont(style.bodyFont);
    keyLabel->setJustificationType(juce::Justification::centred);
    keyLabel->setColour(juce::Label::textColourId, style.primary);
    panel->addAndMakeVisible(keyLabel);
    
    auto* tempoLabel = new juce::Label();
    tempoLabel->setText("Tempo: 120 BPM", juce::dontSendNotification);
    tempoLabel->setFont(style.bodyFont);
    tempoLabel->setJustificationType(juce::Justification::centred);
    tempoLabel->setColour(juce::Label::textColourId, style.secondary);
    panel->addAndMakeVisible(tempoLabel);
    
    featurePanels["Key/Tempo Detection"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createVisualAnalysisPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Visual Analyzer");
    
    // Add visual analysis controls
    auto* visualizeButton = new juce::TextButton();
    visualizeButton->setButtonText("Start Visualization");
    visualizeButton->setColour(juce::TextButton::buttonColourId, style.accent);
    visualizeButton->setColour(juce::TextButton::textColourOnId, juce::Colours::white);
    panel->addAndMakeVisible(visualizeButton);
    
    featurePanels["Visual Analyzer"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createMoodRemixingPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Mood Remixer");
    
    // Add mood remixing controls
    auto* remixButton = new juce::TextButton();
    remixButton->setButtonText("Remix to New Mood");
    remixButton->setColour(juce::TextButton::buttonColourId, style.success);
    remixButton->setColour(juce::TextButton::textColourOnId, juce::Colours::white);
    panel->addAndMakeVisible(remixButton);
    
    featurePanels["Mood Remixer"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createMasteringToolsPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Mastering Tools");
    
    // Add mastering tools controls
    auto* masterButton = new juce::TextButton();
    masterButton->setButtonText("Apply AI Mastering");
    masterButton->setColour(juce::TextButton::buttonColourId, style.success);
    masterButton->setColour(juce::TextButton::textColourOnId, juce::Colours::white);
    panel->addAndMakeVisible(masterButton);
    
    featurePanels["Mastering Tools"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createGrooveHumanizationPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Groove Humanizer");
    
    // Add groove humanization controls
    auto* humanizeButton = new juce::TextButton();
    humanizeButton->setButtonText("Humanize Groove");
    humanizeButton->setColour(juce::TextButton::buttonColourId, style.success);
    humanizeButton->setColour(juce::TextButton::textColourOnId, juce::Colours::white);
    panel->addAndMakeVisible(humanizeButton);
    
    featurePanels["Groove Humanizer"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::createDynamicBalancingPanel()
{
    auto* panel = new juce::Component();
    panel->setName("Dynamic Balancer");
    
    // Add dynamic balancing controls
    auto* balanceButton = new juce::TextButton();
    balanceButton->setButtonText("Balance Dynamics");
    balanceButton->setColour(juce::TextButton::buttonColourId, style.success);
    balanceButton->setColour(juce::TextButton::textColourOnId, juce::Colours::white);
    panel->addAndMakeVisible(balanceButton);
    
    featurePanels["Dynamic Balancer"] = panel;
    featurePanel.addChildComponent(panel);
}

void ModernUI::paint(juce::Graphics& g)
{
    // Draw main background
    g.fillAll(style.background);
    
    // Draw panels
    g.setColour(style.surface);
    g.fillRoundedRectangle(headerPanel.getBounds().toFloat(), style.cornerRadius);
    g.fillRoundedRectangle(moodPanel.getBounds().toFloat(), style.cornerRadius);
    g.fillRoundedRectangle(featurePanel.getBounds().toFloat(), style.cornerRadius);
    g.fillRoundedRectangle(controlPanel.getBounds().toFloat(), style.cornerRadius);
    g.fillRoundedRectangle(statusPanel.getBounds().toFloat(), style.cornerRadius);
    
    // Draw borders
    g.setColour(style.primary.withAlpha(0.3f));
    g.drawRoundedRectangle(headerPanel.getBounds().toFloat(), style.cornerRadius, style.borderWidth);
    g.drawRoundedRectangle(moodPanel.getBounds().toFloat(), style.cornerRadius, style.borderWidth);
    g.drawRoundedRectangle(featurePanel.getBounds().toFloat(), style.cornerRadius, style.borderWidth);
    g.drawRoundedRectangle(controlPanel.getBounds().toFloat(), style.cornerRadius, style.borderWidth);
    g.drawRoundedRectangle(statusPanel.getBounds().toFloat(), style.cornerRadius, style.borderWidth);
}

void ModernUI::resized()
{
    // Update panel bounds
    headerPanel.setBounds(10, 10, getWidth() - 20, 60);
    moodPanel.setBounds(10, 80, getWidth() - 20, 100);
    featurePanel.setBounds(10, 190, getWidth() - 20, 400);
    controlPanel.setBounds(10, 600, getWidth() - 20, 80);
    statusPanel.setBounds(10, 690, getWidth() - 20, 80);
    
    // Layout header components
    titleLabel.setBounds(headerPanel.getBounds().withSizeKeepingCentre(200, 40));
    uploadButton.setBounds(headerPanel.getWidth() - 200, 10, 80, 30);
    downloadButton.setBounds(headerPanel.getWidth() - 110, 10, 100, 30);
    settingsButton.setBounds(headerPanel.getWidth() - 200, 40, 80, 20);
    
    // Layout mood display components
    moodTitleLabel.setBounds(moodPanel.getBounds().withSizeKeepingCentre(200, 20));
    primaryMoodLabel.setBounds(20, 30, 200, 20);
    secondaryMoodLabel.setBounds(20, 50, 200, 20);
    confidenceLabel.setBounds(20, 70, 200, 15);
    tagsLabel.setBounds(240, 30, 300, 20);
    analysisLabel.setBounds(240, 50, 300, 20);
    moodProgressBar.setBounds(240, 70, 300, 15);
    
    // Layout feature buttons in a grid
    int buttonWidth = 150;
    int buttonHeight = 40;
    int spacing = 10;
    int buttonsPerRow = (featurePanel.getWidth() - 20) / (buttonWidth + spacing);
    
    for (size_t i = 0; i < featureButtons.size(); ++i)
    {
        int row = i / buttonsPerRow;
        int col = i % buttonsPerRow;
        int x = 10 + col * (buttonWidth + spacing);
        int y = 10 + row * (buttonHeight + spacing);
        
        featureButtons[i].button.setBounds(x, y, buttonWidth, buttonHeight);
    }
    
    // Layout active feature panel
    if (activeFeaturePanel)
    {
        activeFeaturePanel->setBounds(10, 200, featurePanel.getWidth() - 20, 180);
    }
}

void ModernUI::updateMoodDisplay(const MoodDisplay& mood)
{
    currentMood = mood;
    
    primaryMoodLabel.setText("Primary: " + mood.primaryMood, juce::dontSendNotification);
    secondaryMoodLabel.setText("Secondary: " + mood.secondaryMood, juce::dontSendNotification);
    confidenceLabel.setText("Confidence: " + juce::String(mood.confidence * 100, 1) + "%", juce::dontSendNotification);
    
    // Update tags
    std::string tagsText = "Tags: ";
    for (size_t i = 0; i < mood.tags.size(); ++i)
    {
        if (i > 0) tagsText += ", ";
        tagsText += mood.tags[i];
    }
    tagsLabel.setText(tagsText, juce::dontSendNotification);
    
    // Update progress bar
    moodProgressBar.setPercentage(mood.confidence);
    
    repaint();
}

void ModernUI::setMoodAnalysis(const std::string& analysis)
{
    analysisLabel.setText("Analysis: " + analysis, juce::dontSendNotification);
    repaint();
}

void ModernUI::showFeaturePanel(const std::string& featureName)
{
    // Hide current panel
    if (activeFeaturePanel)
    {
        activeFeaturePanel->setVisible(false);
    }
    
    // Show new panel
    auto it = featurePanels.find(featureName);
    if (it != featurePanels.end())
    {
        activeFeaturePanel = it->second;
        activeFeaturePanel->setVisible(true);
    }
    
    // Update button states
    updateFeatureButtonStates();
    
    repaint();
}

void ModernUI::hideFeaturePanel()
{
    if (activeFeaturePanel)
    {
        activeFeaturePanel->setVisible(false);
        activeFeaturePanel = nullptr;
    }
    
    updateFeatureButtonStates();
    repaint();
}

void ModernUI::toggleAdvancedFeatures()
{
    showAdvancedFeatures = !showAdvancedFeatures;
    repaint();
}

void ModernUI::onUploadMIDI()
{
    // Implement MIDI upload functionality
    juce::FileChooser chooser("Select MIDI file", juce::File(), "*.mid;*.midi");
    if (chooser.browseForFileToOpen())
    {
        juce::File selectedFile = chooser.getResult();
        // Process the selected MIDI file
        setMoodAnalysis("Processing " + selectedFile.getFileName().toStdString() + "...");
    }
}

void ModernUI::onDownloadReport()
{
    // Implement report download functionality
    setMoodAnalysis("Generating report...");
}

void ModernUI::updateFeatureButtonStates()
{
    for (auto& button : featureButtons)
    {
        button.isActive = (activeFeaturePanel && activeFeaturePanel->getName() == button.name);
        button.button.setColour(juce::TextButton::buttonColourId, 
                               button.isActive ? button.color : style.surface);
    }
}
