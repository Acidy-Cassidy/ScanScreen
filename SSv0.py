import cv2
import numpy as np
import time
import pyautogui
import keyboard

def select_rect():
    # Initialize variables
    mouse_is_pressed = False
    start_point = None
    end_point = None

    # Define callback function for mouse events
    def mouse_callback(event, x, y, flags, param):
        nonlocal mouse_is_pressed, start_point, end_point
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse_is_pressed = True
            start_point = (x, y)
            end_point = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            if mouse_is_pressed:
                end_point = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            mouse_is_pressed = False
            end_point = (x, y)

    # Create window and set mouse callback
    cv2.namedWindow("Select Region", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Select Region", mouse_callback)

    # Loop until user selects a rectangle
    while True:
        # Capture screen and draw rectangle
        img = pyautogui.screenshot()
        screenshot_array = np.array(img)
        img = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2RGBA)
        if start_point is not None and end_point is not None:
            cv2.rectangle(img, start_point, end_point, (0, 255, 0, 255), 2)
        cv2.imshow("Select Region", img)
        cv2.setWindowProperty("Select Region", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setWindowProperty("Select Region", cv2.WND_PROP_TOPMOST, 1)

        # Exit loop if user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Exit loop if user selects a rectangle
        if not mouse_is_pressed and start_point is not None and end_point is not None:
            break

    # Destroy window
    cv2.destroyAllWindows()

    # Return coordinates of selected rectangle
    x1, y1 = start_point
    x2, y2 = end_point
    return (x1, y1, x2 - x1, y2 - y1)

# Example usage
monitor_region = select_rect()
print("Selected region:", monitor_region)

time_interval = 0.5
previous_gray = None
previous_motion_time = None
program_state = "stopped"
brightness_factor = 1.0
motion_detected = False
motion_start_time = None

def start_program():
    global program_state
    program_state = "running"
    print("Program started")

def stop_program():
    global program_state
    program_state = "stopped"
    print("Program stopped")

def increase_brightness1():
    global brightness_factor
    if brightness_factor == 1.0:
        brightness_factor = 2.5
        print("Brightness increased to", brightness_factor)
    else:
        brightness_factor = 1.0
        print("Brightness reset to", brightness_factor)

keyboard.add_hotkey("s", start_program)
keyboard.add_hotkey("q", stop_program)
keyboard.add_hotkey("b", increase_brightness1)

while True:
    if program_state == "running":
        screenshot = pyautogui.screenshot(region=monitor_region)
        screenshot_array = np.array(screenshot)
        gray = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2GRAY)
        if previous_gray is None:
            previous_gray = gray
            continue
        diff = cv2.absdiff(gray, previous_gray)
        threshold = 30
        _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        count = np.count_nonzero(thresh)
        if count > 0:
            if not motion_detected:
                motion_detected = True
                motion_start_time = time.time()
                print("Motion detected at", time.ctime(motion_start_time))
            else:
                current_time = time.time()
                elapsed_time = current_time - motion_start_time
                if elapsed_time > time_interval:
                    motion_start_time = current_time
                    print("Motion detected at", time.ctime(motion_start_time))
        else:
            motion_detected = False
        previous_gray = gray
        screenshot_overlay = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2RGBA)
        if motion_detected:
            x, y, w, h = cv2.boundingRect(thresh)
            cv2.rectangle(screenshot_overlay, (x, y), (x + w, y + h), (0, 0, 255, 255), 2)
            if motion_start_time is not None:
                elapsed_time = time.time() - motion_start_time
                if elapsed_time > 3.0:
                    alpha = max(0, 255 - int(((elapsed_time - 3.0) / 1.0) * 255))
                else:
                    alpha = min(255, int(((3.0 - elapsed_time) / 3.0) * 255))
            else:
                alpha = 255
            screenshot_overlay[:, :, 3] = alpha
        else:
            screenshot_overlay[:, :, 3] = 255
        screenshot_overlay = np.clip(screenshot_overlay * brightness_factor, 0, 255).astype(np.uint8)
        cv2.imshow("Screenshot Overlay", screenshot_overlay)
        cv2.waitKey(1)

        # Quit the program if the user presses the "q" key
        if keyboard.is_pressed("q"):
            break
