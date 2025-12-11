#!/usr/bin/env python3
"""
Simple HTTP Server with Range Request Support
Required for video seeking to work properly
"""

import os
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class RangeRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler with proper Range request support for video seeking"""
    
    def end_headers(self):
        """Add CORS headers and cache control"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Range')
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests with Range support"""
        path = self.translate_path(self.path)
        
        # Check if file exists
        if not os.path.exists(path) or not os.path.isfile(path):
            return super().do_GET()
        
        # Get file size
        file_size = os.path.getsize(path)
        
        # Check for Range header
        range_header = self.headers.get('Range')
        
        if range_header:
            # Parse range header (e.g., "bytes=1024-2047" or "bytes=1024-")
            range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
            
            if range_match:
                start = int(range_match.group(1))
                end = range_match.group(2)
                end = int(end) if end else file_size - 1
                
                # Ensure valid range
                if start >= file_size:
                    self.send_error(416, "Requested Range Not Satisfiable")
                    return
                
                if end >= file_size:
                    end = file_size - 1
                
                length = end - start + 1
                
                # Send 206 Partial Content response
                self.send_response(206)
                self.send_header('Content-Type', self.guess_type(path))
                self.send_header('Content-Length', str(length))
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
                self.end_headers()
                
                # Send the requested range
                try:
                    with open(path, 'rb') as f:
                        f.seek(start)
                        remaining = length
                        while remaining > 0:
                            chunk_size = min(8192, remaining)
                            chunk = f.read(chunk_size)
                            if not chunk:
                                break
                            try:
                                self.wfile.write(chunk)
                            except (BrokenPipeError, ConnectionResetError):
                                # Client disconnected, which is normal for range requests
                                break
                            remaining -= len(chunk)
                except Exception as e:
                    print(f"Error serving range request: {e}")
                
                return
        
        # No range header, send entire file
        self.send_response(200)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Length', str(file_size))
        self.end_headers()
        
        try:
            with open(path, 'rb') as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        # Client disconnected
                        break
        except Exception as e:
            print(f"Error serving file: {e}")
    
    def log_message(self, format, *args):
        """Custom logging to reduce noise"""
        # Only log non-range requests and errors
        if "206" not in str(args) and "Range" not in str(args):
            super().log_message(format, *args)


def run_server(port=8080):
    """Start the HTTP server with Range request support"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, RangeRequestHandler)
    
    print(f"╔═══════════════════════════════════════════════════════╗")
    print(f"║  🎬 360° Street View Server (Range Requests Enabled) ║")
    print(f"╚═══════════════════════════════════════════════════════╝")
    print(f"")
    print(f"  📍 Server running at: http://localhost:{port}")
    print(f"  📁 Serving from: {os.getcwd()}")
    print(f"  🎥 Video seeking: ENABLED")
    print(f"")
    print(f"  Press Ctrl+C to stop the server")
    print(f"")
    print(f"─────────────────────────────────────────────────────────")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n\n✓ Server stopped")
        httpd.shutdown()


if __name__ == '__main__':
    run_server(8080)


