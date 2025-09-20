# MP3 Chord Detection Script

A Python script that analyzes MP3 audio files and live audio recordings to extract chord progressions using chromagram analysis and template matching.

## Features

- **Chord Detection**: Identifies major and minor chords (C, C#, D, D#, E, F, F#, G, G#, A, A#, B and their minor variants)
- **Timing Information**: Provides start/end times and duration for each chord with millisecond precision
- **Chord Statistics**: Shows frequency analysis of detected chords
- **Multiple Audio Formats**: Supports MP3, WAV, FLAC, and M4A files
- **Live Audio Recording**: Record and analyze audio directly from your microphone
- **Interactive Mode**: Choose between file input or live recording when no arguments provided
- **File Output**: Save results to text files with custom timeline visualization
- **Visual Timeline**: ASCII-based chord progression timeline using `|` and `-` characters
- **Clean Output**: Formatted results with progression timeline and statistics

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python music-script.py path/to/your/audio/file.mp3
```

### With Verbose Output
```bash
python music-script.py path/to/your/audio/file.mp3 --verbose
```

### Save Results to File
```bash
# Save to default chord-output.txt
python music-script.py path/to/your/audio/file.mp3 --save

# Save to custom file
python music-script.py path/to/your/audio/file.mp3 --save --output my-results.txt

# Short form
python music-script.py path/to/your/audio/file.mp3 -s -o my-results.txt
```

### Live Audio Recording
```bash
# Record live audio from microphone
python music-script.py --live

# Interactive mode (choose file or live recording)
python music-script.py
```

## How It Works

1. **Audio Loading**: Uses librosa to load and preprocess audio files
2. **Chromagram Extraction**: Converts audio to chromagram features (12-dimensional pitch class profiles)
3. **Template Matching**: Compares chromagram frames against predefined chord templates
4. **Smoothing**: Applies temporal smoothing to reduce noise in chord detection
5. **Progression Analysis**: Extracts unique chord changes with timing information

## Output Format

The script provides:

### Console Output
- Sequential list of detected chords with timestamps
- Format: `Chord | Start - End | Duration`
- Chord frequency statistics

### File Output (when using --save)
- All console information saved to file
- **Visual Timeline**: Custom chord progression visualization
- Timeline format: `|-----|-----|-----|` where `|` marks chord changes and `-` represents duration

## Example Output

### Console Display
```
============================================================
CHORD ANALYSIS RESULTS FOR: example.mp3
============================================================

Total Duration: 00:03.450

📊 CHORD PROGRESSION:
--------------------------------------------------
 1. Am   | 00:00.000 - 00:00.863 | Duration: 00:00.863
 2. F    | 00:00.863 - 00:01.726 | Duration: 00:00.863
 3. C    | 00:01.726 - 00:02.589 | Duration: 00:00.863
 4. G    | 00:02.589 - 00:03.450 | Duration: 00:00.861

🎵 CHORD FREQUENCY:
------------------------------
Am  :  25.0% (30 frames)
F   :  25.0% (30 frames)
C   :  25.0% (30 frames)
G   :  25.0% (30 frames)
============================================================
```

### File Output (chord-output.txt)
```
============================================================
CHORD ANALYSIS RESULTS FOR: example.mp3
============================================================

Total Duration: 00:03.450

📊 CHORD PROGRESSION:
--------------------------------------------------
 1. Am   | 00:00.000 - 00:00.863 | Duration: 00:00.863
 2. F    | 00:00.863 - 00:01.726 | Duration: 00:00.863
 3. C    | 00:01.726 - 00:02.589 | Duration: 00:00.863
 4. G    | 00:02.589 - 00:03.450 | Duration: 00:00.861

|-----|-----|-----|-----|
  Am    F     C     G   

🎵 CHORD FREQUENCY:
------------------------------
Am  :  25.0% (30 frames)
F   :  25.0% (30 frames)
C   :  25.0% (30 frames)
G   :  25.0% (30 frames)
============================================================
```

## Limitations

- Works best with clear, harmonic music (pop, rock, folk)
- May struggle with heavily distorted or complex jazz harmonies
- Accuracy depends on audio quality and mixing
- Currently detects only major and minor triads

## Technical Details

- **Sample Rate**: 22.05 kHz (downsampled for efficiency)
- **Hop Length**: 512 samples (~23ms frames)
- **Chord Templates**: Based on chromagram patterns for major/minor triads
- **Smoothing Window**: 5 frames to reduce temporal noise

## Project Structure

```
help-me-play-music/
├── music-script.py          # Main script with CLI interface
├── ChordDetector.py         # Core chord detection class
├── utils/                   # Utility modules
│   ├── __init__.py
│   └── save_to_output.py    # Output formatting functions
├── live_recordings/         # Directory for saved live recordings
├── requirements.txt         # Python dependencies
├── chord-output.txt         # Default output file (generated)
└── README.md               # This file
```

## Live Recording Features

When using live recording mode:
- Press 'q' and Enter to stop recording
- Recordings are automatically saved to `live_recordings/` directory
- Files are named with timestamps: `live_recording_[timestamp].wav`
- Same chord analysis is applied to live recordings as audio files
- Interactive prompts guide you through the process

## Requirements

- Python 3.7+
- librosa 0.10.0+
- numpy 1.21.0+
- scipy 1.7.0+
- sounddevice 0.4.0+ (for live recording)
- keyboard 0.13.5+ (for live recording controls)
