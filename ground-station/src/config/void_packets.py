"""
🛰️ VOID PROTOCOL v2.1 | Tiny Innovation Group Ltd
File:      void_packets.py
Desc:      Python ctypes definitions for OTA serialization.
           Matches 'void_packets.h' byte-for-byte.
"""

from ctypes import *

# --- CONSTANTS (from void_types.h) ---
SIZE_PACKET_H = 112
SIZE_PACKET_A = 68
SIZE_PACKET_B = 176
SIZE_PACKET_ACK = 120
SIZE_TUNNEL_DATA = 88
SIZE_PACKET_C = 104
SIZE_PACKET_D = 128

# --- COMMON HEADER ---

class VoidHeader_t(Structure):
    """
    Standard CCSDS Primary Header (6 Bytes)
    Note: Fields are Big-Endian on wire, but we parse as bytes usually.
    """
    _pack_ = 1
    _fields_ = [
        ("ver_type_sec", c_uint8),  # Version(3)|Type(1)|SecHead(1)|APID_Hi(3)
        ("apid_lo",      c_uint8),  # APID_Lo(8)
        ("seq_flags",    c_uint8),  # Flags(2)|Count_Hi(6)
        ("seq_count_lo", c_uint8),  # Count_Lo(8)
        ("packet_len",   c_uint16)  # Total Length - 1 (Big Endian)
    ]

# --- PHASE 1: HANDSHAKE (Packet H) ---

class PacketH_t(Structure):
    """
    Packet H: Ephemeral Key Exchange (112 Bytes)
    """
    _pack_ = 1
    _fields_ = [
        ("header",      VoidHeader_t),      # 00-05
        ("session_ttl", c_uint16),          # 06-07 (Little)
        ("timestamp",   c_uint64),          # 08-15 (Little)
        ("eph_pub_key", c_uint8 * 32),      # 16-47
        ("signature",   c_uint8 * 64)       # 48-111
    ]

# --- PHASE 2: INVOICE (Packet A) ---

class PacketA_t(Structure):
    """
    Packet A: The Invoice (68 Bytes)
    """
    _pack_ = 1
    _fields_ = [
        ("header",   VoidHeader_t),         # 00-05
        ("epoch_ts", c_uint64),             # 06-13 (Little)
        ("pos_vec",  c_double * 3),         # 14-37 (Little IEEE 754)
        ("vel_vec",  c_float * 3),          # 38-49 (Little IEEE 754)
        ("sat_id",   c_uint32),             # 50-53 (Little)
        ("amount",   c_uint64),             # 54-61 (Little)
        ("asset_id", c_uint16),             # 62-63 (Little)
        ("crc32",    c_uint32)              # 64-67 (Little)
    ]

# --- PHASE 3: PAYMENT (Packet B) ---

class PacketB_t(Structure):
    """
    Packet B: Encrypted Payment (176 Bytes)
    """
    _pack_ = 1
    _fields_ = [
        ("header",      VoidHeader_t),      # 00-05
        ("epoch_ts",    c_uint64),          # 06-13
        ("pos_vec",     c_double * 3),      # 14-37
        ("enc_payload", c_uint8 * 62),      # 38-99 (ChaCha20)
        ("sat_id",      c_uint32),          # 100-103
        ("nonce",       c_uint32),          # 104-107
        ("signature",   c_uint8 * 64),      # 108-171
        ("global_crc",  c_uint32)           # 172-175
    ]

# --- PHASE 4: ACKNOWLEDGEMENT & TUNNEL ---

class RelayOps_t(Structure):
    """
    Relay Instructions (12 Bytes)
    """
    _pack_ = 1
    _fields_ = [
        ("azimuth",     c_uint16),          # 14-15
        ("elevation",   c_uint16),          # 16-17
        ("frequency",   c_uint32),          # 18-21
        ("duration_ms", c_uint32)           # 22-25
    ]

