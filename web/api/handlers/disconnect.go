package handlers

import (
	"fmt"
	"log"
	"net/http"
	"os/exec"
)

func DisconnectAllPeersHandler(w http.ResponseWriter, r *http.Request) {
	// Run the `ipfs swarm disconnect -all` command
	cmd := exec.Command("ipfs", "bootstrap", "rm", "--all")

	// Execute the command and capture its output
	output, err := cmd.Output()
	if err != nil {
		log.Fatal("Failed to run `ipfs bootstrap rm --all` command:", err)
	}

	// Print the result
	fmt.Println("Connected peers:")
	fmt.Println(string(output))
}
