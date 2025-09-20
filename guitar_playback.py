#!/usr/bin/env python3
"""
Guitar Chord Playback System
Reads chord-output.txt and plays back the detected chords using synthesized guitar sounds.
"""

import re
import time
import sys
from synthesizer import Player, Synthesizer, Waveform

class GuitarPlayback:
    def __init__(self):
        # Initialize synthesizer with guitar-like settings
        self.player = Player()
        self.player.open_stream()
        
        # Use sawtooth wave for a more guitar-like sound
        self.synthesizer = Synthesizer(
            osc1_waveform=Waveform.sawtooth,
            osc1_volume=0.8,
            use_osc2=True,
            osc2_waveform=Waveform.square,
            osc2_volume=0.3,
            osc2_freq_transpose=12  # One octave higher
        )
        
        # Define chord note mappings (guitar voicings in 4th octave)
        self.chord_notes = {
            # Major chords
            'C': ['C4', 'E4', 'G4'],
            'C#': ['C#4', 'F4', 'G#4'],
            'D': ['D4', 'F#4', 'A4'],
            'D#': ['D#4', 'G4', 'A#4'],
            'E': ['E4', 'G#4', 'B4'],
            'F': ['F4', 'A4', 'C5'],
            'F#': ['F#4', 'A#4', 'C#5'],
            'G': ['G4', 'B4', 'D5'],
            'G#': ['G#4', 'C5', 'D#5'],
            'A': ['A4', 'C#5', 'E5'],
            'A#': ['A#4', 'D5', 'F5'],
            'B': ['B4', 'D#5', 'F#5'],
            
            # Minor chords
            'Cm': ['C4', 'D#4', 'G4'],
            'C#m': ['C#4', 'E4', 'G#4'],
            'Dm': ['D4', 'F4', 'A4'],
            'D#m': ['D#4', 'F#4', 'A#4'],
            'Em': ['E4', 'G4', 'B4'],
            'Fm': ['F4', 'G#4', 'C5'],
            'F#m': ['F#4', 'A4', 'C#5'],
            'Gm': ['G4', 'A#4', 'D5'],
            'G#m': ['G#4', 'B4', 'D#5'],
            'Am': ['A4', 'C5', 'E5'],
            'A#m': ['A#4', 'C#5', 'F5'],
            'Bm': ['B4', 'D5', 'F#5'],
        }
    
    def parse_chord_output(self, file_path):
        """Parse chord-output.txt file to extract chord progression with timing."""
        chords = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Find chord progression section
            progression_match = re.search(r'📊 CHORD PROGRESSION:\s*-+\s*(.*?)(?=\n\||\n🎵|\Z)', content, re.DOTALL)
            if not progression_match:
                print("❌ Could not find chord progression in file")
                return []
            
            progression_text = progression_match.group(1)
            
            # Parse each chord line
            chord_pattern = r'\s*\d+\.\s+(\w+(?:m)?)\s+\|\s+(\d{2}:\d{2}\.\d{3})\s+-\s+(\d{2}:\d{2}\.\d{3})\s+\|\s+Duration:\s+(\d{2}:\d{2}\.\d{3})'
            
            for match in re.finditer(chord_pattern, progression_text):
                chord_name = match.group(1)
                start_time = self.parse_time(match.group(2))
                end_time = self.parse_time(match.group(3))
                duration = self.parse_time(match.group(4))
                
                chords.append({
                    'chord': chord_name,
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': duration
                })
            
            return chords
            
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return []
        except Exception as e:
            print(f"❌ Error parsing file: {e}")
            return []
    
    def parse_time(self, time_str):
        """Convert time string (MM:SS.mmm) to seconds."""
        parts = time_str.split(':')
        minutes = int(parts[0])
        seconds_parts = parts[1].split('.')
        seconds = int(seconds_parts[0])
        milliseconds = int(seconds_parts[1])
        
        return minutes * 60 + seconds + milliseconds / 1000.0
    
    def play_chord(self, chord_name, duration):
        """Play a single chord for the specified duration."""
        if chord_name not in self.chord_notes:
            print(f"⚠️  Unknown chord: {chord_name}, skipping...")
            time.sleep(duration)
            return
        
        notes = self.chord_notes[chord_name]
        print(f"🎸 Playing {chord_name} for {duration:.3f}s")
        
        # Generate and play the chord
        wave = self.synthesizer.generate_chord(notes, duration)
        self.player.play_wave(wave)
    
    def play_progression(self, chords):
        """Play the entire chord progression with proper timing."""
        if not chords:
            print("❌ No chords to play")
            return
        
        print(f"\n🎵 Playing chord progression ({len(chords)} chords)...")
        print("=" * 50)
        
        start_time = time.time()
        
        for i, chord_info in enumerate(chords):
            chord_name = chord_info['chord']
            duration = chord_info['duration']
            
            # Calculate when this chord should start
            target_time = start_time + chord_info['start_time']
            current_time = time.time()
            
            # Wait if we're ahead of schedule
            if current_time < target_time:
                time.sleep(target_time - current_time)
            
            # Play the chord
            self.play_chord(chord_name, duration)
        
        print("=" * 50)
        print("✅ Playback complete!")
    
    def close(self):
        """Clean up resources."""
        try:
            self.player.close_stream()
        except AttributeError:
            # Some versions don't have close_stream method
            pass

def main():
    if len(sys.argv) < 2:
        print("Usage: python guitar_playback.py <chord-output.txt>")
        print("Example: python guitar_playback.py chord-output.txt")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print("🎸 Guitar Chord Playback System")
    print("=" * 40)
    
    # Initialize playback system
    playback = GuitarPlayback()
    
    try:
        # Parse chord progression
        print(f"📖 Reading chord progression from: {file_path}")
        chords = playback.parse_chord_output(file_path)
        
        if not chords:
            print("❌ No valid chords found in file")
            return
        
        print(f"✅ Found {len(chords)} chords")
        
        # Display chord progression
        print("\n📊 Chord Progression:")
        print("-" * 30)
        for i, chord_info in enumerate(chords, 1):
            print(f"{i:2d}. {chord_info['chord']:4s} | {chord_info['duration']:.3f}s")
        
        # Ask user if they want to play
        print("\n🎵 Ready to play! Press Enter to start (or Ctrl+C to cancel)")
        input()
        
        # Play the progression
        playback.play_progression(chords)
        
    except KeyboardInterrupt:
        print("\n⏹️  Playback cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        playback.close()

if __name__ == "__main__":
    main()
