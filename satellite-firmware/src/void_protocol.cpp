#include "void_protocol.h"
#include "void_config.h"

VoidProtocol Void;

void VoidProtocol::begin() {
    // 1. Init Serial
    Serial.begin(115200);
    while(!Serial); 

    // 2. Init Display
    pinMode(OLED_RST, OUTPUT);
    digitalWrite(OLED_RST, LOW); delay(20); digitalWrite(OLED_RST, HIGH);
    display.init();
    display.flipScreenVertically();
    display.setFont(ArialMT_Plain_10);
    updateDisplay("BOOT", "Initializing...");

    // 3. Init Crypto (Sodium)
    if (sodium_init() < 0) {
        updateDisplay("ERROR", "Sodium Init Fail");
        while(1);
    }

    // 4. Init LoRa (SX1262)
    int state = radio.begin(LORA_FREQ, LORA_BW, LORA_SF, LORA_CR, LORA_SYNC, 10);
    if (state != RADIOLIB_ERR_NONE) {
        String err = "LoRa Fail: " + String(state);
        updateDisplay("ERROR", err);
        while(1);
    }
    
    // Set Output Power to +22 dBm (Heltec V3 limit)
    radio.setOutputPower(22);
    
    updateDisplay("READY", "Void v2.1");
}

void VoidProtocol::updateDisplay(String status, String subtext) {
    //TODO: optimise font i.e. header, desc, footer and wire(8000) for writing faster
    display.clear();
    display.drawString(0, 0, "VOID PROTOCOL v2.1");
    display.drawString(0, 16, "Status: " + status);
    display.drawString(0, 32, subtext);
    display.display();
}

void VoidProtocol::hexDump(uint8_t* data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        if (data[i] < 0x10) Serial.print("0");
        Serial.print(data[i], HEX);
    }
    Serial.println();
}

// Simple CRC32 wrapper (or use Sodium's logic)
uint32_t VoidProtocol::calculateCRC(uint8_t* data, size_t len) {
    // Placeholder: In real code, use CRC32 from a lib or custom implementation
    return 0xCAFEBABE; 
}