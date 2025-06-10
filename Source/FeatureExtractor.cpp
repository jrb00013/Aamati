#include "FeatureExtractor.h"
#include "MidiFile.h"
#include "Options.h"
#include <cmath>
#include <vector>
#include <numeric>
#include <algorithm>

using namespace std;
using namespace smf;

array<float, 5> FeatureExtractor::extractFeaturesFromMIDI(const string& midiPath) {
    MidiFile midi;
    if (!midi.read(midiPath)) return {120.0f, 0.0f, 0.0f, 0.0f, 0.0f}; // fallback

    midi.doTimeAnalysis();
    midi.linkNotePairs();

    vector<float> noteTimes;
    vector<int> velocities;
    float endTime = 0.0f;

    for (int t = 0; t < midi.getTrackCount(); ++t) {
        for (int e = 0; e < midi[t].size(); ++e) {
            MidiEvent& mev = midi[t][e];
            if (!mev.isNoteOn()) continue;
            if (!mev.isDrumNote()) continue;

            float time = mev.seconds;
            noteTimes.push_back(time);
            velocities.push_back(mev.getVelocity());

            if (time > endTime) endTime = time;
        }
    }

    if (noteTimes.size() < 2 || endTime <= 0.0f)
        return {120.0f, 0.0f, 0.0f, 0.0f, 0.0f};

    float density = noteTimes.size() / endTime;

    // Swing: Deviation from strict 8th note grid (assume 120 BPM 8th notes = 0.25s apart)
    float swingSum = 0.0f;
    for (auto& time : noteTimes) {
        float quant = round(time * 4.0f) / 4.0f; // nearest 0.25
        swingSum += fabs(time - quant);
    }
    float swing = swingSum / noteTimes.size();

    int maxVel = *max_element(velocities.begin(), velocities.end());
    int minVel = *min_element(velocities.begin(), velocities.end());
    float dynamicRange = static_cast<float>(maxVel - minVel);
    float meanVel = accumulate(velocities.begin(), velocities.end(), 0.0f) / velocities.size();

    float energy = (density * 0.5f) + (meanVel / 127.0f * 0.5f);

    float tempo = 120.0f;
    if (midi.getTicksPerQuarterNote() > 0) {
        tempo = 60.0f / midi.getTimeInSeconds(midi.getTicksPerQuarterNote());
    }

    return {tempo, swing, density, dynamicRange, energy};
}
