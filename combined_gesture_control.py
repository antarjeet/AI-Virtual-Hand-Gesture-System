import cv2
import numpy as np
import time
import autopy
import math
import pyautogui
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandTrackingModule as htm

###############
# Screen & Camera Settings
wcam, hcam = 640, 480
frameR = 100
smoothening = 7
###############

# Time variables
cTime = 0
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

# Initialize hand detector
detector = htm.HandDetector()

# Get screen dimensions
wScr, hScr = autopy.screen.size()

# Audio setup for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Get volume control range
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

vol = 0
volbar = 400
volper = 0

# Mode tracking
current_mode = "IDLE"

# Tab switching tracking
last_hand_state = None
hand_state_change_time = 0
hand_state_debounce = 0.5  # seconds

while True:
    # Find hand landmarks
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break
    
    # Flip camera horizontally for mirror effect
    img = cv2.flip(img, 1)
    
    img = detector.find_hands(img)
    lmList, bbox = detector.find_position(img)

    if len(lmList) != 0:
        # Get finger states
        fingers = detector.fingersUp()
        
        # Extract key landmark positions
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip
        x_thumb, y_thumb = lmList[4][1:]  # Thumb tip
        
        # ============ MOUSE CONTROL MODE ============
        # Only index finger up = Move mouse
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            current_mode = "MOUSE MOVE"
            
            # Draw gesture frame
            cv2.rectangle(img, (frameR, frameR), (wcam-frameR, hcam-frameR),
                          (255, 0, 255), 2)
            
            # Convert hand coordinates to screen coordinates
            x3 = np.interp(x1, (frameR, wcam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hcam-frameR), (0, hScr))
            
            # Apply smoothing
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            
            # Move mouse (fixed direction - removed wScr subtraction)
            autopy.mouse.move(clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            
            # Display mode
            cv2.putText(img, "MODE: MOUSE MOVE", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        
        # ============ MOUSE CLICK MODE ============
        # Index + Middle fingers up = Click mode
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            current_mode = "MOUSE CLICK"
            
            # Calculate distance between index and middle fingers
            length, img, lineinfo = detector.find_Distance(8, 12, img)
            
            # Draw mode indicator
            cv2.putText(img, "MODE: MOUSE CLICK", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            
            # Click if fingers are close
            if length < 40:
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
        
        # ============ VOLUME CONTROL MODE ============
        # Thumb + Index up = Volume control
        elif fingers[0] == 1 and fingers[1] == 1:
            current_mode = "VOLUME CONTROL"
            
            # Calculate distance between thumb and index
            length = math.hypot(x2 - x_thumb, y2 - y_thumb)
            
            # Draw gesture visualization
            cv2.circle(img, (x_thumb, y_thumb), 15, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 255, 255), cv2.FILLED)
            cv2.line(img, (x_thumb, y_thumb), (x1, y1), (0, 255, 255), 3)
            
            # Map distance to volume
            vol = np.interp(length, [50, 218], [minVol, maxVol])
            volbar = np.interp(length, [50, 218], [400, 150])
            volper = np.interp(length, [50, 218], [0, 100])
            
            # Set system volume
            volume.SetMasterVolumeLevel(vol, None)
            
            # Visual feedback
            if length < 50:
                cv2.circle(img, (int((x_thumb + x1) / 2), int((y_thumb + y1) / 2)), 15, (0, 255, 0), cv2.FILLED)
            
            # Draw volume bar
            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 255), 3)
            cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 255), cv2.FILLED)
            cv2.putText(img, f'{int(volper)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
            
            # Display mode
            cv2.putText(img, f"MODE: VOLUME CONTROL | {int(volper)}%", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        
        else:
            current_mode = "IDLE"
            cv2.putText(img, "MODE: IDLE - Show a gesture", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (200, 200, 200), 2)
        
        # ============ TAB SWITCHING ============
        # Open hand (all 5 fingers up) = Switch next tab
        if sum(fingers) == 5:  # All fingers up
            cv2.putText(img, "HAND: OPEN - Next Tab", (10, 80), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 0), 2)
            
            current_time = time.time()
            if last_hand_state != "OPEN" and (current_time - hand_state_change_time) > hand_state_debounce:
                pyautogui.hotkey('alt', 'tab')
                hand_state_change_time = current_time
                last_hand_state = "OPEN"
        
        # Closed hand (all 5 fingers down) = Switch previous tab
        elif sum(fingers) == 0:  # All fingers down
            cv2.putText(img, "HAND: CLOSED - Previous Tab", (10, 80), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 100, 0), 2)
            
            current_time = time.time()
            if last_hand_state != "CLOSED" and (current_time - hand_state_change_time) > hand_state_debounce:
                pyautogui.hotkey('alt', 'shift', 'tab')
                hand_state_change_time = current_time
                last_hand_state = "CLOSED"

    # Frame rate calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime
    
    # Display FPS
    cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    
    # Display instructions
    cv2.putText(img, "Index: Mouse | Index+Middle: Click | Thumb+Index: Volume | Open Hand: Next Tab | Closed Hand: Prev Tab", 
                (10, hcam - 10), cv2.FONT_HERSHEY_PLAIN, 1, (200, 200, 200), 1)

    # Show frame
    cv2.imshow("Combined Gesture Control", img)

    # Check for exit
    k = cv2.waitKey(1)
    if k % 256 == 27:  # ESC key
        print("Escape hit, closing the app")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
