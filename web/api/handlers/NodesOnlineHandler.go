package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
)

var onlineNodeCount int
var numNodes int
var mu sync.Mutex
var onlineNodes []NodeInfo

// NodeInfo represents information about an IPFS node
type NodeInfo struct {
	ID      string `json:"id"`
	Version string `json:"version"`
	Addr    string `json:"address"`
	Proto   string `json:"protocol"`
}

func NodesOnlineHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()
	fmt.Fprintf(w, "%d nodes online", numNodes)
}

func NodeConnectedHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()
	onlineNodeCount++
	fmt.Printf("Node connected. Online nodes: %d\n", onlineNodeCount)
}

func NodeDisconnectedHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()
	onlineNodeCount--
	fmt.Printf("Node disconnected. Online nodes: %d\n", onlineNodeCount)
}

func main() {
	http.HandleFunc("/nodes", HomeHandler)
	http.HandleFunc("/nodes-online", NodesOnlineHandler)
	http.HandleFunc("/node-connected", NodeConnectedHandler)
	http.HandleFunc("/node-disconnected", NodeDisconnectedHandler)
	http.HandleFunc("/online-nodes", OnlineNodesHandler)
	http.HandleFunc("/disconnect", DisconnectAllPeersHandler)

	http.ListenAndServe(":8081", nil)
}

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()
	numNodes++
	fmt.Fprintf(w, "Welcome to my website! Number of nodes online: %d", numNodes)
}

func OnlineNodesHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	// Print the list of online nodes in the terminal
	fmt.Println("Online Nodes:")
	for _, node := range onlineNodes {
		fmt.Printf("ID: %s, Version: %s, Address: %s, Protocol: %s\n", node.ID, node.Version, node.Addr, node.Proto)
	}

	// Optionally, you can also send a response back to the HTTP request if needed
	fmt.Fprintf(w, "Online nodes printed in the terminal")

	// Convert onlineNodes slice to JSON
	jsonData, err := json.Marshal(onlineNodes)
	if err != nil {
		http.Error(w, "Failed to get online nodes", http.StatusInternalServerError)
		return
	}

	// Set the Content-Type header to application/json
	w.Header().Set("Content-Type", "application/json")

	// Write the JSON response
	w.Write(jsonData)
}

func LessHomeHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()
	numNodes--
}
