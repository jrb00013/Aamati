#pragma once
#include <vector>

struct GrooveFeatures {
    double tempo;
    double swing;
    double density;
    double dynamicRange;
    double energy;
};

class FeatureExtractor {
public:
    FeatureExtractor();
    GrooveFeatures extractFeaturesFromMidi(const std::string& midiFilePath);
};