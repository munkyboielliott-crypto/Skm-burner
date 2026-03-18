import os
import shutil
import sys

def list_drives():
    if os.name == 'nt':  # Windows
        from string import ascii_uppercase
        return [f"{d}:\\" for d in ascii_uppercase if os.path.exists(f"{d}:\\")]
    else:  # Linux/macOS
        return [os.path.join("/Volumes", d) for d in os.listdir("/Volumes")]

def find_usb(usb_name):
    for drive in list_drives():
        if usb_name.lower() in drive.lower():
            return drive
    return None

def skm(file_path, current_fmt, new_fmt, usb_name):
    if not os.path.exists(file_path):
        print("File not found!")
        return
    if not file_path.endswith(current_fmt):
        print(f"Warning: file does not match format {current_fmt}")

    out_name = os.path.basename(file_path)
    if new_fmt:
        out_name = out_name.rsplit('.',1)[0] + '.' + new_fmt

    usb_path = find_usb(usb_name)
    if not usb_path:
        print(f"USB '{usb_name}' not found!")
        return

    shutil.copy(file_path, os.path.join(usb_path, out_name))
    print(f"File '{file_path}' copied as '{out_name}' to USB '{usb_name}'")

if len(sys.argv) < 5:
    print("Usage: -skm <file> <current format> <new format optional> <thumb stick name>")
else:
    _, file_path, current_fmt, new_fmt, usb_name = sys.argv
    if new_fmt.lower() == "none":
        new_fmt = None
    skm(file_path, current_fmt, new_fmt, usb_name)
