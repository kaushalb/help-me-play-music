#!/usr/bin/env python3
"""
MP3 Chord Detection Script
Analyzes MP3 audio files to extract chord progressions using chromagram analysis.
"""

import librosa
import numpy as np
import argparse
import sys
from scipy.signal import find_peaks
from collections import Counter
import os

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

def format_time(seconds):
    """Format time in MM:SS.mmm format with milliseconds."""
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    secs = int(remaining_seconds)
    milliseconds = int((remaining_seconds - secs) * 1000)
    return f"{minutes:02d}:{secs:02d}.{milliseconds:03d}"

def create_chord_timeline(results):
    """Create a visual timeline representation of chord progression."""
    if not results or not results['progression']:
        return "No chord progression detected."
    
    # Create a continuous timeline with | for chord changes and - for duration
    timeline_line = "|"
    chord_labels = []
    
    for i, chord_info in enumerate(results['progression']):
        # Calculate relative duration (simple approach: use 5 dashes per chord for now)
        # You could make this proportional to actual duration if needed
        duration_dashes = "-----"
        timeline_line += duration_dashes + "|"
        chord_labels.append(chord_info['chord'])
    
    # Create the chord labels line, spaced to align with timeline
    chord_line = ""
    for i, chord in enumerate(chord_labels):
        if i == 0:
            chord_line += f"{chord:^6}"  # Center chord name in 6 characters (5 dashes + 1 |)
        else:
            chord_line += f"{chord:^6}"
    
    return f"{timeline_line}\n{chord_line}"

def save_results_to_file(results, file_path, output_file="chord-output.txt"):
    """Save analysis results to a text file."""
    try:
        # Create the file if it doesn't exist, or overwrite if it does
        if not os.path.exists(output_file):
            print(f"Creating new file: {output_file}")
        else:
            print(f"Overwriting existing file: {output_file}")
            
        with open(output_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write(f"CHORD ANALYSIS RESULTS FOR: {os.path.basename(file_path)}\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"Total Duration: {format_time(results['total_duration'])}\n\n")
            
            f.write("📊 CHORD PROGRESSION:\n")
            f.write("-" * 50 + "\n")
            
            if results['progression']:
                for i, chord_info in enumerate(results['progression'], 1):
                    start_time = format_time(chord_info['start_time'])
                    end_time = format_time(chord_info['end_time'])
                    duration = format_time(chord_info['duration'])
                    
                    f.write(f"{i:2d}. {chord_info['chord']:4s} | {start_time} - {end_time} | Duration: {duration}\n")
                
                f.write("\n" + create_chord_timeline(results) + "\n\n")
            else:
                f.write("No clear chord progression detected.\n\n")
            
            f.write("🎵 CHORD FREQUENCY:\n")
            f.write("-" * 30 + "\n")
            
            if results['chord_counts']:
                total_frames = sum(results['chord_counts'].values())
                for chord, count in results['chord_counts'].most_common():
                    percentage = (count / total_frames) * 100
                    f.write(f"{chord:4s}: {percentage:5.1f}% ({count} frames)\n")
            else:
                f.write("No chords detected.\n")
            
            f.write("\n" + "="*60 + "\n")
        
        print(f"Results saved to {output_file}")
        
    except Exception as e:
        print(f"Error saving to file: {e}")

def print_analysis_results(results, file_path):
    """Print the chord analysis results in a formatted way."""
    if not results:
        print("No results to display.")
        return
    
    print("\n" + "="*60)
    print(f"CHORD ANALYSIS RESULTS FOR: {os.path.basename(file_path)}")
    print("="*60)
    
    print(f"\nTotal Duration: {format_time(results['total_duration'])}")
    
    print("\n📊 CHORD PROGRESSION:")
    print("-" * 50)
    
    if results['progression']:
        for i, chord_info in enumerate(results['progression'], 1):
            start_time = format_time(chord_info['start_time'])
            end_time = format_time(chord_info['end_time'])
            duration = format_time(chord_info['duration'])
            
            print(f"{i:2d}. {chord_info['chord']:4s} | {start_time} - {end_time} | Duration: {duration}")
    else:
        print("No clear chord progression detected.")
    
    print("\n🎵 CHORD FREQUENCY:")
    print("-" * 30)
    
    if results['chord_counts']:
        total_frames = sum(results['chord_counts'].values())
        for chord, count in results['chord_counts'].most_common():
            percentage = (count / total_frames) * 100
            print(f"{chord:4s}: {percentage:5.1f}% ({count} frames)")
    else:
        print("No chords detected.")
    
    print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(description='Analyze MP3 files for chord progressions')
    parser.add_argument('file_path', help='Path to the MP3 file to analyze')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--output', '-o', default='chord-output.txt', help='Output file for results (default: chord-output.txt)')
    parser.add_argument('--save', '-s', action='store_true', help='Save results to output file')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.file_path):
        print(f"Error: File '{args.file_path}' not found.")
        sys.exit(1)
    
    # Check if file is MP3
    if not args.file_path.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
        print("Warning: File doesn't appear to be an audio file. Proceeding anyway...")
    
    # Create chord detector and analyze
    detector = ChordDetector()
    
    try:
        results = detector.analyze_mp3(args.file_path)
        print_analysis_results(results, args.file_path)
        
        # Save results to file if requested
        if args.save:
            save_results_to_file(results, args.file_path, args.output)
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()