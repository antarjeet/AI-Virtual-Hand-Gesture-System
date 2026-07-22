# AI Virtual Mouse - Project Persona

## Project Overview
**AI Virtual Mouse** is a Python-based hand gesture recognition system that enables touchless control of computer peripherals using a webcam and AI-powered hand tracking. The project leverages MediaPipe for hand detection and implements gesture recognition to control mouse movements, mouse clicks, and system volume.

---

## Project Purpose
Replace traditional input devices (mouse, keyboard) with hand gestures captured through a webcam, enabling:
- **Virtual Mouse Control**: Move cursor and click using hand gestures
- **Volume Control**: Adjust system volume using thumb-to-index finger distance
- **Gesture Recognition**: Detect which fingers are extended and their positions

---

## Core Components

### 1. **HandTrackingModule.py**
**Role**: Core hand detection engine (reusable module)

**HandDetector Class Methods**:
- `find_hands(img, draw=True)`: Detects hands using MediaPipe and optionally draws landmarks
- `find_position(img, handno=0, draw=True)`: Returns list of landmark coordinates and bounding box
- `fingersUp()`: Returns array of 5 values (0/1) indicating which fingers are extended
- `find_Distance(p1, p2, img, draw=True, r=15, t=3)`: Calculates Euclidean distance between two landmarks

**Key Data**:
- `tipIds = [4, 8, 12, 16, 20]` - Landmark IDs for finger tips
- Supports single hand detection (first hand by default)

**Issues Found**:
- `main()` function has typo: `cap.distroyAllWindowa()` (should be `destroyAllWindows()`)

---

### 2. **AI_virtual_mouse.py**
**Role**: Mouse cursor and click control application

**Functionality**:
- Maps hand position to screen coordinates with smoothing
- **Single Index Finger**: Move mouse cursor
- **Index + Middle Fingers**: Click mode
  - Distance < 40px triggers mouse click
  - Distance > 40px = ready to click

**Key Features**:
- Frame rate display (FPS)
- Gesture detection frame (purple rectangle)
- Smoothing factor: 7 (reduces jitter)
- Screen mapping with interpolation

**Dependencies**:
- `autopy.mouse.move()` - Move cursor
- `autopy.mouse.click()` - Trigger click

---

### 3. **HandTracking.py**
**Role**: Hand-based system volume control application

**Functionality**:
- Uses thumb (landmark 4) and index finger (landmark 8)
- Maps finger distance to volume level
  - Distance 50-218px maps to min-max volume
- Visual feedback: vertical volume bar (green)
- Shows volume percentage on screen

**Key Features**:
- System volume integration via Windows COM API (pycaw)
- Real-time volume display and bar visualization
- FPS counter
- Green circle feedback when fingers are close (< 50px)

**Dependencies**:
- `pycaw` - Windows audio control
- `comtypes` - COM interface access

---

### 4. **hand_volume_control.py**
**Role**: Object-oriented version of volume control (class-based)

**HandVolumeControl Class**:
- Encapsulates all volume control functionality
- Methods mirror HandTracking.py but in class structure
- Better for integration into larger applications

**Main Method**: `control_volume()` - Main control loop

---

### 5. **HandTrackingMin.py**
**Role**: Minimal hand tracking example for testing

**Functionality**:
- Basic MediaPipe implementation
- Draws landmarks and connections
- Prints landmark coordinates to console
- Simple FPS display

**Purpose**: Educational/debugging reference

---

### 6. **combined_gesture_control.py** ⭐ NEW
**Role**: Unified application combining mouse and volume control

**Functionality**:
- **Gesture-based mode switching** - detects finger combinations to activate features
- **Mouse Move Mode** (Index finger only):
  - Moves cursor smoothly across screen
  - Purple frame indicates active area
- **Mouse Click Mode** (Index + Middle fingers):
  - Green visual feedback
  - Triggers click when fingers < 40px apart
- **Volume Control Mode** (Thumb + Index fingers):
  - Cyan visual feedback
  - Adjusts system volume based on thumb-to-index distance
  - Displays live volume percentage and bar
  - Green circle when fingers are close

