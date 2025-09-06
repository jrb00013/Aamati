#include "ModelRunner.h"
#include <vector>
#include <iostream>

ModelRunner::ModelRunner(const std::string& modelPath)
    : env(ORT_LOGGING_LEVEL_WARNING, "Aamati"),
      modelLoaded(false)
{
    loadModel(modelPath);
}

ModelRunner::~ModelRunner()
{
    unloadModel();
}

bool ModelRunner::loadModel(const std::string& modelPath)
{
    try
    {
        session = Ort::Session(env, modelPath.c_str(), Ort::SessionOptions{nullptr});
        initializeModel();
        modelLoaded = true;
        return true;
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error loading model: " << e.what() << std::endl;
        modelLoaded = false;
        return false;
    }
}

void ModelRunner::unloadModel()
{
    if (modelLoaded)
    {
        // Session will be automatically destroyed
        modelLoaded = false;
    }
}

void ModelRunner::initializeModel()
{
    Ort::AllocatorWithDefaultOptions allocator;

    // Copy input name string safely
    char* input_name_ptr = session.GetInputName(0, allocator);
    inputName = std::string(input_name_ptr);
    allocator.Free(input_name_ptr);

    // Copy output name string safely
    char* output_name_ptr = session.GetOutputName(0, allocator);
    outputName = std::string(output_name_ptr);
    allocator.Free(output_name_ptr);
}

std::string ModelRunner::predict(const std::array<float, 5>& features)
{
    if (!modelLoaded)
    {
        return "model_not_loaded";
    }

    try
    {
        std::vector<int64_t> dims = {1, 5}; // batch size 1, 5 features

        Ort::AllocatorWithDefaultOptions allocator;
        auto memory_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeCPU);

        Ort::Value inputTensor = Ort::Value::CreateTensor<float>(
            memory_info,
            const_cast<float*>(features.data()),
            features.size(),
            dims.data(),
            dims.size()
        );

        auto outputTensors = session.Run(Ort::RunOptions{nullptr},
                                         &inputName, &inputTensor, 1,
                                         &outputName, 1);

        float* outData = outputTensors.front().GetTensorMutableData<float>();

        // Get mood labels
        auto moodLabels = getMoodLabels();
        
        // Find the index with highest probability
        int bestIdx = 0;
        float bestScore = outData[0];
        
        for (size_t i = 1; i < moodLabels.size(); ++i)
        {
            if (outData[i] > bestScore)
            {
                bestScore = outData[i];
                bestIdx = static_cast<int>(i);
            }
        }

        if (bestIdx >= 0 && bestIdx < static_cast<int>(moodLabels.size()))
            return moodLabels[bestIdx];
        
        return "unknown";
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error during prediction: " << e.what() << std::endl;
        return "prediction_error";
    }
}

std::vector<float> ModelRunner::predictProbabilities(const std::array<float, 5>& features)
{
    if (!modelLoaded)
    {
        return {};
    }

    try
    {
        std::vector<int64_t> dims = {1, 5}; // batch size 1, 5 features

        Ort::AllocatorWithDefaultOptions allocator;
        auto memory_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeCPU);

        Ort::Value inputTensor = Ort::Value::CreateTensor<float>(
            memory_info,
            const_cast<float*>(features.data()),
            features.size(),
            dims.data(),
            dims.size()
        );

        auto outputTensors = session.Run(Ort::RunOptions{nullptr},
                                         &inputName, &inputTensor, 1,
                                         &outputName, 1);

        float* outData = outputTensors.front().GetTensorMutableData<float>();
        auto moodLabels = getMoodLabels();
        
        return std::vector<float>(outData, outData + moodLabels.size());
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error during probability prediction: " << e.what() << std::endl;
        return {};
    }
}

std::vector<std::string> ModelRunner::getMoodLabels()
{
    // These should match the labels used in your trained model
    return {
        "chill", "energetic", "suspenseful", "uplifting", "ominous",
        "romantic", "gritty", "dreamy", "frantic", "focused"
    };
}
