#!/usr/bin/env python3
"""
MP3 Chord Detection Script
Analyzes MP3 audio files to extract chord progressions using chromagram analysis.
"""

import argparse
import sys
import os
from ChordDetector import ChordDetector
from utils.save_to_output import format_time, create_chord_timeline, save_results_to_file, print_analysis_results


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