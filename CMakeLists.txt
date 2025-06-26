cmake_minimum_required(VERSION 3.15)

project(Aamati VERSION 1.1.0)

# Find and include JUCE
set(JUCE_DIR "JUCE")
add_subdirectory(${JUCE_DIR} JUCE)

# Include Midifile and link libraries
add_subdirectory(midifile midifile_build)
target_link_libraries(Aamati PRIVATE midifile)

# Include Onnx Runtime and link libraries
add_subdirectory(onnxruntime)
target_link_libraries(Aamati PRIVATE
    onnxruntime
)

# Create the plugin
juce_add_plugin(Aamati
    COMPANY_NAME "Aamati Productions"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    COPY_PLUGIN_AFTER_BUILD TRUE
    PLUGIN_MANUFACTURER_CODE Amat
    PLUGIN_CODE Amt1
    FORMATS VST3 Standalone
    PRODUCT_NAME "Aamati"
    BUNDLE_ID "com.AamatiProductions.Aamati")

# Generate JUCE header
juce_generate_juce_header(Aamati)

# Add source files
target_sources(Aamati PRIVATE
    Source/PluginProcessor.cpp
    Source/PluginEditor.cpp)

# Add compiler definitions
target_compile_definitions(Aamati PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
    JUCE_USE_CUSTOM_PLUGIN_STANDALONE_APP=0)

# Link required JUCE modules
target_link_libraries(Aamati
    PRIVATE
        juce::juce_audio_utils
        juce::juce_audio_processors
        juce::juce_dsp
        midifile
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags)

# Enable DSP module
target_compile_definitions(Aamati PRIVATE
    JUCE_DSP=1)

# Link pthread and dl on UNIX systems
if(UNIX)
    target_link_libraries(Aamati PRIVATE pthread dl)
endif()

# === Copy ONNX model to build Resources ===
set(MODEL_PATH "${CMAKE_CURRENT_SOURCE_DIR}/MLPython/groove_mood_model.onnx")
set(DEST_PATH "${CMAKE_CURRENT_BINARY_DIR}/Resources")

file(MAKE_DIRECTORY ${DEST_PATH})

add_custom_command(
    TARGET Aamati POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different ${MODEL_PATH} ${DEST_PATH}/groove_mood_model.onnx
)

