import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math

class VirtualKeyboard:
    def __init__(self):
        self.wcam, self.hcam = 640, 480
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.wcam)
        self.cap.set(4, self.hcam)
        
        self.detector = htm.HandDetector()
        self.cTime = 0
        self.pTime = 0
        
        # Keyboard layout
        self.keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'DEL'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', ',', 'SPACE']
        ]
        
        # Key dimensions
        self.key_width = 60
        self.key_height = 50
        self.key_gap = 2
        self.keyboard_start_x = 20
        self.keyboard_start_y = 250
        
        # Text display
        self.typed_text = ""
        self.selected_key = None
        self.key_pressed_time = 0
        self.press_duration = 0.3  # seconds
        
    def get_key_rect(self, row, col):
        """Get the rectangle coordinates for a key"""
        x = self.keyboard_start_x + col * (self.key_width + self.key_gap)
        y = self.keyboard_start_y + row * (self.key_height + self.key_gap)
        return (x, y, self.key_width, self.key_height)
    
    def point_in_key(self, point, key_rect):
        """Check if a point is inside a key rectangle"""
        x, y, w, h = key_rect
        px, py = point
        return x <= px <= x + w and y <= py <= y + h
    
    def get_key_at_position(self, x, y):
        """Get the key at a specific position"""
        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                rect = self.get_key_rect(row_idx, col_idx)
                if self.point_in_key((x, y), rect):
                    return key, row_idx, col_idx
        return None, None, None
    
    def draw_keyboard(self, img, selected_key_pos=None, pressed_key_pos=None):
        """Draw the virtual keyboard on the image"""
        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                x, y, w, h = self.get_key_rect(row_idx, col_idx)
                
                # Determine key color
                if pressed_key_pos == (row_idx, col_idx):
                    color = (0, 255, 0)  # Green for pressed
                    thickness = cv2.FILLED
                elif selected_key_pos == (row_idx, col_idx):
                    color = (0, 255, 255)  # Cyan for selected
                    thickness = 2
                else:
                    color = (200, 200, 200)  # Gray for normal
                    thickness = 2
                
                # Draw key rectangle
                cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)
                
                # Draw key text
                font_scale = 0.5 if key in ['SPACE', 'DEL'] else 0.6
                text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1)[0]
                text_x = x + (w - text_size[0]) // 2
                text_y = y + (h + text_size[1]) // 2
                
                text_color = (0, 0, 0) if pressed_key_pos == (row_idx, col_idx) else (0, 0, 0)
                cv2.putText(img, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 
                           font_scale, text_color, 1)
        
        return img
    
    def process_key(self, key):
        """Process a key press"""
        if key == 'DEL':
            self.typed_text = self.typed_text[:-1] if self.typed_text else ""
        elif key == 'SPACE':
            self.typed_text += ' '
        else:
            self.typed_text += key
    
    def run(self):
        """Main application loop"""
        while True:
            success, img = self.cap.read()
            if not success:
                print("Failed to grab frame")
                break
            
            # Flip for selfie view
            img = cv2.flip(img, 1)
            img = self.detector.find_hands(img)
            lmList, bbox = self.detector.find_position(img)
            
            selected_pos = None
            pressed_pos = None
            
            if len(lmList) != 0:
                # Get index finger position
                x_index, y_index = lmList[8][1:]
                
                # Get middle finger position
                x_middle, y_middle = lmList[12][1:]
                
                # Check which key is selected
                selected_key, row, col = self.get_key_at_position(x_index, y_index)
                if selected_key:
                    selected_pos = (row, col)
                    cv2.circle(img, (x_index, y_index), 15, (0, 255, 255), cv2.FILLED)
                
                # Get fingers state
                fingers = self.detector.fingersUp()
                
                # Mode 1: Index + Middle close = Press key
                if fingers[1] == 1 and fingers[2] == 1:
                    length = math.hypot(x_middle - x_index, y_middle - y_index)
                    
                    if length < 40 and selected_key:  # Close proximity = press
                        pressed_pos = (row, col)
                        cv2.circle(img, (x_index, y_index), 15, (0, 255, 0), cv2.FILLED)
                        self.key_pressed_time = time.time()
                        
                        # Process key if not already processed
                        if time.time() - self.key_pressed_time < self.press_duration:
                            if self.selected_key != selected_key:
                                self.process_key(selected_key)
                                self.selected_key = selected_key
                
                # Mode 2: Only index finger = Hover/Select
                elif fingers[1] == 1 and fingers[2] == 0:
                    cv2.circle(img, (x_index, y_index), 10, (255, 0, 255), cv2.FILLED)
                    self.selected_key = None
            
            # Draw keyboard
            img = self.draw_keyboard(img, selected_pos, pressed_pos)
            
            # Draw typed text display
            cv2.rectangle(img, (20, 180), (self.wcam - 20, 240), (50, 50, 50), cv2.FILLED)
            cv2.rectangle(img, (20, 180), (self.wcam - 20, 240), (0, 255, 0), 2)
            cv2.putText(img, "Typed: " + self.typed_text[-30:], (30, 210), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw instructions
            cv2.putText(img, "Index finger: Select | Index+Middle close: Press Key", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # FPS counter
            self.cTime = time.time()
            fps = 1 / (self.cTime - self.pTime) if (self.cTime - self.pTime) > 0 else 0
            self.pTime = self.cTime
            cv2.putText(img, f"FPS: {int(fps)}", (self.wcam - 80, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Show frame
            cv2.imshow("Virtual Keyboard", img)
            
            # Check for exit
            k = cv2.waitKey(1)
            if k % 256 == 27:  # ESC key
                print("Escape hit, closing the app")
                break
            elif k % 256 == ord('c'):  # 'c' to clear
                self.typed_text = ""
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    kb = VirtualKeyboard()
    kb.run()
