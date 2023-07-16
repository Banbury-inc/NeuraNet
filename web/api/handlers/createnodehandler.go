package handlers

import (
	"fmt"
	"log"
	"net/http"
	"os/exec"

	shell "github.com/ipfs/go-ipfs-api"
)

func CreateNodeHandler(w http.ResponseWriter, r *http.Request) {
	// Connect to local IPFS node
	sh := shell.NewShell("localhost:5001")

	// Check if the connection was successful
	if _, err := sh.ID(); err != nil {
		fmt.Println("Failed to connect to IPFS node, starting a new node")

		// Start a local IPFS node on port 5001
		err := exec.Command("ipfs", "daemon").Start()
		if err != nil {
			fmt.Println("Failed to start IPFS node:", err)
			return
		}

		// Retry connecting to the IPFS node
		sh = shell.NewShell("localhost:5001")
		if _, err := sh.ID(); err != nil {
			fmt.Println("Failed to connect to IPFS node after starting it:", err)
			return
		}
	}

	// Connection successful
	fmt.Println("Connection successful!")

	// Automatically create an IPFS node for the client
	clientSh := shell.NewShell("localhost:5001")
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
		fmt.Printf("Local IPFS node Public Key: %s\n", nodeInfo.PublicKey)
		//		fmt.Printf("Local IPFS node Addresses: %s\n", nodeInfo.Addresses)
		fmt.Printf("Local IPFS node agent version: %s\n", nodeInfo.AgentVersion)
		fmt.Printf("Local IPFS node protocol version: %s\n", nodeInfo.ProtocolVersion)

		// add the most recently connected node to the bootstrap list
		err = exec.Command("ipfs", "bootstrap", "add", fmt.Sprintf("/ip4/127.0.0.1/tcp/4001/ipfs/%s", nodeInfo.ID)).Run()
		if err != nil {
			log.Fatal(err)
		}
		if err != nil {
			fmt.Println("Failed to add node to bootstrap list:", err)
		}

	}

	// Print a list of all the IPFS nodes currently connected
	// Get a list of all the IPFS nodes currently connected

	// Run the `ipfs swarm peers` command
	cmd := exec.Command("ipfs", "bootstrap", "list")

	// Execute the command and capture its output
	output, err := cmd.Output()
	if err != nil {
		log.Fatal("Failed to run `ipfs swarm peers` command:", err)
	}

	// Print the result
	fmt.Println("Connected peers:")
	fmt.Println(string(output))
}
