#pragma once

#include <onnxruntime_cxx_api.h>
#include <string>
#include <array>

class ModelRunner {
public:
    explicit ModelRunner(const std::string& modelPath);
    std::string predict(const std::array<float, 5>& features);

private:
    Ort::Env env;
    Ort::Session session;
    std::string inputName;
    std::string outputName;
};