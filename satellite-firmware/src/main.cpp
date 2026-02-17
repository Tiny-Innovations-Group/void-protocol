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