**Mode Display**:
- Real-time mode indicator at top of window
- FPS counter
- On-screen instructions for all gestures

**Key Features**:
- Single application replaces need to run separate mouse/volume apps
- Intelligent gesture recognition automatically switches modes
- Combined visual feedback (different colors for each mode)
- Full integration of both audio and mouse control

---

### 8. **ultimate_gesture_control.py** ⭐ ALL-IN-ONE
**Role**: Ultimate unified application combining mouse, keyboard, AND volume control

**Functionality**:
- **Single application** with intelligent gesture-based mode detection
- All three features (mouse, keyboard, volume) in one seamless window
- Automatic mode switching based on finger positions
- Enhanced keyboard with visual feedback and real-time text display

**Gesture-Based Modes**:
1. **Mouse Move Mode** (Index finger only)
   - Controls cursor position
   - Purple frame shows active area
   - Smooth motion interpolation

2. **Mouse Click Mode** (Index + Middle fingers)
   - Green visual feedback
   - Triggers click when distance < 40px

3. **Keyboard Mode** (Middle finger only)
   - On-screen QWERTY keyboard with dark background
   - Select keys with **middle finger** (cyan circle)
   - **Bring index finger close to middle finger** (< 35px) to press key
   - Green highlight shows pressed key
   - Real-time typed text displayed in large cyan box above keyboard
   - Full alphabet + punctuation + DEL/SPACE keys
   - Automatic debounce to prevent duplicate presses

4. **Volume Control Mode** (Thumb + Index fingers)
   - Cyan visual elements
   - Adjust system volume by changing distance
   - Live percentage and visual bar display

**Enhanced Features**:
- Real-time mode indicator at top
- FPS counter
- **Improved keyboard with better visual design**:
  - Dark keyboard background for better visibility
  - Larger text display area
  - Better key highlighting (cyan for selected, green for pressed)
  - Smooth key press detection with debouncing
- **Tab/Window switching**:
  - Open hand → Next window (Alt+Tab)
  - Closed hand → Previous window (Alt+Shift+Tab)
  - 0.5s debounce to prevent multiple rapid switches
- Live text display during keyboard mode
- Color-coded feedback for each mode
- 'c' key clears keyboard text
- ESC to exit

**Keyboard Interaction**:
```
Step 1: Show only middle finger (other fingers down) → Keyboard mode activates
Step 2: Move middle finger to select key (cyan highlight)
Step 3: Bring index finger close to middle finger (< 35px) → Key presses
Step 4: Text appears in display box above keyboard
Step 5: Repeat or switch modes by changing finger positions
```

**Tab Switching Gestures**:
```
Open Hand (all 5 fingers extended) → Alt+Tab (Next window/tab)
                                      Yellow indicator shown

Closed Hand (all fingers down) → Alt+Shift+Tab (Previous window/tab)
                                 Orange indicator shown
```

---

### 9. **virtual_keyboard.py** ⭐ KEYBOARD-ONLY
**Role**: Standalone hand gesture-based virtual keyboard application

**VirtualKeyboard Class**:
- On-screen QWERTY keyboard with 3 rows
- Hand gesture detection for key selection and pressing
- Real-time text display showing typed content

**Keyboard Layout**:
```
Row 1: Q W E R T Y U I O P
Row 2: A S D F G H J K L DEL
Row 3: Z X C V B N M . , SPACE
```

**Gesture Controls**:
- **Index finger alone**: Hover and select keys (purple circle)
- **Index + Middle fingers close** (< 40px): Press/activate key (green circle)
- **Cyan highlight**: Selected key
- **Green fill**: Key pressed

**Features**:
- Real-time typed text display at top
- Automatic text scrolling for long input
- DEL key: Delete last character
- SPACE key: Add space
- Clear text with 'c' key
- Visual feedback for selection and activation
- FPS counter
- Press duration: 0.3 seconds (configurable)

**Key Dimensions**:
- Width: 60px, Height: 50px
- 2px gap between keys
- Starts at position (20, 250)

---

### 7. **main.py**
**Role**: Template file (default PyCharm sample)

**Status**: Unused placeholder

---

## Technical Architecture

