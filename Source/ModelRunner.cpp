#include "ModelRunner.h"
#include <vector>

ModelRunner::ModelRunner(const std::string& modelPath)
    : env(ORT_LOGGING_LEVEL_WARNING, "Aamati"),
      session(env, modelPath.c_str(), Ort::SessionOptions{nullptr})
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

std::string ModelRunner::predict(const std::array<float, 5>& features) {
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

    // Map output to mood string (replace with your actual logic)
    static const std::vector<std::string> moods = {"happy", "sad", "chill", "energetic", "calm"};
    int idx = static_cast<int>(outData[0] + 0.5f);
    if (idx >= 0 && idx < static_cast<int>(moods.size()))
        return moods[idx];
    return "unknown";
}
