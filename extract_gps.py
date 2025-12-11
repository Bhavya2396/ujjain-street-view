#!/usr/bin/env python3
"""
Extract GPS coordinates from Insta360 video and create route JSON
"""

import subprocess
import sys
import json
import re
from datetime import datetime

def extract_gps_to_json(video_file, output_file='route.json'):
    """Extract GPS data and save as JSON for the web app"""
    
    print(f"🚀 Extracting GPS from: {video_file}\n")
    print("=" * 60)
    
    try:
        # Use exiftool to extract GPS data
        print("\n📊 Extracting GPS data with exiftool...\n")
        result = subprocess.run(
            ['exiftool', '-ee', '-G3', '-n', '-j', video_file],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print("❌ Error running exiftool")
            return False
        
        # Parse JSON output
        data = json.loads(result.stdout)
        
        if not data:
            print("❌ No metadata found")
            return False
        
        # Extract GPS coordinates
        gps_points = []
        metadata = data[0] if isinstance(data, list) else data
        
        # Look for GPS data in various formats
        lat = metadata.get('GPSLatitude') or metadata.get('Composite:GPSLatitude')
        lon = metadata.get('GPSLongitude') or metadata.get('Composite:GPSLongitude')
        
        if lat and lon:
            # Single GPS point
            gps_points.append({
                'lat': lat,
                'lng': lon,
                'time': 0
            })
            print(f"  ✅ Found GPS: {lat:.6f}, {lon:.6f}")
        
        # Check for GPS track (multiple points over time)
        # Insta360 sometimes stores this differently
        for key, value in metadata.items():
            if 'gps' in key.lower() and isinstance(value, list):
                print(f"  📍 Found GPS track: {key} ({len(value)} points)")
                # Process track data here
        
        if not gps_points:
            print("\n⚠️  Could not extract GPS coordinates")
            print("💡 The video might not have GPS data embedded")
            return False
        
        # Create route JSON
        route_data = {
            'type': 'FeatureCollection',
            'features': [{
                'type': 'Feature',
                'properties': {
                    'name': 'GPS Track',
                    'video_file': video_file,
                    'extracted_at': datetime.now().isoformat()
                },
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [[p['lng'], p['lat']] for p in gps_points]
                }
            }]
        }
        
        # Save to JSON file
        with open(output_file, 'w') as f:
            json.dump(route_data, f, indent=2)
        
        print(f"\n✅ SUCCESS! GPS data saved to: {output_file}")
        print(f"\n📊 Summary:")
        print(f"   - GPS points: {len(gps_points)}")
        print(f"   - First point: {gps_points[0]['lat']:.6f}, {gps_points[0]['lng']:.6f}")
        if len(gps_points) > 1:
            print(f"   - Last point: {gps_points[-1]['lat']:.6f}, {gps_points[-1]['lng']:.6f}")
        
        print("\n" + "=" * 60)
        print("\n🎯 Next Steps:")
        print("   1. I'll update the web app to use this GPS data")
        print("   2. Your video will be mapped to the actual route!")
        print("   3. Run the dev server to see it in action")
        print("\n" + "=" * 60)
        
        return True
        
    except FileNotFoundError:
        print("❌ exiftool not installed")
        print("💡 Install with: brew install exiftool")
        return False
    except json.JSONDecodeError:
        print("❌ Could not parse exiftool output")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 extract_gps.py your-video.mp4")
        print("Optional: python3 extract_gps.py your-video.mp4 custom-route.json")
        sys.exit(1)
    
    video_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'route.json'
    
    extract_gps_to_json(video_file, output_file)

