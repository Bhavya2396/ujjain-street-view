# 🎥 How to Upload Your Insta360 X5 Video - Complete Guide

## 📚 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start (5 minutes)](#quick-start)
3. [Detailed Steps](#detailed-steps)
4. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Software You Need:
- ✅ **Insta360 Studio** (download from Insta360.com)
- ✅ **Homebrew** (for Mac) - Install tools
- ✅ **exiftool** - Extract GPS data
- ✅ **ffmpeg** - Video processing

### Install Required Tools:

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install exiftool and ffmpeg
brew install exiftool ffmpeg
```

---

## Quick Start (5 Minutes)

### Option A: Video WITHOUT GPS Data (Easiest)

```bash
# 1. Copy your video to the project folder
cp /path/to/your-video.mp4 "/Users/bhavyasethi/ujjain-street-product /your-video.mp4"

# 2. Update index.html to use your video (I'll do this for you!)

# 3. Done! The app will use the fake route (already works)
```

### Option B: Video WITH GPS Data (Best Experience)

```bash
# 1. Check if your video has GPS
python3 check_gps.py your-video.mp4

# 2. If YES, extract GPS coordinates
python3 extract_gps.py your-video.mp4

# 3. I'll update the app to use real GPS data

# 4. Done! Your video will follow the actual route!
```

---

## Detailed Steps

### Step 1: Export from Insta360 Studio

1. **Open Insta360 Studio**
   - Launch the app
   - Click "Open" or drag your `.insv` file

2. **Export Settings**
   ```
   Format: MP4
   Resolution: 4K (3840x1920) or 5.7K
   Codec: H.264
   Frame Rate: 30fps (or original)
   
   ⚠️ IMPORTANT:
   ☑️ Enable "Export 360° video" (Equirectangular)
   ☑️ Enable "Keep GPS data" or "Keep metadata"
   ```

3. **Export**
   - Click "Export"
   - Wait for processing
   - Save to your Desktop or Downloads

### Step 2: Copy Video to Project

**Method 1: Using Finder**
1. Open Finder
2. Navigate to your exported video
3. Copy it
4. Paste into: `/Users/bhavyasethi/ujjain-street-product /`

**Method 2: Using Terminal**
```bash
# Copy your video
cp ~/Downloads/your-insta360-video.mp4 "/Users/bhavyasethi/ujjain-street-product /my-video.mp4"
```

### Step 3: Check for GPS Data

```bash
# Run the GPS checker
cd "/Users/bhavyasethi/ujjain-street-product "
python3 check_gps.py my-video.mp4
```

**Expected Output:**

✅ **If GPS data found:**
```
🎉 SUCCESS! Your video has GPS data!
📍 You can extract GPS coordinates for the map.
```

⚠️ **If NO GPS data:**
```
⚠️  No GPS data found in standard metadata.
💡 You can still use the video with a manual route!
```

### Step 4A: With GPS Data (Automatic Route)

```bash
# Extract GPS coordinates
python3 extract_gps.py my-video.mp4

# This creates a file: route.json
# Contains all GPS points from your video
```

**I'll then update the code to:**
1. Load `route.json`
2. Draw your actual route on the map
3. Sync video with real GPS coordinates

### Step 4B: Without GPS Data (Manual Route)

**No problem!** We have two options:

**Option 1: Use Fake Route (Current Setup)**
- Video works immediately
- Route is hardcoded (Ujjain, India)
- Good for testing

**Option 2: Create Manual Route**
I can add a feature where you:
1. Click on map to draw your route
2. Save the route
3. Video syncs to your drawn path

### Step 5: Update the App

Tell me:
1. **Your video filename** (e.g., `street-tour.mp4`)
2. **Does it have GPS?** (YES/NO)
3. **What's the video duration?** (approximate)

I'll update `index.html` to use your video!

---

## What I'll Do For You

Once you upload your video, I'll:

### 1. Update Video Source
```javascript
// Change from:
<source src="Street2.mp4" type="video/mp4">

// To:
<source src="your-video.mp4" type="video/mp4">
```

### 2. Load GPS Route (if available)
```javascript
// Load your real GPS data
fetch('route.json')
  .then(response => response.json())
  .then(data => {
    // Draw actual route on map
    drawRoute(data.features[0].geometry.coordinates);
  });
```

### 3. Center Map on Your Location
```javascript
// Automatically center map on your route
map.fitBounds(routeBounds);
```

---

## Troubleshooting

### Problem: "exiftool: command not found"
**Solution:**
```bash
brew install exiftool
```

### Problem: "No GPS data found"
**Possible Reasons:**
1. GPS was disabled on camera
2. Recording was indoors
3. Video was heavily edited
4. GPS didn't have time to lock

**Solutions:**
- Re-export from Insta360 Studio with "Keep GPS"
- Use manual route drawing feature
- Check if raw `.insv` file has GPS

### Problem: Video doesn't load
**Checklist:**
- ✅ Is video in correct folder?
- ✅ Is filename correct in `index.html`?
- ✅ Is video format MP4?
- ✅ Is it 360° equirectangular?
- ✅ Is dev server running?

### Problem: Video plays but 360° doesn't work
**Fix:** Video must be:
- Equirectangular projection
- 2:1 aspect ratio (e.g., 3840x1920)
- Full 360° (not cropped)

---

## Next Steps

1. **Upload your video** to the project folder
2. **Run the GPS checker:**
   ```bash
   python3 check_gps.py your-video.mp4
   ```
3. **Tell me the results** - I'll handle the rest!

---

## Examples

### Example 1: Video WITH GPS
```bash
$ python3 check_gps.py tokyo-ride.mp4
🎉 SUCCESS! Your video has GPS data!

$ python3 extract_gps.py tokyo-ride.mp4
✅ GPS data saved to: route.json
📊 Summary:
   - GPS points: 342
   - First point: 35.689487, 139.691711
   - Last point: 35.681382, 139.767125
```

### Example 2: Video WITHOUT GPS
```bash
$ python3 check_gps.py city-tour.mp4
⚠️  No GPS data found

# No problem! Use manual route or fake route
# Video still works perfectly for 360° viewing
```

---

## FAQ

**Q: What if my video is too large (>1GB)?**
A: No problem! The server handles large files. Consider:
- Compressing to 4K instead of 5.7K
- Using H.265 codec for smaller file size

**Q: Can I use multiple videos?**
A: Yes! I can add a video switcher. Upload multiple videos and switch between them.

**Q: What about privacy (faces, license plates)?**
A: I can add automatic blurring in Phase 2 using AI.

**Q: Can I edit the route after uploading?**
A: Yes! I can add route editing tools.

---

## Ready to Upload?

Just tell me:
1. "I've copied my video to the folder"
2. The filename
3. Results from `check_gps.py`

And I'll integrate it! 🚀

