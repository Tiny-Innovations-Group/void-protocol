/*-------------------------------------------------------------------------
 * 🛰️ VOID PROTOCOL v2.1 | Tiny Innovation Group Ltd
 * -------------------------------------------------------------------------
 * Authority: Tiny Innovation Group Ltd
 * License:   Apache 2.0
 * Status:    Authenticated Clean Room Spec
 * File:      buyer.cpp
 * Desc:      Buyer-side packet processing loop.
 * Compliant: NSA Strict Type Checking & Header Validation.
 * -------------------------------------------------------------------------*/
#include "void_protocol.h"
#include "buyer.h"

// Helper to extract APID from Big-Endian Header without reinterpret_cast
uint16_t getAPID(const uint8_t* buf) {
    // APID is 11 bits: Last 3 bits of byte 0 + all 8 bits of byte 1
    return ((buf[0] & 0x07) << 8) | buf[1];
}

void runBuyerLoop() {
    // 1. Check for incoming data availability
    // Note: We use a static buffer to avoid stack overflow or heap fragmentation
    static uint8_t rx_buffer[VOID_MAX_PACKET_SIZE];  
    
    int state = Void.radio.readData((uint8_t*)NULL, 0);

    if (state == RADIOLIB_ERR_NONE) {
        // 2. Get the actual length received
        size_t len = Void.radio.getPacketLength();

        // 3. SAFETY CHECK: Oversized Packet?
        if (len > VOID_MAX_PACKET_SIZE) {
            Serial.println("ERR: Packet > MTU");
            Void.radio.readData(rx_buffer, 0); // Flush
            return;
        }

        // 4. Read Data
        Void.radio.readData(rx_buffer, len);

        // 5. SAFETY CHECK: Undersized Packet?
        if (len < SIZE_VOID_HEADER) {
            Serial.println("ERR: Packet < Header");
            return;
        }

        // 6. HEADER INSPECTION (The NSA Way)
        // We peek at the APID (Application Process ID) to know what it CLAIMS to be.
        uint16_t apid = getAPID(rx_buffer);

        switch (apid) {
            case 0xA1: // Sat A (Seller) - Sending Invoice
                // 7. STRICT SIZE VALIDATION
                if (len == SIZE_PACKET_A) {
                    // Safe to cast because we verified ID AND Size
                    PacketA_t* pkt = (PacketA_t*)rx_buffer;
                    
                    Void.updateDisplay("BUYER", "RX Invoice Verified");
                    
                    // Pipe to Ground Station
                    Serial.print("INVOICE:");
                    Void.hexDump(rx_buffer, len);
                } else {
                    Serial.printf("ERR: Size Mismatch (Exp: %d, Got: %d)\n", SIZE_PACKET_A, len);
                }
                break;

            case 0xB2: // Sat B (Myself) - Echo? or Loopback?
                // Ignore self-talk
                break;
                
            case 0x18: // Handshake (Security Manager)
                if (len == SIZE_PACKET_H) {
                    Serial.print("HANDSHAKE:");
                    Void.hexDump(rx_buffer, len);
                }
                break;

            default:
                Serial.printf("WARN: Unknown APID 0x%03X\n", apid);
                break;
        }
    }
}