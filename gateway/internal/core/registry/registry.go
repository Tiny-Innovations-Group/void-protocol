package registry

import (
	"log"
)

// SatRecord holds the critical identity data for a satellite
type SatRecord struct {
	SatID     uint32
	PubKeyHex string // Ed25519 Public Key
	Wallet    string // Ethereum/L2 Wallet Address
	Role      string // "Seller" or "Mule"
}

// MockDB simulates our NoSQL database
var MockDB = map[uint32]SatRecord{}

// Initialize populates our hardcoded registry
func Initialize() {
	// Example Sat A (The Seller/Gas Station)
	MockDB[100] = SatRecord{
		SatID:     100,
		PubKeyHex: "4822f97bc9e8746acc9b2401e21db1afba0212657ad4ae8ee9fd16964dd27d97", // We will replace this with a real generated key later
		Wallet:    "0x1A2B3C4D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B",
		Role:      "Seller",
	}

	// Example Sat B (The Buyer/Mule)
	MockDB[101] = SatRecord{
		SatID:     101,
		PubKeyHex: "4102f95e145ccbaea5959f51cdf2e52e31b2de6bc19ae9ba1347f57e31549dd3",
		Wallet:    "0x9F8E7D6C5B4A39281706F5E4D3C2B1A09F8E7D6C",
		Role:      "Mule",
	}

	log.Println("🗄️  Registry Initialized with Hardcoded Satellites")
}

func GetSat(id uint32) (SatRecord, bool) {
	sat, exists := MockDB[id]
	return sat, exists
}
