package handlers

import (
	"fmt"
	"log"
	"net/http"
	"os/exec"
)

func ListFilesHandler(w http.ResponseWriter, r *http.Request) {

	// Print a list of all the IPFS nodes currently connected
	// Get a list of all the IPFS nodes currently connected

	// Run the `ipfs swarm peers` command
	cmd := exec.Command("ipfs", "files", "ls")

	// Execute the command and capture its output
	output, err := cmd.Output()
	if err != nil {
		log.Fatal("Failed to run `ipfs swarm peers` command:", err)
	}

	// Print the result
	fmt.Fprintf(w, string(output))

}
