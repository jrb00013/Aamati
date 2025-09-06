#pragma once

#include <onnxruntime_cxx_api.h>
#include <string>
#include <array>
#include <vector>

class ModelRunner {
public:
    explicit ModelRunner(const std::string& modelPath);
    ~ModelRunner();
    
    // Main prediction method
    std::string predict(const std::array<float, 5>& features);
    
    // Additional prediction methods for different model types
    std::vector<float> predictProbabilities(const std::array<float, 5>& features);
    bool isModelLoaded() const { return modelLoaded; }
    
    // Model management
    bool loadModel(const std::string& modelPath);
    void unloadModel();

private:
    Ort::Env env;
    Ort::Session session;
    std::string inputName;
    std::string outputName;
    bool modelLoaded;
    
    // Helper methods
    void initializeModel();
    std::vector<std::string> getMoodLabels();
};