import hid
import time

# STM32 VID/PID (CubeMX Default: 0x0483 / 0x5750)
VID = 0x0483
PID = 0x5750

def send_config():
    try:
        # Open the device
        device = hid.device()
        device.open(VID, PID)
        
        print(f"Connected to Device: {device.get_manufacturer_string()} {device.get_product_string()}")
        
        # Prepare Data (32 bytes + Report ID if needed)
        # ちなみに hidapi は Report ID 0 (無し) の場合、先頭に 0x00 をつけることがある
        # ここでは Report ID なし構成にしたので、そのまま32バイト送るか、OSによっては 0x00 + 32bytes
        
        # Command: Set Sensitivity (Example)
        # Byte 0: Command ID (0x01)
        # Byte 1: Key Index (0xFF = All)
        # Byte 2-5: Value (Integer 50)
        
        # Prepare Data (33 bytes: Report ID 0x00 + 32 bytes Data)
        data = [0x00] + [0] * 32
        
        # Test Data: Set Sensitivity to 100 for ALL Keys
        data[1] = 0x01 # Command (Set Sensitivity)
        data[2] = 0xFF # Key Index (0xFF = 255 = All)
        data[3] = 200  # Val (Sensitivity = 100)

        device.write(data)
        print(f"Sent Config Command: Set Sensitivity to {data[2]}")
        print(f"Bytes Sent: {len(data)}")
        
        device.close()
        
    except IOError as ex:
        print(ex)
        print("Device not found or error")

if __name__ == "__main__":
    send_config()