```
MediaPipe Hand Detection
        ↓
HandDetector (HandTrackingModule.py)
        ↓
┌─────────────────────────────────────────┐
│  ULTIMATE APP ⭐⭐⭐ (All-in-One)      │
│  Mouse + Keyboard + Volume              │
│  (ultimate_gesture_control.py)          │
└─────────────────────────────────────────┘
        ↓
    ┌───────────────────────┐
    │ COMBINED APP ⭐       │
    │ (Mouse + Volume)      │
    ├───────┬───────┬───────┤
    ↓       ↓       ↓       ↓
 Mouse   Mouse  Volume  Keyboard
 Move    Click  Control  (Standalone)
```

**Architecture Comparison**:
- **ultimate_gesture_control.py**: All features in one app with gesture-based mode detection
- **combined_gesture_control.py**: Mouse + Volume in one app
- **virtual_keyboard.py**: Keyboard-only standalone
- **Individual apps**: AI_virtual_mouse.py, HandTracking.py, etc. (legacy)

**Mode Detection Logic**:
- Analyzes which fingers are extended
- Automatically switches between 4 modes
- Provides real-time visual feedback for each mode



### Hand Landmark IDs (MediaPipe)
- 0: Wrist
- 1-4: Thumb (4 = tip)
- 5-8: Index (8 = tip)
- 9-12: Middle (12 = tip)
- 13-16: Ring (16 = tip)
- 17-20: Pinky (20 = tip)

---

## Dependencies

### Required Packages
```
opencv-python (cv2)      - Video capture and image processing
mediapipe (mp)           - Hand detection and landmark tracking
numpy                    - Numerical operations
autopy                   - Mouse control (virtual mouse only)
pyautogui                - Keyboard automation (tab switching)
pycaw                    - Windows audio control (volume control only)
comtypes                 - COM interface for Windows audio
```

### Installation
```bash
pip install opencv-python mediapipe numpy autopy pyautogui pycaw comtypes
```

---

## Configuration Parameters

### Virtual Mouse (AI_virtual_mouse.py)
- `wcam, hcam = 640, 480` - Webcam resolution
- `frameR = 100` - Gesture frame border (pixels)
- `smoothening = 7` - Mouse movement smoothing factor
- Click threshold: `40px` (finger distance)

### Volume Control (HandTracking.py)
- `wcam, hcam = 640, 480` - Webcam resolution
- Distance range: `[50, 218]px` - Maps to volume
- Volume bar position: `(50, 150) to (85, 400)` - x, y coordinates

---

## Usage

### 🚀 Run Ultimate Gesture Control (SUPER RECOMMENDED) ⭐
```bash
python ultimate_gesture_control.py
```
**All-in-One Gesture Controls**:
- **Index finger alone**: Move mouse cursor (purple)
- **Index + Middle fingers (< 40px apart)**: Click mouse (green)
- **Middle finger alone**: Virtual keyboard mode (cyan)
  - Move middle finger to select keys
  - Bring index finger close to middle (< 35px) to press
- **Thumb + Index fingers**: Volume control (cyan)
- **Open hand** (all 5 fingers extended): Switch to next tab/window (Alt+Tab)
- **Closed hand** (all fingers down): Switch to previous tab/window (Alt+Shift+Tab)
- Press 'c' to clear keyboard text
- Press ESC to exit

**Features**:
- ✅ Single window with ALL 3 features
- ✅ Automatic mode switching
- ✅ Real-time mode indicator
- ✅ Enhanced keyboard with dark background
- ✅ Live typed text display
- ✅ Color-coded feedback
- ✅ FPS counter
- ✅ Smooth debounced key presses

---

### 🎯 Run Combined Gesture Control
```bash
python combined_gesture_control.py
```
**Gesture Controls**:
- **Index finger extended alone**: Move mouse cursor
- **Index + Middle fingers extended**: Click mode (click when < 40px apart)
- **Thumb + Index fingers extended**: Volume control (distance = volume level)
- Press ESC to exit

**Visual Feedback**:
- Purple frame: Mouse move area
- Green circle: Click ready/Volume min detected
- Cyan elements: Volume control active
- Mode indicator at top of screen

