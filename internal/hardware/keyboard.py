from evdev import InputDevice, UInput, ecodes
import evdev
import threading
class Keyboard:
    def __init__(self):
        self.selected_device = None
        self.uinput = None

    

    def detect_keyboard(self):
        """
        Detect keyboard based on user key press, filtering out non-keyboard devices.
        """
        devices = [InputDevice(path) for path in evdev.list_devices()]
        print("Press a key on the keyboard you want to set up as a macro keyboard...")

        # Filter for devices that are likely keyboards
        keyboard_devices = []
        for device in devices:
            try:
                capabilities = device.capabilities()
                if evdev.ecodes.EV_KEY in capabilities:
                    supported_keys = capabilities[evdev.ecodes.EV_KEY]
                    # Consider as keyboard if it has alphanumeric or function keys
                    if any(key in supported_keys for key in range(ecodes.KEY_A, ecodes.KEY_Z + 1)):
                        keyboard_devices.append(device)
            except Exception as e:
                print(f"Error reading device {device.path}: {e}")

        # Listen to valid keyboard devices only
        for device in keyboard_devices:
            threading.Thread(target=self.listen_for_key, args=(device,), daemon=True).start()

        # Wait for the user to select a device
        while not self.selected_device:
            pass

    def listen_for_key(self, device):
        """
        Listen for a key press on a device.
        """
        try:
            for event in device.read_loop():
                if event.type == ecodes.EV_KEY and event.value == 1:  # Key press detected
                    self.selected_device = device.path
                    print(f"Selected keyboard: {device.name} (ID: {device.path})")
                    break
        except Exception as e:
            print(f"Error reading from device {device.name}: {e}")

        if self.selected_device:
            self.disable_keyboard()

    def disable_keyboard(self):
        """
        Disable the selected keyboard for other applications and create a virtual keyboard.
        """
        try:
            device = InputDevice(self.selected_device)
            self.uinput = UInput.from_device(device, name="MacroKeyboard")
            print(f"Keyboard {device.name} has been disabled for other applications.")
            print("You can now use it exclusively for macro setup.")
            
            # Redirect events from the original device to the virtual device
            for event in device.read_loop():
                self.uinput.write_event(event)
                self.uinput.syn()
        except Exception as e:
            print(f"Error disabling keyboard {self.selected_device}: {e}")

    def get_physical_layout(self):
        """
        Determine the physical layout of the selected keyboard.
        """
        if not self.selected_device:
            print("No keyboard selected. Run detect_keyboard first.")
            return "Unknown Layout"

        try:
            device = InputDevice(self.selected_device)
            capabilities = device.capabilities().get(ecodes.EV_KEY, [])
            supported_keys = set(capabilities)

            # Define key groups
            numpad_keys = {ecodes.ecodes[key] for key in ecodes.KEY if key.startswith('KEY_KP')}
            navigation_keys = {
                ecodes.KEY_INSERT,
                ecodes.KEY_DELETE,
                ecodes.KEY_HOME,
                ecodes.KEY_END,
                ecodes.KEY_PAGEUP,
                ecodes.KEY_PAGEDOWN,
                ecodes.KEY_ARROW_UP,
                ecodes.KEY_ARROW_DOWN,
                ecodes.KEY_ARROW_LEFT,
                ecodes.KEY_ARROW_RIGHT
            }
            function_keys = {ecodes.KEY_F1, ecodes.KEY_F2, ecodes.KEY_F3, ecodes.KEY_F4, ecodes.KEY_F5, 
                             ecodes.KEY_F6, ecodes.KEY_F7, ecodes.KEY_F8, ecodes.KEY_F9, ecodes.KEY_F10, 
                             ecodes.KEY_F11, ecodes.KEY_F12}

            # Check key groups
            has_numpad = bool(supported_keys & numpad_keys)
            has_navigation = bool(supported_keys & navigation_keys)
            has_function_keys = bool(supported_keys & function_keys)

            # Infer layout
            if has_numpad and has_function_keys and has_navigation:
                return "Full-size"
            elif not has_numpad and has_function_keys and has_navigation:
                return "Tenkeyless (TKL)"
            elif not has_numpad and not has_navigation and has_function_keys:
                return "60%"
            else:
                return "Unknown Layout"
        except Exception as e:
            print(f"Error determining layout for device {self.selected_device}: {e}")
            return "Error"

    def start(self):
        """
        Main entry point to start the keyboard setup process.
        """
        self.detect_keyboard()
        layout = self.get_physical_layout()
        print(f"The physical layout of the keyboard is: {layout}")

    # Getter methods
    def get_device_name(self):
        """
        Get the name of the selected device.
        """
        if not self.selected_device:
            return "No device selected"
        return self.selected_device.name

    def get_device_path(self):
        """
        Get the path of the selected device.
        """
        if not self.selected_device:
            return "No device selected"
        return self.selected_device.path

    def get_device_vendor_id(self):
        """
        Get the Vendor ID of the selected device.
        """
        if not self.selected_device:
            return "No device selected"
        return hex(self.selected_device.info.vendor)

    def get_device_product_id(self):
        """
        Get the Product ID of the selected device.
        """
        if not self.selected_device:
            return "No device selected"
        return hex(self.selected_device.info.product)

    def get_device_version(self):
        """
        Get the version or serial-like identifier of the selected device.
        """
        if not self.selected_device:
            return "No device selected"
        return self.selected_device.info.version



