# from time import time
# import spotify
# import time
# string = ""

# while True:
#     if string != spotify.get_current_track():
#         string = spotify.get_current_track()
#         print("Song:"+string['track_name'])
#         print(string['artists'])
#     time.sleep(1)

import win32gui

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print (hex(hwnd), win32gui.GetWindowText( hwnd ))

win32gui.EnumWindows( winEnumHandler, None )