---

### 💻 Run Virtual Keyboard (Standalone)
```bash
python virtual_keyboard.py
```
**Gesture Controls**:
- **Index finger alone**: Select/hover over keys (purple circle)
- **Index + Middle fingers close (< 40px)**: Press key (green circle and highlighting)
- Typed text appears in green box at top
- Press 'c' to clear all text
- Press ESC to exit

**Keyboard Features**:
- QWERTY layout with 3 rows
- DEL key: Delete last character
- SPACE key: Add space
- Real-time text display
- Live FPS counter

---

### Run Virtual Mouse (Legacy)
```bash
python AI_virtual_mouse.py
```
**Controls**:
- Index finger extended: Move cursor
- Index + Middle extended: Click mode
- Press ESC to exit

### Run Volume Control (Legacy)
```bash
python HandTracking.py
```
**Controls**:
- Thumb and index finger: Adjust volume
- Press ESC to exit

### Run Class-Based Volume Control
```bash
python hand_volume_control.py
```

### Test Hand Tracking
```bash
python HandTrackingMin.py
```


---

## Known Issues

### HandTrackingModule.py
1. **Line 148**: Typo in cleanup method
   ```python
   cap.distroyAllWindowa()  # Wrong
   cap.destroyAllWindows()  # Correct
   ```
2. **Line 124**: Logic error - should be `if len(lmList) != 0` (not `==`)

### HandTracking.py
1. **Line 32**: Logic error - condition should be `if len(lmList) != 0` (not `<= 0`)

---

## Performance Considerations

- **FPS**: Typically 20-30 FPS depending on hardware
- **Latency**: ~100-150ms from hand movement to cursor response (due to smoothing)
- **Accuracy**: Works best with good lighting and contrasting hand background
- **Resolution**: 640x480 is optimal balance between accuracy and performance

---

## Future Enhancements

1. **Keyboard Improvements**:
   - Multi-language keyboard layouts (AZERTY, Dvorak, etc.)
   - Gesture-based number pad
   - Function keys (F1-F12) and special keys
   - Shift/Ctrl modifiers using additional fingers
   - Swipe typing for faster input

2. **Mouse Enhancements**:
   - Drag and drop support
   - Scroll wheel control
   - Right-click gestures
   - Double-click detection

3. **System Control**:
   - Window management gestures
   - Application switching
   - Desktop navigation

4. **ML & Optimization**:
   - Multi-hand gesture recognition
   - Custom gesture training
   - Model optimization for faster inference
   - Gesture confidence scoring

5. **UI/UX**:
   - Configuration file for parameter tuning
   - Gesture learning/recording system
   - Keyboard theme customization
   - Fullscreen keyboard mode

---

## Summary of Capabilities

| Feature | Status | File | Use Case |
|---------|--------|------|----------|
| **Virtual Mouse** | ✅ Complete | `AI_virtual_mouse.py` | Point & click control |
| **Volume Control** | ✅ Complete | `HandTracking.py` | Audio adjustment |
| **Keyboard (Standalone)** | ✅ Complete | `virtual_keyboard.py` | Text input only |
| **Combined (Mouse + Volume)** | ✅ Complete | `combined_gesture_control.py` | Mouse + audio |
| **Ultimate (All 4 Features)** | ✅ Complete | `ultimate_gesture_control.py` | Full control suite |
| **Tab Switching** | ✅ Complete | `ultimate_gesture_control.py` | Window/tab navigation |
| **Class-Based Volume** | ✅ Complete | `hand_volume_control.py` | OOP implementation |
| **Hand Tracking Core** | ✅ Complete | `HandTrackingModule.py` | Detection engine |
| **Test/Debug** | ✅ Complete | `HandTrackingMin.py` | Minimal reference |

---

## Platform Support

- **Windows**: ✅ Full support (audio control via pycaw)
- **macOS**: ⚠️ Partial (audio control requires adaptation)
- **Linux**: ⚠️ Partial (audio control requires adaptation)

---

## Project Status
**Active Development** - Core functionality working, minor bugs to fix, potential for optimization and feature expansion.
