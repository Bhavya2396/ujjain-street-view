#!/usr/bin/env python3
"""
Convert GPX file to GeoJSON for the web app
"""

import xml.etree.ElementTree as ET
import json
import sys
import math

def calculate_heading(lat1, lon1, lat2, lon2):
    """Calculate compass heading (bearing) between two GPS points in degrees (0-360)"""
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    Δλ = math.radians(lon2 - lon1)
    
    y = math.sin(Δλ) * math.cos(φ2)
    x = math.cos(φ1) * math.sin(φ2) - math.sin(φ1) * math.cos(φ2) * math.cos(Δλ)
    
    heading = math.degrees(math.atan2(y, x))
    return (heading + 360) % 360  # Normalize to 0-360


def get_compass_direction(heading):
    """Convert heading degrees to compass direction (N, NE, E, etc.)"""
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = round(heading / 45) % 8
    return directions[index]


def parse_gpx_to_geojson(gpx_file, output_file='route.json'):
    """Parse GPX file and convert to GeoJSON with heading data"""
    
    print(f"📍 Parsing GPX file: {gpx_file}\n")
    
    try:
        # Parse GPX XML
        tree = ET.parse(gpx_file)
        root = tree.getroot()
        
        # GPX namespace
        ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
        
        # Extract track points
        trackpoints = []
        
        for trkpt in root.findall('.//gpx:trkpt', ns):
            lat = float(trkpt.get('lat'))
            lon = float(trkpt.get('lon'))
            
            # Extract elevation and time if available
            ele_elem = trkpt.find('gpx:ele', ns)
            time_elem = trkpt.find('gpx:time', ns)
            
            ele = float(ele_elem.text) if ele_elem is not None else 0
            time = time_elem.text if time_elem is not None else None
            
            trackpoints.append({
                'lat': lat,
                'lon': lon,
                'ele': ele,
                'time': time
            })
        
        if not trackpoints:
            print("❌ No trackpoints found in GPX file")
            return False
        
        print(f"✅ Found {len(trackpoints)} GPS points\n")
        
        # Calculate heading (compass direction) for each trackpoint
        print("📐 Calculating vehicle heading from GPS track...")
        headings = []
        
        for i in range(len(trackpoints) - 1):
            pt1 = trackpoints[i]
            pt2 = trackpoints[i + 1]
            
            heading = calculate_heading(
                pt1['lat'], pt1['lon'],
                pt2['lat'], pt2['lon']
            )
            headings.append(heading)
        
        # Last point uses same heading as previous point
        if headings:
            headings.append(headings[-1])
        else:
            headings.append(0)
        
        print(f"✅ Calculated headings (range: {min(headings):.1f}° - {max(headings):.1f}°)\n")
        
        # Create GeoJSON with heading data
        coordinates = [[pt['lon'], pt['lat']] for pt in trackpoints]
        
        geojson = {
            'type': 'FeatureCollection',
            'features': [{
                'type': 'Feature',
                'properties': {
                    'name': 'Insta360 GPS Track',
                    'trackpoints': len(trackpoints),
                    'source': gpx_file,
                    'headings': headings,  # Add heading data for each point
                    'times': [pt['time'] for pt in trackpoints]  # Add timestamps
                },
                'geometry': {
                    'type': 'LineString',
                    'coordinates': coordinates
                }
            }]
        }
        
        # Save to JSON
        with open(output_file, 'w') as f:
            json.dump(geojson, f, indent=2)
        
        # Print summary
        print("=" * 60)
        print("📊 GPS Track Summary:")
        print("=" * 60)
        print(f"  Total Points: {len(trackpoints)}")
        print(f"  Start: {trackpoints[0]['lat']:.6f}, {trackpoints[0]['lon']:.6f}")
        print(f"  End: {trackpoints[-1]['lat']:.6f}, {trackpoints[-1]['lon']:.6f}")
        print(f"  Initial Heading: {headings[0]:.1f}° ({get_compass_direction(headings[0])})")
        print(f"  Average Heading: {sum(headings)/len(headings):.1f}°")
        
        if trackpoints[0]['ele'] and trackpoints[-1]['ele']:
            ele_change = trackpoints[-1]['ele'] - trackpoints[0]['ele']
            print(f"  Elevation: {trackpoints[0]['ele']:.1f}m → {trackpoints[-1]['ele']:.1f}m ({ele_change:+.1f}m)")
        
        print(f"\n✅ GeoJSON saved to: {output_file}")
        print(f"✅ Heading data included (for accurate 3D marker placement)")
        print("=" * 60)
        
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {gpx_file}")
        return False
    except ET.ParseError as e:
        print(f"❌ Error parsing GPX file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 parse_gpx.py input.gpx [output.json]")
        sys.exit(1)
    
    gpx_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'route.json'
    
    success = parse_gpx_to_geojson(gpx_file, output_file)
    sys.exit(0 if success else 1)

