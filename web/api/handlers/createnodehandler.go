package handlers

import (
	"fmt"
	"net/http"

	shell "github.com/ipfs/go-ipfs-api"
)

func CreateNodeHandler(w http.ResponseWriter, r *http.Request) {
	// Connect to local IPFS node
	sh := shell.NewShell("localhost:5001")

	// Check if the connection was successful
	if _, err := sh.ID(); err != nil {
		fmt.Println("Failed to connect to IPFS node")
	} else {
		fmt.Println("Connection successful!")
	}

	// Automatically create an IPFS node for the client
	clientSh := shell.NewLocalShell()
	if nodeInfo, err := clientSh.ID(); err != nil {
		fmt.Println("Failed to create IPFS node for client")
	} else {
		fmt.Printf("IPFS node created for client with ID %s\n", nodeInfo.ID)
	}

	// Print information about the local IPFS node
	if nodeInfo, err := sh.ID(); err != nil {
		fmt.Println("Failed to get information about local IPFS node")
	} else {
		fmt.Printf("Local IPFS node ID: %s\n", nodeInfo.ID)
		fmt.Printf("Local IPFS node agent version: %s\n", nodeInfo.AgentVersion)
		fmt.Printf("Local IPFS node protocol version: %s\n", nodeInfo.ProtocolVersion)

	}
}
