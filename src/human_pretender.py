import pyautogui
import time
import sys

if __name__ == '__main__':
    template = sys.argv[1]
    
    for line in open(template, "r"):

        # Write paragraph
        pyautogui.typewrite(line, interval=0.05)

    # Clear file
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    pyautogui.hotkey("ctrl", "s")
