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
        // Validate model file exists and is readable
        if (!validateModelFile(modelPath))
        {
            std::cerr << "Model file validation failed: " << modelPath << std::endl;
            return false;
        }
        
        // Create session with enhanced options
        Ort::SessionOptions sessionOptions;
        sessionOptions.SetIntraOpNumThreads(1);
        sessionOptions.SetGraphOptimizationLevel(ORT_ENABLE_BASIC);
        
        session = Ort::Session(env, modelPath.c_str(), sessionOptions);
        
        // Validate model structure
        if (!validateModelStructure())
        {
            std::cerr << "Model structure validation failed" << std::endl;
            return false;
        }
        
        initializeModel();
        modelLoaded = true;
        
        std::cout << "Model loaded successfully: " << modelPath << std::endl;
        return true;
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error loading model: " << e.what() << std::endl;
        modelLoaded = false;
        return false;
    }
}

bool ModelRunner::validateModelFile(const std::string& modelPath)
{
    // Check if file exists
    std::ifstream file(modelPath);
    if (!file.good())
    {
        std::cerr << "Model file does not exist or is not readable: " << modelPath << std::endl;
        return false;
    }
    
    // Check file size (basic validation)
    file.seekg(0, std::ios::end);
    size_t fileSize = file.tellg();
    if (fileSize < 1024) // Minimum reasonable model size
    {
        std::cerr << "Model file too small: " << fileSize << " bytes" << std::endl;
        return false;
    }
    
    return true;
}

bool ModelRunner::validateModelStructure()
{
    try
    {
        Ort::AllocatorWithDefaultOptions allocator;
        
        // Check input count
        size_t inputCount = session.GetInputCount();
        if (inputCount != 1)
        {
            std::cerr << "Expected 1 input, got: " << inputCount << std::endl;
            return false;
        }
        
        // Check output count
        size_t outputCount = session.GetOutputCount();
        if (outputCount != 1)
        {
            std::cerr << "Expected 1 output, got: " << outputCount << std::endl;
            return false;
        }
        
        // Validate input shape
        auto inputTypeInfo = session.GetInputTypeInfo(0);
        auto inputTensorInfo = inputTypeInfo.GetTensorTypeAndShapeInfo();
        auto inputShape = inputTensorInfo.GetShape();
        
        if (inputShape.size() != 2 || inputShape[1] != 5)
        {
            std::cerr << "Invalid input shape. Expected [batch_size, 5], got: [";
            for (size_t i = 0; i < inputShape.size(); ++i)
            {
                if (i > 0) std::cerr << ", ";
                std::cerr << inputShape[i];
            }
            std::cerr << "]" << std::endl;
            return false;
        }
        
        // Validate output shape
        auto outputTypeInfo = session.GetOutputTypeInfo(0);
        auto outputTensorInfo = outputTypeInfo.GetTensorTypeAndShapeInfo();
        auto outputShape = outputTensorInfo.GetShape();
        
        if (outputShape.size() != 2 || outputShape[1] != 10)
        {
            std::cerr << "Invalid output shape. Expected [batch_size, 10], got: [";
            for (size_t i = 0; i < outputShape.size(); ++i)
            {
                if (i > 0) std::cerr << ", ";
                std::cerr << outputShape[i];
            }
            std::cerr << "]" << std::endl;
            return false;
        }
        
        return true;
    }
    catch (const std::exception& e)
    {
        std::cerr << "Model structure validation error: " << e.what() << std::endl;
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
        std::cerr << "Model not loaded" << std::endl;
        return "model_not_loaded";
    }

    try
    {
        // Validate input features
        if (!validateInputFeatures(features))
        {
            std::cerr << "Invalid input features" << std::endl;
            return "invalid_input";
        }

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

        if (outputTensors.empty())
        {
            std::cerr << "No output from model" << std::endl;
            return "no_output";
        }

        float* outData = outputTensors.front().GetTensorMutableData<float>();

        // Get mood labels
        auto moodLabels = getMoodLabels();
        
        // Validate output size
        if (moodLabels.size() != 10)
        {
            std::cerr << "Mismatch between mood labels and model output size" << std::endl;
            return "output_size_mismatch";
        }
        
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

        // Validate confidence threshold
        if (bestScore < 0.1f) // Very low confidence
        {
            std::cerr << "Low confidence prediction: " << bestScore << std::endl;
            return "low_confidence";
        }

        if (bestIdx >= 0 && bestIdx < static_cast<int>(moodLabels.size()))
        {
            std::cout << "Predicted mood: " << moodLabels[bestIdx] << " (confidence: " << bestScore << ")" << std::endl;
            return moodLabels[bestIdx];
        }
        
        return "unknown";
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error during prediction: " << e.what() << std::endl;
        return "prediction_error";
    }
}

bool ModelRunner::validateInputFeatures(const std::array<float, 5>& features)
{
    // Check for NaN or infinite values
    for (float feature : features)
    {
        if (!std::isfinite(feature))
        {
            std::cerr << "Invalid feature value: " << feature << std::endl;
            return false;
        }
    }
    
    // Check reasonable ranges for each feature
    if (features[0] < 60.0f || features[0] > 200.0f) // Tempo
    {
        std::cerr << "Tempo out of range: " << features[0] << std::endl;
        return false;
    }
    
    if (features[1] < 0.0f || features[1] > 1.0f) // Swing
    {
        std::cerr << "Swing out of range: " << features[1] << std::endl;
        return false;
    }
    
    if (features[2] < 0.0f || features[2] > 10.0f) // Density
    {
        std::cerr << "Density out of range: " << features[2] << std::endl;
        return false;
    }
    
    if (features[3] < 0.0f || features[3] > 127.0f) // Dynamic range
    {
        std::cerr << "Dynamic range out of range: " << features[3] << std::endl;
        return false;
    }
    
    if (features[4] < 0.0f || features[4] > 1.0f) // Energy
    {
        std::cerr << "Energy out of range: " << features[4] << std::endl;
        return false;
    }
    
    return true;
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
