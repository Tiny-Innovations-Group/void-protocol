"""
🛰️ VOID PROTOCOL v2.1 | Tiny Innovation Group Ltd
File:      main.py
Desc:      Main entry point foer the Void Ground Station (Lite) Python script.
           Listens on serial port for incoming packets from the Heltec Buyer board.
"""

import serial
import struct
import time
import sys

# --- CONFIGURATION ---
SERIAL_PORT = '/dev/tty.usbserial-0001' # Update this for your OS (e.g., COM3 on Windows)
BAUD_RATE = 115200

# --- PACKET STRUCTURES ---
# Packet A Size: 68 Bytes
# Header (6B) + Body (62B)
# Body Format (Little Endian '<'):
#   u64 timestamp (Q)
#   f64 pos_x, pos_y, pos_z (3d)
#   f32 vel_x, vel_y, vel_z (3f)
#   u32 sat_id (I)
#   u64 amount (Q)
#   u16 asset_id (H)
#   u32 crc32 (I)
PACKET_A_FMT = '<QdddfffIQHI'
PACKET_A_SIZE = 68
HEADER_SIZE = 6

def parse_packet_a(raw_bytes):
    if len(raw_bytes) != PACKET_A_SIZE:
        print(f"[ERR] Invalid Size: {len(raw_bytes)} bytes (Expected {PACKET_A_SIZE})")
        return

    # 1. Parse Header (Big Endian - Network Byte Order)
    # We just grab the raw bytes for display, or parse specific fields if needed
    header = raw_bytes[:HEADER_SIZE]
    apid = ((header[0] & 0x07) << 8) | header[1] # Simple parse for APID logic
    
    # 2. Parse Payload (Little Endian - MCU Native)
    payload = raw_bytes[HEADER_SIZE:]
    try:
        data = struct.unpack(PACKET_A_FMT, payload)
        
        # Unpack tuple
        epoch_ts, px, py, pz, vx, vy, vz, sat_id, amount, asset_id, crc = data
        
        print("-" * 40)
        print(f"📡 INVOICE RECEIVED (Sat ID: {sat_id})")
        print("-" * 40)
        print(f"⏰ Timestamp : {epoch_ts}")
        print(f"📍 Position  : [{px:.2f}, {py:.2f}, {pz:.2f}] km")
        print(f"🚀 Velocity  : [{vx:.2f}, {vy:.2f}, {vz:.2f}] m/s")
        print(f"💰 Cost      : {amount} (Asset ID: {asset_id})")
        print(f"🔐 Integrity : CRC32 0x{crc:08X}")
        print("-" * 40)
        print("")
        
    except struct.error as e:
        print(f"[ERR] Struct Unpack Failed: {e}")

def main():
    print(f"🛰️  Void Ground Station (Lite) | Listening on {SERIAL_PORT}...")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as e:
        print(f"[FATAL] Could not open port: {e}")
        sys.exit(1)

    while True:
        try:
            # Read line from Heltec Buyer
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Check for magic prefix from buyer.cpp
                if line.startswith("PKT_A:"):
                    hex_str = line.split(":")[1]
                    try:
                        raw_data = bytes.fromhex(hex_str)
                        parse_packet_a(raw_data)
                    except ValueError:
                        print(f"[ERR] Bad Hex Data: {hex_str[:10]}...")
                
                elif line.startswith("PKT_H:"):
                     print(f"[HANDSHAKE] {line}")
                
                else:
                    # Print debug logs from the board (e.g., RSSI info)
                    print(f"[BOARD] {line}")
                    
        except KeyboardInterrupt:
            print("\n[STOP] Ground Station shutting down.")
            break
        except Exception as e:
            print(f"[ERR] Loop Error: {e}")

    ser.close()

if __name__ == "__main__":
    main()