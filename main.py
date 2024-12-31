# import os 
# import subprocess
# import sys
# from internal.hardware.keyboard import Keyboard
# if os.geteuid() != 0:
#         print("This script requires root privileges to access input devices.")
#         print("Attempting to run with sudo...")
#         subprocess.check_call(['sudo', 'python3'] + sys.argv)
#         sys.exit()
# else:
#     print("You are running as root")
#     keyboard = Keyboard()
#     keyboard.start()

from internal.UI.keyboard_ui import VirtualKeyboard

if __name__ == "__main__":
    keyboard = VirtualKeyboard()
    keyboard.engine()
    keyboard.start()