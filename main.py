import win32api
import win32con

# Constants for the input type and keyboard scan code
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
VK_CAPITAL = 0x14
VK_NUMLOCK = 0x90
VK_SCROLL = 0x91

def disable_input():
    # Create an input event structure
    class Input_I(ctypes.Structure):
        _fields_ = [("type", ctypes.c_ulong),
                    ("ii", InputUnion)]

    # Create an input event union
    class InputUnion(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT),
                    ("ki", KEYBDINPUT)]

    # Create a mouse input event structure
    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [("dx", ctypes.c_long),
                    ("dy", ctypes.c_long),
                    ("mouseData", ctypes.c_ulong),
                    ("dwFlags", ctypes.c_ulong),
                    ("time",ctypes.c_ulong),
                    ("dwExtraInfo", PUL)]

    # Create a keyboard input event structure
    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [("wVk", ctypes.c_ushort),
                    ("wScan", ctypes.c_ushort),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", PUL)]

    # Create a pointer to the input event union
    PUL = ctypes.POINTER(ctypes.c_ulong)

    # Create a function prototype for SendInput with an input event structure as the parameter
    SendInput = ctypes.windll.user32.SendInput

    # Create instances of the input event structures and union
    ii = Input_I()
    ieu = InputUnion()
    mi = MOUSEINPUT(0, 0, 0, 0x0001, 0, ctypes.pointer(ctypes.c_ulong(0)))
    ki = KEYBDINPUT(0, 0, 0, 0, ctypes.pointer(ctypes.c_ulong(0)))

    # Set the input event structure's type to INPUT_MOUSE
    ii.type = INPUT_MOUSE

    # Set the input event union's mouse event to the mouse event structure
    ieu.mi = mi

    # Set the input event structure's union to the input event union
    ii.ii = ieu

    # Send the input event to the system
    SendInput(1, ctypes.pointer(ii), ctypes.sizeof(ii))

    # Set the input event structure's type to INPUT_KEYBOARD
    ii.type = INPUT_KEYBOARD

    # Set the input event union's keyboard event to the keyboard event structure
    ieu.ki = ki

    # Set the keyboard event structure's virtual key to VK_CAPITAL (Caps Lock key)
    ki.wVk = VK_CAPITAL

    # Set the keyboard event structure's scan code to the value for the Caps Lock key
    # This is necessary for the key event to be recognized by the system
    ki.wScan = win32api.MapVirtualKey(VK_CAPITAL, 0)

    # Set the keyboard event structure's flags to indicate that the key is being released
    ki.dwFlags = KEYEVENTF_KEYUP

    # Set the input event structure's union to the input event union
    ii.ii = ieu

    # Send the input event to the system
    SendInput(1, ctypes.pointer(ii), ctypes.sizeof(ii))

    # Repeat the process for the Num Lock and Scroll Lock keys
    ki.wVk = VK_NUMLOCK
    ki.wScan = win32api.MapVirtualKey(VK_NUMLOCK, 0)
    ki.dwFlags = KEYEVENTF_KEYUP
    ii.ii = ieu
    SendInput(1, ctypes.pointer(ii), ctypes.sizeof(ii))

    ki.wVk = VK_SCROLL
    ki.wScan = win32api.MapVirtualKey(VK_SCROLL, 0)
    ki.dwFlags = KEYEVENTF_KEYUP
    ii.ii = ieu
    SendInput(1, ctypes.pointer(ii), ctypes.sizeof(ii))
