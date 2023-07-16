package handlers

import (
	"fmt"
	"log"
	"net/http"
	"os/exec"
	"strings"
)

func CountPeersHandler(w http.ResponseWriter, r *http.Request) {
	command := exec.Command("ipfs", "bootstrap", "list")
	output, err := command.Output()
	if err != nil {
		log.Fatal(err)
	}

	// Convert the command output to string
	outputStr := string(output)

	// Split the output by newline to get individual items
	items := strings.Split(outputStr, "\n")

	// Remove empty item at the end of the list
	if len(items) > 0 && items[len(items)-1] == "" {
		items = items[:len(items)-1]
	}

	// Count the number of items
	count := len(items)

	// Print the count
	fmt.Fprintf(w, "Number of items in bootstrap list: %d\n", count)
}
