#ifndef VOID_CONFIG_H
#define VOID_CONFIG_H

// Heltec V3 LoRa Pins (SX1262)
#define RADIO_NSS       8
#define RADIO_RST       12
#define RADIO_BUSY      13
#define RADIO_DIO1      14

// Heltec V3 OLED Pins
#define OLED_SDA        17
#define OLED_SCL        18
#define OLED_RST        21
#define OLED_ADDR       0x3C

// LoRa Config (EU868)
#define LORA_FREQ       868.0
#define LORA_BW         125.0
#define LORA_SF         9
#define LORA_CR         5
#define LORA_SYNC       0x12 // Private Sync Word

#endif