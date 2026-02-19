/*-------------------------------------------------------------------------
 * 🛰️ VOID PROTOCOL v2.1 | Tiny Innovation Group Ltd
 * -------------------------------------------------------------------------
 * Authority: Tiny Innovation Group Ltd
 * License:   Apache 2.0
 * Status:    Authenticated Clean Room Spec
 * File:      main.cpp
 * Desc:      Main entry point for VOID Protocol satellite firmware.
 * -------------------------------------------------------------------------*/
#include <Arduino.h>
#include "void_protocol.h"
#include "seller.h"
#include "buyer.h"

// --- CONFIGURATION ---
// Uncomment ONE of these to set the board role
//#define ROLE_SELLER 
#define ROLE_BUYER 
// ---------------------

void setup() {
    Void.begin();
    
    #ifdef ROLE_SELLER
        Void.updateDisplay("ROLE", "SELLER (Sat A)");
    #else
        Void.updateDisplay("ROLE", "BUYER (Sat B)");
        Void.radio.startReceive(); // Buyer starts in RX mode
    #else
        #error "Please define a ROLE in main.cpp"
    #endif
}

void loop() {
    #ifdef ROLE_SELLER
        runSellerLoop();
    #elif defined(ROLE_BUYER)
        runBuyerLoop();
    #endif
}