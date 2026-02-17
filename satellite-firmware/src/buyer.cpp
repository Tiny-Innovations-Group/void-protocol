#include "void_protocol.h"
#include "buyer.h"

void runBuyerLoop() {
    // 1. Check for incoming packets
    int state = Void.radio.readData((uint8_t*)NULL, 0); // Check buffer

    if (state == RADIOLIB_ERR_NONE) {
        // We have data!
        size_t len = Void.radio.getPacketLength();
        uint8_t buffer[256];
        
        Void.radio.readData(buffer, len);

        // 2. Filter: Is it an Invoice (68 Bytes)?
        if (len == sizeof(PacketA_t)) {
            PacketA_t* pkt = (PacketA_t*)buffer;
            
            Void.updateDisplay("BUYER", "RX Invoice! Syncing...");
            
            // 3. PIPE TO PYTHON (Ground Station)
            // Format: "INVOICE:<HEX_DATA>"
            Serial.print("INVOICE:");
            Void.hexDump(buffer, len);
            
        } else {
            Serial.print("UNKNOWN_PKT:");
            Void.hexDump(buffer, len);
        }
    }
}