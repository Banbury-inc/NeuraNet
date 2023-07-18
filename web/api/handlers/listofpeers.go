package handlers

import (
	"fmt"
	"log"
	"net/http"
	"os/exec"
)

func ListofPeersHandler(w http.ResponseWriter, r *http.Request) {

	// Print a list of all the IPFS nodes currently connected
	// Get a list of all the IPFS nodes currently connected

	// Run the `ipfs swarm peers` command
	cmd2 := exec.Command("ipfs", "bootstrap", "list")

	// Execute the command and capture its output
	output2, err := cmd2.Output()
	if err != nil {
		log.Fatal("Failed to run `ipfs swarm peers` command:", err)
	}

	// Print the result
	fmt.Fprintf(w, string(output2))

}
