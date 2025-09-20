# MP3 Chord Detection Script

A Python script that analyzes MP3 audio files to extract chord progressions using chromagram analysis and template matching.

## Features

- **Chord Detection**: Identifies major and minor chords (C, C#, D, D#, E, F, F#, G, G#, A, A#, B and their minor variants)
- **Timing Information**: Provides start/end times and duration for each chord
- **Chord Statistics**: Shows frequency analysis of detected chords
- **Multiple Audio Formats**: Supports MP3, WAV, FLAC, and M4A files
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

## How It Works

1. **Audio Loading**: Uses librosa to load and preprocess audio files
2. **Chromagram Extraction**: Converts audio to chromagram features (12-dimensional pitch class profiles)
3. **Template Matching**: Compares chromagram frames against predefined chord templates
4. **Smoothing**: Applies temporal smoothing to reduce noise in chord detection
5. **Progression Analysis**: Extracts unique chord changes with timing information

## Output Format

The script provides:

### Chord Progression
- Sequential list of detected chords with timestamps
- Format: `Chord | Start - End | Duration`

### Chord Frequency
- Percentage breakdown of how often each chord appears
- Useful for understanding the harmonic content of the song

## Example Output

```
============================================================
CHORD ANALYSIS RESULTS FOR: example.mp3
============================================================

Total Duration: 03:45

📊 CHORD PROGRESSION:
--------------------------------------------------
 1. Am   | 00:00 - 00:15 | Duration: 00:15
 2. F    | 00:15 - 00:30 | Duration: 00:15
 3. C    | 00:30 - 00:45 | Duration: 00:15
 4. G    | 00:45 - 01:00 | Duration: 00:15

🎵 CHORD FREQUENCY:
------------------------------
Am  :  25.0% (120 frames)
F   :  25.0% (120 frames)
C   :  25.0% (120 frames)
G   :  25.0% (120 frames)
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

## Requirements

- Python 3.7+
- librosa 0.10.0+
- numpy 1.21.0+
- scipy 1.7.0+
