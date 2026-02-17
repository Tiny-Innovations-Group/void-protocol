#include "void_protocol.h"
#include "seller.h"

// Mock Data for Phase 1
PacketA_t invoice;

void runSellerLoop() {
    static unsigned long lastTx = 0;
    
    // Broadcast every 5 seconds (Advertising Phase)
    if (millis() - lastTx > 5000) {
        
        // 1. Fill Invoice Data
        // Header (Big Endian)
        invoice.header.ver_type_sec = 0x10; // Version 0, Type 1 (TM)
        invoice.header.apid_lo = 0xA1;      // ID: Sat A
        
        // Payload (Little Endian)
        invoice.sat_id = 0xAAAAAAAA;        // "Sat A"
        invoice.amount = 500;               // 5.00 USDC
        invoice.asset_id = 1;               // USDC
        invoice.epoch_ts = millis();        // Fake timestamp
        
        // 2. Transmit
        int state = Void.radio.transmit((uint8_t*)&invoice, sizeof(PacketA_t));
        
        if (state == RADIOLIB_ERR_NONE) {
            Void.updateDisplay("SELLER", "Broadcasting Invoice...");
            Serial.println("[TX] Sent Packet A (68 Bytes)");
        } else {
            Void.updateDisplay("ERROR", "Tx Failed");
        }
        
        lastTx = millis();
        
        // 3. Listen Window (60s would go here)
        Void.radio.startReceive();
    }
}