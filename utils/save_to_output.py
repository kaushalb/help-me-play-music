#!/usr/bin/env python3
"""
Output Utilities for Chord Detection
Contains functions for formatting and saving chord analysis results to files.
"""

import os

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
