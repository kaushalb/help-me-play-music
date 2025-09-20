#!/usr/bin/env python3
"""
ChordDetector Class
Handles chord detection from audio files using chromagram analysis and template matching.
"""

import librosa
import numpy as np
from scipy.signal import find_peaks
from collections import Counter

class ChordDetector:
    def __init__(self):
        # Define chord templates based on chromagram patterns
        self.chord_templates = {
            'C': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],      # C major
            'C#': [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],     # C# major
            'D': [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],      # D major
            'D#': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],     # D# major
            'E': [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],      # E major
            'F': [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],      # F major
            'F#': [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],     # F# major
            'G': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],      # G major
            'G#': [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],     # G# major
            'A': [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],      # A major
            'A#': [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],     # A# major
            'B': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],      # B major
            
            # Minor chords
            'Cm': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],     # C minor
            'C#m': [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],    # C# minor
            'Dm': [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],     # D minor
            'D#m': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],    # D# minor
            'Em': [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],     # E minor
            'Fm': [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],     # F minor
            'F#m': [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],    # F# minor
            'Gm': [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],     # G minor
            'G#m': [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],    # G# minor
            'Am': [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],     # A minor
            'A#m': [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],    # A# minor
            'Bm': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],     # B minor
        }
        
        # Convert templates to numpy arrays for easier computation
        for chord in self.chord_templates:
            self.chord_templates[chord] = np.array(self.chord_templates[chord])
    
    def load_audio(self, file_path):
        """Load MP3 file and return audio time series and sample rate."""
        try:
            print(f"Loading audio file: {file_path}")
            y, sr = librosa.load(file_path, sr=22050)
            print(f"Audio loaded successfully. Duration: {len(y)/sr:.2f} seconds")
            return y, sr
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return None, None
    
    def extract_chromagram(self, y, sr, hop_length=512):
        """Extract chromagram features from audio."""
        print("Extracting chromagram features...")
        # Compute chromagram
        chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop_length)
        return chroma
    
    def detect_chords_from_chroma(self, chroma):
        """Detect chords from chromagram using template matching."""
        print("Detecting chords from chromagram...")
        
        # Number of time frames
        n_frames = chroma.shape[1]
        detected_chords = []
        
        # Analyze each time frame
        for frame_idx in range(n_frames):
            frame_chroma = chroma[:, frame_idx]
            
            # Normalize the chroma vector
            if np.sum(frame_chroma) > 0:
                frame_chroma = frame_chroma / np.sum(frame_chroma)
            
            # Find best matching chord template
            best_chord = None
            best_score = -1
            
            for chord_name, template in self.chord_templates.items():
                # Compute correlation between frame and template
                score = np.corrcoef(frame_chroma, template)[0, 1]
                if not np.isnan(score) and score > best_score:
                    best_score = score
                    best_chord = chord_name
            
            detected_chords.append(best_chord if best_score > 0.5 else 'N/A')
        
        return detected_chords
    
    def smooth_chord_progression(self, chords, window_size=5):
        """Smooth chord progression to reduce noise."""
        smoothed_chords = []
        
        for i in range(len(chords)):
            start_idx = max(0, i - window_size // 2)
            end_idx = min(len(chords), i + window_size // 2 + 1)
            
            window_chords = chords[start_idx:end_idx]
            # Find most common chord in window
            chord_counts = Counter([c for c in window_chords if c != 'N/A'])
            
            if chord_counts:
                most_common_chord = chord_counts.most_common(1)[0][0]
                smoothed_chords.append(most_common_chord)
            else:
                smoothed_chords.append('N/A')
        
        return smoothed_chords
    
    def get_chord_progression(self, chords, hop_length=512, sr=22050):
        """Extract unique chord progression with timing information."""
        print("Extracting chord progression...")
        
        progression = []
        current_chord = None
        start_time = 0
        
        frame_duration = hop_length / sr  # Duration of each frame in seconds
        
        for i, chord in enumerate(chords):
            if chord != current_chord and chord != 'N/A':
                if current_chord is not None:
                    end_time = i * frame_duration
                    progression.append({
                        'chord': current_chord,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': end_time - start_time
                    })
                
                current_chord = chord
                start_time = i * frame_duration
        
        # Add the last chord
        if current_chord is not None:
            end_time = len(chords) * frame_duration
            progression.append({
                'chord': current_chord,
                'start_time': start_time,
                'end_time': end_time,
                'duration': end_time - start_time
            })
        
        return progression
    
    def analyze_mp3(self, file_path):
        """Main method to analyze MP3 file and return chord information."""
        # Load audio
        y, sr = self.load_audio(file_path)
        if y is None:
            return None
        
        # Extract chromagram
        chroma = self.extract_chromagram(y, sr)
        
        # Detect chords
        raw_chords = self.detect_chords_from_chroma(chroma)
        
        # Smooth chord progression
        smoothed_chords = self.smooth_chord_progression(raw_chords)
        
        # Get final chord progression
        progression = self.get_chord_progression(smoothed_chords)
        
        # Get chord statistics
        chord_counts = Counter([c for c in smoothed_chords if c != 'N/A'])
        
        return {
            'progression': progression,
            'chord_counts': chord_counts,
            'total_duration': len(y) / sr
        }