class TunnelData_t(Structure):
    """
    Tunnel Data: The Encrypted Payload (88 Bytes)
    Recovered from PacketAck_t.enc_tunnel
    """
    _pack_ = 1
    _fields_ = [
        ("header",      VoidHeader_t),      # 00-05
        ("_pad_a",      c_uint8 * 2),       # 06-07
        ("block_nonce", c_uint64),          # 08-15
        ("cmd_code",    c_uint16),          # 16-17
        ("ttl",         c_uint16),          # 18-19
        ("ground_sig",  c_uint8 * 64),      # 20-83
        ("crc32",       c_uint32)           # 84-87
    ]

class PacketAck_t(Structure):
    """
    ACK Packet: Ground -> Sat B (120 Bytes)
    """
    _pack_ = 1
    _fields_ = [
        ("header",       VoidHeader_t),     # 00-05
        ("_pad_a",       c_uint16),         # 06-07
        ("target_tx_id", c_uint32),         # 08-11
        ("status",       c_uint8),          # 12
        ("_pad_b",       c_uint8),          # 13
        ("relay_ops",    RelayOps_t),       # 14-25
        ("enc_tunnel",   c_uint8 * 88),     # 26-113
        ("_pad_c",       c_uint16),         # 114-115
        ("crc32",        c_uint32)          # 116-119
    ]

# --- PHASE 5: RECEIPT & DELIVERY (Packet C & D) ---

class PacketC_t(Structure):
    """
    Packet C: The Receipt (104 Bytes)
    """
    _pack_ = 1
    _fields_ = [
        ("header",      VoidHeader_t),      # 00-05
        ("_pad_head",   c_uint16),          # 06-07
        ("exec_time",   c_uint64),          # 08-15
        ("enc_tx_id",   c_uint64),          # 16-23
        ("enc_status",  c_uint8),           # 24
        ("_pad_sig",    c_uint8 * 7),       # 25-31
        ("signature",   c_uint8 * 64),      # 32-95
        ("crc32",       c_uint32),          # 96-99
        ("_tail_pad",   c_uint8 * 4)        # 100-103
    ]

class PacketD_t(Structure):
    """
    Packet D: Delivery (128 Bytes)
    """
    _pack_ = 1
    _fields_ = [
        ("header",      VoidHeader_t),      # 00-05
        ("_pad_head",   c_uint16),          # 06-07
        ("downlink_ts", c_uint64),          # 08-15
        ("sat_b_id",    c_uint32),          # 16-19
        ("payload",     c_uint8 * 98),      # 20-117
        ("global_crc",  c_uint32),          # 118-121
        ("_tail",       c_uint8 * 6)        # 122-127
    ]

# --- VERIFICATION CHECKS ---
if __name__ == "__main__":
    print(f"Packet H Size:   {sizeof(PacketH_t)} (Expected {SIZE_PACKET_H})")
    print(f"Packet A Size:   {sizeof(PacketA_t)} (Expected {SIZE_PACKET_A})")
    print(f"Packet B Size:   {sizeof(PacketB_t)} (Expected {SIZE_PACKET_B})")
    print(f"Packet Ack Size: {sizeof(PacketAck_t)} (Expected {SIZE_PACKET_ACK})")
    print(f"Tunnel Data Size:{sizeof(TunnelData_t)} (Expected {SIZE_TUNNEL_DATA})")
    print(f"Packet C Size:   {sizeof(PacketC_t)} (Expected {SIZE_PACKET_C})")
    print(f"Packet D Size:   {sizeof(PacketD_t)} (Expected {SIZE_PACKET_D})")
    
    assert sizeof(PacketH_t) == SIZE_PACKET_H
    assert sizeof(PacketA_t) == SIZE_PACKET_A
    assert sizeof(PacketB_t) == SIZE_PACKET_B
    assert sizeof(PacketAck_t) == SIZE_PACKET_ACK
    assert sizeof(TunnelData_t) == SIZE_TUNNEL_DATA
    assert sizeof(PacketC_t) == SIZE_PACKET_C
    assert sizeof(PacketD_t) == SIZE_PACKET_D
    print("✅ All Struct Sizes Verified")