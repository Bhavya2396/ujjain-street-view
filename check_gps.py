#!/usr/bin/env python3
"""
Simple script to check if an Insta360 video has GPS data
"""

import subprocess
import sys
import json
import re

def check_gps_data(video_file):
    """Check if video has GPS metadata"""
    
    print(f"🔍 Checking GPS data in: {video_file}\n")
    print("=" * 60)
    
    try:
        # Try using exiftool (most reliable)
        print("\n📊 Method 1: Using exiftool...")
        result = subprocess.run(
            ['exiftool', '-ee', '-G3', video_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            output = result.stdout
            
            # Look for GPS-related tags
            gps_keywords = ['GPS', 'GPSLatitude', 'GPSLongitude', 'Location']
            found_gps = False
            
            for line in output.split('\n'):
                for keyword in gps_keywords:
                    if keyword in line and ':' in line:
                        print(f"  ✅ {line.strip()}")
                        found_gps = True
            
            if found_gps:
                print("\n🎉 SUCCESS! Your video has GPS data!")
                print("\n📍 You can extract GPS coordinates for the map.")
                return True
            else:
                print("\n⚠️  No GPS data found in standard metadata.")
                
    except FileNotFoundError:
        print("  ❌ exiftool not installed")
        print("  💡 Install with: brew install exiftool")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Try using ffmpeg
    try:
        print("\n📊 Method 2: Using ffmpeg...")
        result = subprocess.run(
            ['ffmpeg', '-i', video_file, '-f', 'ffmetadata', '-'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stderr + result.stdout
        
        if 'location' in output.lower() or 'gps' in output.lower():
            print("  ✅ Found GPS-related metadata!")
            return True
        else:
            print("  ⚠️  No GPS metadata found")
            
    except FileNotFoundError:
        print("  ❌ ffmpeg not installed")
        print("  💡 Install with: brew install ffmpeg")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("\n💡 RECOMMENDATIONS:")
    print("   1. Make sure GPS was enabled when recording")
    print("   2. Export from Insta360 Studio with 'Keep GPS data'")
    print("   3. Check if the file is the RAW .insv file or exported MP4")
    print("   4. You can still use the video with a manual route!")
    print("\n" + "=" * 60)
    
    return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 check_gps.py your-video.mp4")
        sys.exit(1)
    
    video_file = sys.argv[1]
    check_gps_data(video_file)

