import re
import tk
import fileinput
from Device import Device
import bluetooth


def browse_file_location():
    root = tk.Tk()
    # Display the file dialog and get the selected file path
    file_path = filedialog.askopenfilename(title="Select File to Send", filetypes=[("All files", "*.*")])
    root.withdraw()  # Hide the main window
    return file_path

def browse_save_location():
    root = tk.Tk()
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    root.withdraw()  # Hide the main window
    return file_path


def validate_mac_address(mac_address):
    # Regular expression to match a Bluetooth MAC address
    mac_pattern = re.compile("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
    if mac_pattern.match(mac_address):
        return True
    else:
        return False


def get_device_mac():
    while True:
        # Ask the user to input their device's Bluetooth MAC address
        device_mac = input("Enter your device's Bluetooth MAC address: ")
        if validate_mac_address(device_mac):
            print("Device MAC address is valid.")
            return device_mac
        else:
            print("Invalid MAC address format. Please try again.")


def get_server_mac():
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found {} devices.".format(len(nearby_devices)))
    i = 0
    for addr, name in nearby_devices:
        print(i + 1, "  {} - {}".format(name, addr))
        i += 1
    i = 0
    choice = int(input("Which device would you like to connect with ?: "))
    for addr, name in nearby_devices:
        if i == choice-1:
            return addr
        i += 1


class NinjaShareApp():
    def __init__(self):
        self.my_device = None
        self.server_mac_address = None

    def ask_change_server_mac(self):
        while True:
            print("Server Mac Address:", self.server_mac_address)
            answer = input("Change Server Mac Address" + " (y/n): ").strip().lower()
            if answer in ('y', 'n'):
                if answer == 'y':
                    self.server_mac_address = get_server_mac()
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")

    def connect(self):
        try:
            self.ask_change_server_mac()
            self.my_device.connect_to_server(self.server_mac_address)
        except Exception as e:
            self.my_device.open_connection()

    def receive_file(self):
        save_path = browse_save_location()
        self.connect()
        self.my_device.receive_file(save_path)

    def send_file(self):
        file_path = browse_file_location()
        self.connect()
        self.my_device.send_file(file_path)

    def create_room(self):
        self.my_device.open_connection()
        self.my_device.establish_room()

    def enter_room(self):
        self.ask_change_server_mac()
        self.my_device.connect_to_server(self.server_mac_address)
        self.my_device.enter_room()

    # Display chat menu
    def display_chat_menu(self):
        while True:
            print("1. Create room")
            print("2. Enter room")
            print("3. Back")
            chat_choice = input("Enter your choice: ")

            if chat_choice == '1':
                try:
                    self.create_room()
                    break
                except Exception as e:
                    print(e)
            elif chat_choice == '2':
                try:
                    self.enter_room()
                    break
                except Exception as e:
                    print("Room Not Founded")
            elif chat_choice == '3':
                break  # Go back to main menu
            else:
                print("Invalid choice. Please select again.")

    # Display menu
    def display_menu(self):
        while True:
            print("1. Send file")
            print("2. Receive file")
            print("3. chat")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.send_file()
            elif choice == '2':
                self.receive_file()
            elif choice == '3':
                self.display_chat_menu()
            elif choice == '4':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please select again.")

    def run(self):
        my_mac_address = "70-A6-CC-DC-0B-F8"
        self.server_mac_address = get_server_mac()
        # default data can develop to make the user enter this data
        port = 15
        backlog = 1
        size = 1024 * 1024 * 20
        self.my_device = Device(my_mac_address, port, backlog, size)
        self.display_menu()


if __name__ == "__main__":
    app = NinjaShareApp()
    app.run()
