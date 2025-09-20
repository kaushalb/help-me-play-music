#!/usr/bin/env python3
"""
MP3 Chord Detection Script
Analyzes MP3 audio files to extract chord progressions using chromagram analysis.
Supports both file analysis and live audio recording.
"""

import argparse
import sys
import os
from ChordDetector import ChordDetector
from utils.save_to_output import format_time, create_chord_timeline, save_results_to_file, print_analysis_results

def get_user_choice():
    """Get user's choice for input mode."""
    print("\n🎵 Chord Detection Tool")
    print("="*50)
    print("Choose input mode:")
    print("1. Analyze audio file (MP3, WAV, FLAC, M4A)")
    print("2. Record live audio from microphone")
    print("3. Play back chords from existing output file")
    
    while True:
        try:
            choice = input("\nEnter your choice (1, 2, or 3): ").strip()
            if choice in ['1', '2', '3']:
                return int(choice)
            else:
                print("Please enter 1, 2, or 3")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

def get_file_path():
    """Get file path from user."""
    while True:
        file_path = input("Enter the path to your audio file: ").strip()
        
        # Remove quotes if present
        file_path = file_path.strip('"\'')
        
        if os.path.exists(file_path):
            if file_path.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
                return file_path
            else:
                print("Warning: File doesn't appear to be an audio file.")
                confirm = input("Continue anyway? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    return file_path
        else:
            print(f"File not found: {file_path}")
            print("Please check the path and try again.")

def interactive_mode():
    """Run in interactive mode with user choice."""
    choice = get_user_choice()
    
    # Create chord detector
    detector = ChordDetector()
    
    try:
        if choice == 1:
            # File analysis mode
            file_path = get_file_path()
            print(f"\n🎵 Analyzing file: {os.path.basename(file_path)}")
            results = detector.analyze_mp3(file_path)
            source_name = file_path
            
        elif choice == 2:
            # Live recording mode
            print(f"\n🎤 Live recording mode")
            results = detector.analyze_live_audio()
            source_name = results.get('filename', 'live_recording') if results else 'live_recording'
            
        else:
            # Playback mode
            from guitar_playback import GuitarPlayback
            
            output_file = input("Enter path to chord output file (default: chord-output.txt): ").strip()
            if not output_file:
                output_file = 'chord-output.txt'
            
            print("🎸 Guitar Chord Playback System")
            print("=" * 40)
            
            playback = GuitarPlayback()
            try:
                print(f"📖 Reading chord progression from: {output_file}")
                chords = playback.parse_chord_output(output_file)
                
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
            
            return
        
        if results:
            print_analysis_results(results, source_name)
            
            # Ask if user wants to save results
            save_choice = input("\nSave results to file? (y/n): ").strip().lower()
            if save_choice in ['y', 'yes']:
                output_file = input("Output filename (press Enter for 'chord-output.txt'): ").strip()
                if not output_file:
                    output_file = 'chord-output.txt'
                save_results_to_file(results, source_name, output_file)
        else:
            print("No results to display.")
            
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Analyze audio for chord progressions')
    parser.add_argument('file_path', nargs='?', help='Path to the audio file to analyze (optional)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--output', '-o', default='chord-output.txt', help='Output file for results (default: chord-output.txt)')
    parser.add_argument('--save', '-s', action='store_true', help='Save results to output file')
    parser.add_argument('--live', '-l', action='store_true', help='Record live audio from microphone')
    parser.add_argument('--playback', '-p', help='Play back chords from output file using guitar sounds')
    
    args = parser.parse_args()
    
    # Handle playback mode
    if args.playback:
        from guitar_playback import GuitarPlayback
        
        print("🎸 Guitar Chord Playback System")
        print("=" * 40)
        
        playback = GuitarPlayback()
        try:
            print(f"📖 Reading chord progression from: {args.playback}")
            chords = playback.parse_chord_output(args.playback)
            
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
        
        return
    
    # If no arguments provided, run in interactive mode
    if not args.file_path and not args.live:
        interactive_mode()
        return
    
    # Create chord detector
    detector = ChordDetector()
    
    try:
        if args.live:
            # Live recording mode
            print("🎤 Live recording mode")
            results = detector.analyze_live_audio()
            source_name = results.get('filename', 'live_recording') if results else 'live_recording'
        else:
            # File analysis mode
            if not os.path.exists(args.file_path):
                print(f"Error: File '{args.file_path}' not found.")
                sys.exit(1)
            
            if not args.file_path.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
                print("Warning: File doesn't appear to be an audio file. Proceeding anyway...")
            
            results = detector.analyze_mp3(args.file_path)
            source_name = args.file_path
        
        if results:
            print_analysis_results(results, source_name)
            
            # Save results to file if requested
            if args.save:
                save_results_to_file(results, source_name, args.output)
        else:
            print("No results to display.")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()