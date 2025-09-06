#pragma once

#include <JuceHeader.h>
#include <vector>
#include <map>
#include <string>

/**
 * Modern UI System for Aamati
 * Clean, professional interface with all advanced features
 */
class ModernUI : public juce::Component
{
public:
    struct UIStyle
    {
        juce::Colour background = juce::Colour(15, 15, 25);
        juce::Colour surface = juce::Colour(25, 25, 35);
        juce::Colour primary = juce::Colour(255, 215, 0);
        juce::Colour secondary = juce::Colour(200, 200, 200);
        juce::Colour accent = juce::Colour(100, 150, 255);
        juce::Colour success = juce::Colour(100, 255, 100);
        juce::Colour warning = juce::Colour(255, 200, 100);
        juce::Colour error = juce::Colour(255, 100, 100);
        
        float cornerRadius = 8.0f;
        float borderWidth = 1.0f;
        juce::Font titleFont = juce::Font(24.0f, juce::Font::bold);
        juce::Font bodyFont = juce::Font(14.0f);
        juce::Font smallFont = juce::Font(12.0f);
    };
    
    struct MoodDisplay
    {
        std::string primaryMood = "unknown";
        std::string secondaryMood = "unknown";
        float confidence = 0.0f;
        std::vector<std::string> tags;
        std::string analysis = "Analyzing...";
    };
    
    ModernUI();
    ~ModernUI();
    
    // Main UI functions
    void paint(juce::Graphics& g) override;
    void resized() override;
    void mouseDown(const juce::MouseEvent& event) override;
    
    // Mood display
    void updateMoodDisplay(const MoodDisplay& mood);
    void setMoodAnalysis(const std::string& analysis);
    
    // Feature panels
    void showFeaturePanel(const std::string& featureName);
    void hideFeaturePanel();
    void toggleAdvancedFeatures();
    
    // File operations
    void onUploadMIDI();
    void onDownloadReport();
    
    // Feature callbacks
    std::function<void()> onEmotionalOptimization;
    std::function<void()> onGrooveShaping;
    std::function<void()> onInstrumentation;
    std::function<void()> onMelodicContour;
    std::function<void()> onHarmonicDensity;
    std::function<void()> onFillOrnament;
    std::function<void()> onAIMidiGeneration;
    std::function<void()> onKeyTempoDetection;
    std::function<void()> onVisualAnalysis;
    std::function<void()> onMoodRemixing;
    std::function<void()> onMasteringTools;
    std::function<void()> onGrooveHumanization;
    std::function<void()> onDynamicBalancing;
    
private:
    // UI Style
    UIStyle style;
    
    // Main components
    juce::Component headerPanel;
    juce::Component moodPanel;
    juce::Component featurePanel;
    juce::Component controlPanel;
    juce::Component statusPanel;
    
    // Header components
    juce::Label titleLabel;
    juce::TextButton uploadButton;
    juce::TextButton downloadButton;
    juce::TextButton settingsButton;
    
    // Mood display components
    juce::Label moodTitleLabel;
    juce::Label primaryMoodLabel;
    juce::Label secondaryMoodLabel;
    juce::Label confidenceLabel;
    juce::Label tagsLabel;
    juce::Label analysisLabel;
    juce::ProgressBar moodProgressBar;
    
    // Feature buttons
    struct FeatureButton
    {
        juce::TextButton button;
        std::string name;
        std::string description;
        juce::Colour color;
        bool isActive = false;
    };
    
    std::vector<FeatureButton> featureButtons;
    
    // Feature panels
    std::map<std::string, juce::Component*> featurePanels;
    juce::Component* activeFeaturePanel = nullptr;
    
    // UI State
    bool showAdvancedFeatures = false;
    MoodDisplay currentMood;
    
    // Internal functions
    void setupUI();
    void createFeatureButtons();
    void createFeaturePanels();
    void updateFeatureButtonStates();
    void drawModernButton(juce::Graphics& g, const juce::Rectangle<int>& bounds, 
                         const std::string& text, bool isActive, juce::Colour color);
    void drawMoodDisplay(juce::Graphics& g, const juce::Rectangle<int>& bounds);
    void drawFeaturePanel(juce::Graphics& g, const juce::Rectangle<int>& bounds);
    
    // Feature panel implementations
    void createEmotionalOptimizationPanel();
    void createGrooveShapingPanel();
    void createInstrumentationPanel();
    void createMelodicContourPanel();
    void createHarmonicDensityPanel();
    void createFillOrnamentPanel();
    void createAIMidiGenerationPanel();
    void createKeyTempoDetectionPanel();
    void createVisualAnalysisPanel();
    void createMoodRemixingPanel();
    void createMasteringToolsPanel();
    void createGrooveHumanizationPanel();
    void createDynamicBalancingPanel();
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(ModernUI)
};
